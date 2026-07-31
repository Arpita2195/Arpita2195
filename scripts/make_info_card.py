"""
Generate a Neofetch-style SVG info card for Arpita Nathwani.
Designed to sit side-by-side with the ASCII portrait (490px wide x matching height).

Outputs: info-card.svg and wordmark.svg
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "..", "info-card.svg")

CANVAS_W = 490
CANVAS_H = 885 # matches 100x53 ASCII portrait height nicely
TITLEBAR_H = 30
PAD = 20

BG = "#0d1117"
BG2 = "#111722"
FRAME = "#30363d"
TITLE_TEXT = "#7d8590"
TEXT = "#c9d1d9"
PINK = "#ff2e88"
PURPLE = "#a78bfa"
TEAL = "#22d3ee"
YELLOW = "#f2cc60"
GREEN = "#39d353"
MUTED = "#8b949e"

rows = [
    ("OS", "MERN & Full Stack Ecosystem", PINK),
    ("Role", "Full Stack Developer", PURPLE),
    ("Portfolio", "portfolio-arpita-21.vercel.app", TEAL),
    ("Frontend", "React.js, Angular, HTML5, CSS3", TEXT),
    ("Backend", "Node.js, Express.js, REST APIs", TEXT),
    ("Database", "MongoDB, Firebase, SQL", TEXT),
    ("Languages", "JavaScript (ES6+), TypeScript", YELLOW),
    ("Tools", "Git, GitHub, Vercel, Postman", TEXT),
    ("Status", "⚡ Open for Opportunities & Internships", GREEN),
]

parts = []
parts.append(
    f'<svg xmlns="http://www.w3.org/2000/svg" width="{CANVAS_W}" height="{CANVAS_H}" '
    f'viewBox="0 0 {CANVAS_W} {CANVAS_H}" font-family="ui-monospace, SFMono-Regular, '
    f'Menlo, Consolas, monospace">'
)

# CSS Animation for staggered line fade/slide in
parts.append('''<style>
  @keyframes lineIn {
    0% { opacity: 0; transform: translateY(5px); }
    100% { opacity: 1; transform: translateY(0); }
  }
  .row { opacity: 0; animation: lineIn 0.4s cubic-bezier(0.16, 1, 0.3, 1) forwards; }
</style>''')

parts.append('<defs>'
             f'<linearGradient id="icbg" x1="0" y1="0" x2="0" y2="1">'
             f'<stop offset="0" stop-color="{BG2}"/><stop offset="1" stop-color="{BG}"/>'
             f'</linearGradient></defs>')

parts.append(f'<rect width="{CANVAS_W}" height="{CANVAS_H}" rx="12" fill="url(#icbg)"/>')
parts.append(f'<rect x="0.5" y="0.5" width="{CANVAS_W-1}" height="{CANVAS_H-1}" rx="12" '
             f'fill="none" stroke="{FRAME}" stroke-width="1"/>')

# Title bar
parts.append(f'<line x1="0" y1="{TITLEBAR_H}" x2="{CANVAS_W}" y2="{TITLEBAR_H}" stroke="{FRAME}"/>')
for i, dotcol in enumerate(["#ff5f56", "#ffbd2e", "#27c93f"]):
    parts.append(f'<circle cx="{PAD + i*16}" cy="{TITLEBAR_H/2}" r="5" fill="{dotcol}"/>')
parts.append(f'<text x="{CANVAS_W/2}" y="{TITLEBAR_H/2 + 4}" fill="{TITLE_TEXT}" font-size="12" '
             f'text-anchor="middle">arpita@github: ~$ neofetch</text>')

# User Logo/Art Header inside card
curr_y = TITLEBAR_H + 45
parts.append(f'<text class="row" style="animation-delay:0.05s" x="{PAD}" y="{curr_y}" fill="{PINK}" font-size="22" font-weight="bold">Arpita Nathwani</text>')
curr_y += 24
parts.append(f'<text class="row" style="animation-delay:0.1s" x="{PAD}" y="{curr_y}" fill="{MUTED}" font-size="13">---------------------------------------</text>')

curr_y += 35
# Render rows with staggered animation
for idx, (label, val, col) in enumerate(rows):
    delay = 0.15 + idx * 0.08
    parts.append(f'<g class="row" style="animation-delay:{delay:.2f}s">')
    parts.append(f'<text x="{PAD}" y="{curr_y}" fill="{PURPLE}" font-size="13" font-weight="bold">{label:<10}</text>')
    parts.append(f'<text x="{PAD + 105}" y="{curr_y}" fill="{MUTED}" font-size="13">::</text>')
    parts.append(f'<text x="{PAD + 130}" y="{curr_y}" fill="{col}" font-size="13">{val}</text>')
    parts.append('</g>')
    curr_y += 42

curr_y += 10
parts.append(f'<text class="row" style="animation-delay:0.95s" x="{PAD}" y="{curr_y}" fill="{MUTED}" font-size="13">---------------------------------------</text>')
curr_y += 35

# Color swatches row
parts.append(f'<g class="row" style="animation-delay:1.05s">')
swatch_cols = ["#161b22", "#ff5f56", "#39d353", "#f2cc60", "#22d3ee", "#a78bfa", "#ff2e88", "#e6edf3"]
for idx, sc in enumerate(swatch_cols):
    parts.append(f'<rect x="{PAD + idx * 36}" y="{curr_y}" width="28" height="16" rx="3" fill="{sc}"/>')
parts.append('</g>')

parts.append("</svg>")
svg = "".join(parts)

with open(OUT, "w", encoding="utf-8") as f:
    f.write(svg)

# Also write wordmark.svg as alias so existing layout/imports work seamless
wordmark_out = os.path.join(HERE, "..", "wordmark.svg")
with open(wordmark_out, "w", encoding="utf-8") as f:
    f.write(svg)

print("wrote", OUT, "and wordmark.svg", len(svg), "bytes;")
