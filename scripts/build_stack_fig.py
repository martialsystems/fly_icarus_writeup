#!/usr/bin/env python3
# Copyright (c) 2026 Martial Systems LLC
"""One stack diagram: object tags to schema row to hop-1 to hop-2 LH to f table."""

from __future__ import annotations

from pathlib import Path

from reportlab.lib.units import inch
from reportlab.pdfgen import canvas

ROOT = Path(__file__).resolve().parents[1]
OUT_PDF = ROOT / "figures" / "stack.pdf"


def box(c: canvas.Canvas, x: float, y: float, w: float, h: float, title: str, lines: list[str], sha: str) -> None:
    c.setStrokeColorRGB(0.15, 0.15, 0.15)
    c.setFillColorRGB(0.97, 0.97, 0.97)
    c.roundRect(x, y, w, h, 3, fill=1, stroke=1)
    c.setFillColorRGB(0, 0, 0)
    c.setFont("Times-Bold", 9)
    c.drawString(x + 8, y + h - 14, title)
    c.setFont("Times-Roman", 8)
    ty = y + h - 28
    for line in lines:
        c.drawString(x + 8, ty, line)
        ty -= 11
    c.setFont("Times-Italic", 8)
    c.drawString(x + 8, y + 8, sha)


def h_arrow(c: canvas.Canvas, x0: float, y: float, x1: float) -> None:
    c.setStrokeColorRGB(0.2, 0.2, 0.2)
    c.setFillColorRGB(0.2, 0.2, 0.2)
    c.line(x0, y, x1, y)
    path = c.beginPath()
    path.moveTo(x1, y)
    path.lineTo(x1 - 6, y + 3)
    path.lineTo(x1 - 6, y - 3)
    path.close()
    c.drawPath(path, fill=1, stroke=0)


def v_arrow(c: canvas.Canvas, x: float, y0: float, y1: float) -> None:
    c.setStrokeColorRGB(0.2, 0.2, 0.2)
    c.setFillColorRGB(0.2, 0.2, 0.2)
    c.line(x, y0, x, y1)
    path = c.beginPath()
    path.moveTo(x, y1)
    path.lineTo(x - 3, y1 + 6)
    path.lineTo(x + 3, y1 + 6)
    path.close()
    c.drawPath(path, fill=1, stroke=0)


def main() -> None:
    OUT_PDF.parent.mkdir(parents=True, exist_ok=True)
    W, H = 7.4 * inch, 4.15 * inch
    c = canvas.Canvas(str(OUT_PDF), pagesize=(W, H))
    c.setFont("Times-Roman", 8)
    margin = 0.28 * inch
    bw, bh = 2.15 * inch, 1.35 * inch
    gapx, gapy = 0.28 * inch, 0.38 * inch
    top = H - 0.28 * inch - bh
    bot = top - bh - gapy
    row1 = [
        ("Object tags", ["HD, cVA, LC10a size", "cuticle, pin, wings"], "Icarus-from-male"),
        ("11-cell schema", ["HD-on / cVA-off only", "W=-1.8; W_crit=-1.5262"], "@2cf5fd6"),
        ("Hop-1 onto 88", ["LC10a +606", "DA1 +62 ACh; ppk23 0"], "@45aa064"),
    ]
    row2 = [
        ("mAL GABA", ["-8810 if assigned to cVA", "DA1 hop-1 to mAL_m* = 0"], "@e16856c"),
        ("Hop-2 LH", ["DA1 -> type-LH -> mAL", "8773 / 8810 touch"], "@de95257"),
        ("f table", ["f-bar 0.099; f-bar^PN 0.70", "LHAV4c2: 1012 with 5 DA1"], "@01155c3"),
    ]
    xs = [margin + i * (bw + gapx) for i in range(3)]
    for i, spec in enumerate(row1):
        box(c, xs[i], top, bw, bh, *spec)
    for i in range(2):
        h_arrow(c, xs[i] + bw, top + bh / 2, xs[i + 1])
    # hop-1 down, then left, then down onto mAL
    mid_y = bot + bh + gapy / 2
    x_right = xs[2] + bw / 2
    x_left = xs[0] + bw / 2
    c.setStrokeColorRGB(0.2, 0.2, 0.2)
    c.line(x_right, top, x_right, mid_y)
    c.line(x_right, mid_y, x_left, mid_y)
    v_arrow(c, x_left, mid_y, bot + bh)
    for i, spec in enumerate(row2):
        box(c, xs[i], bot, bw, bh, *spec)
    for i in range(2):
        h_arrow(c, xs[i] + bw, bot + bh / 2, xs[i + 1])
    c.setFont("Times-Italic", 7)
    c.drawString(margin, 0.12 * inch, "Locks stay on the trees. Pointer stack, not a new measurement.")
    c.save()
    import pypdfium2 as pdfium

    doc = pdfium.PdfDocument(str(OUT_PDF))
    img = doc[0].render(scale=160 / 72).to_pil()
    png = ROOT / "figures" / "stack.png"
    img.save(png)
    print("wrote", OUT_PDF, png)


if __name__ == "__main__":
    main()
