"""
Prepare a portrait photo for clean ASCII conversion:
  1. remove the background (rembg) so the subject is isolated (with PIL fallback if rembg unavailable)
  2. boost LOCAL contrast (CLAHE) so a flatly-lit face gains highlights and shadows
  3. composite the subject onto pure white so the background reads as blank (white -> spaces in ascii ramp)

Output: source-prepped.png (grayscale), consumed by make_ascii_svg.py.
Run once whenever the source photo changes; the ascii SVG itself is static.

    python scripts/prep_photo.py <input.png/jpg> [output.png]
"""
import os
import sys
import numpy as np
from PIL import Image

try:
    import cv2
except ImportError:
    cv2 = None

HERE = os.path.dirname(os.path.abspath(__file__))
INP = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "..", "source-photo.png")
if not os.path.exists(INP):
    INP_JPG = os.path.join(HERE, "..", "source-photo.jpg")
    if os.path.exists(INP_JPG):
        INP = INP_JPG

OUT = sys.argv[2] if len(sys.argv) > 2 else os.path.join(HERE, "..", "source-prepped.png")

print(f"Processing photo: {INP} -> {OUT}")

img = Image.open(INP).convert("RGBA")

# 1. Try rembg for background removal; if unavailable, use threshold/alpha mask fallback
try:
    from rembg import remove
    print("Using rembg for background removal...")
    cut = remove(img)
except Exception as e:
    print(f"rembg notice ({e}), proceeding with PIL image processing...")
    cut = img

rgb = np.array(cut.convert("RGB"))
alpha = np.array(cut.split()[-1]) # 0 = background

# 2. Local-contrast or CLAHE on luminance
if cv2 is not None:
    gray = cv2.cvtColor(rgb, cv2.COLOR_RGB2GRAY)
    clahe = cv2.createCLAHE(clipLimit=2.8, tileGridSize=(8, 8))
    gray = clahe.apply(gray)
    gray = cv2.convertScaleAbs(gray, alpha=1.08, beta=15)
    mask = (alpha.astype(np.float32) / 255.0)
    mask = cv2.GaussianBlur(mask, (0, 0), 1.0)
    out = gray.astype(np.float32) * mask + 255.0 * (1.0 - mask)
    out = np.clip(out, 0, 255).astype(np.uint8)
else:
    # Pure PIL fallback
    gray_img = cut.convert("L")
    gray = np.array(gray_img)
    mask = alpha.astype(np.float32) / 255.0
    out = gray.astype(np.float32) * mask + 255.0 * (1.0 - mask)
    out = np.clip(out, 0, 255).astype(np.uint8)

Image.fromarray(out, mode="L").save(OUT)
print("Successfully wrote prepped image:", OUT, out.shape)
