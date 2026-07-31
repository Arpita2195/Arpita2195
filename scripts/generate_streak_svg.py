#!/usr/bin/env python3
"""
Wrapper for streak/heatmap SVG rendering.
Usage: python scripts/generate_streak_svg.py [username] [output.svg]
"""
import sys
import os
import render_heatmap_svg

if __name__ == "__main__":
    render_heatmap_svg.main() if hasattr(render_heatmap_svg, 'main') else None
    IN_PATH = render_heatmap_svg.IN_PATH
    OUT_PATH = sys.argv[2] if len(sys.argv) > 2 else render_heatmap_svg.OUT_PATH
    if os.path.exists(IN_PATH):
        with open(IN_PATH, "r", encoding="utf-8") as f:
            data = render_heatmap_svg.json.load(f)
        svg = render_heatmap_svg.render(data)
        with open(OUT_PATH, "w", encoding="utf-8") as f:
            f.write(svg)
        print(f"wrote {OUT_PATH} via generate_streak_svg wrapper")
