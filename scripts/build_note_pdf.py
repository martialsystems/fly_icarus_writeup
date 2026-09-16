#!/usr/bin/env python3
# Copyright (c) 2026 Martial Systems LLC
"""Research-format PDF of NOTE.md. Not a finding."""

from __future__ import annotations

import re
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    Image,
    KeepTogether,
    ListFlowable,
    ListItem,
    PageBreak,
    Paragraph,
    Preformatted,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

ROOT = Path(__file__).resolve().parents[1]
NOTE = ROOT / "NOTE.md"
FIG = ROOT / "figures" / "stack.png"
OUT = ROOT / "docs" / "fly_icarus_chain_note.pdf"

DATE = "2026-09-16"


def styles():
    s = getSampleStyleSheet()
    s.add(
        ParagraphStyle(
            name="PaperTitle",
            fontName="Times-Bold",
            fontSize=14,
            leading=18,
            alignment=TA_CENTER,
            spaceAfter=8,
        )
    )
    s.add(
        ParagraphStyle(
            name="Meta",
            fontName="Times-Roman",
            fontSize=10,
            leading=13,
            alignment=TA_CENTER,
            spaceAfter=4,
        )
    )
    s.add(
        ParagraphStyle(
            name="AbsHead",
            fontName="Times-Bold",
            fontSize=11,
            leading=14,
            spaceBefore=12,
            spaceAfter=6,
        )
    )
    s.add(
        ParagraphStyle(
            name="AbsBody",
            fontName="Times-Roman",
            fontSize=10,
            leading=13,
            alignment=TA_JUSTIFY,
            spaceAfter=8,
            firstLineIndent=0,
        )
    )
    s.add(
        ParagraphStyle(
            name="H",
            fontName="Times-Bold",
            fontSize=11,
            leading=14,
            spaceBefore=12,
            spaceAfter=6,
        )
    )
    s.add(
        ParagraphStyle(
            name="BodyJ",
            fontName="Times-Roman",
            fontSize=10,
            leading=13,
            alignment=TA_JUSTIFY,
            spaceAfter=8,
            firstLineIndent=12,
        )
    )
    s.add(
        ParagraphStyle(
            name="BodyJ0",
            fontName="Times-Roman",
            fontSize=10,
            leading=13,
            alignment=TA_JUSTIFY,
            spaceAfter=8,
            firstLineIndent=0,
        )
    )
    s.add(
        ParagraphStyle(
            name="Cap",
            fontName="Times-Italic",
            fontSize=9,
            leading=12,
            alignment=TA_LEFT,
            spaceBefore=4,
            spaceAfter=10,
        )
    )
    s.add(
        ParagraphStyle(
            name="Cell",
            fontName="Times-Roman",
            fontSize=8,
            leading=10,
        )
    )
    s.add(
        ParagraphStyle(
            name="CellB",
            fontName="Times-Bold",
            fontSize=8,
            leading=10,
        )
    )
    s.add(
        ParagraphStyle(
            name="Foot",
            fontName="Times-Roman",
            fontSize=8,
            leading=10,
            alignment=TA_CENTER,
        )
    )
    s.add(
        ParagraphStyle(
            name="Kw",
            fontName="Times-Roman",
            fontSize=10,
            leading=13,
            spaceAfter=8,
        )
    )
    return s


def inline(text: str) -> str:
    text = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    text = re.sub(r"`([^`]+)`", r"<font face='Courier' size='8'>\1</font>", text)
    text = re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", text)
    text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r"<link href='\2'>\1</link>", text)
    return text


def parse_note() -> list[tuple[str, object]]:
    lines = NOTE.read_text(encoding="utf-8").splitlines()
    blocks: list[tuple[str, object]] = []
    i = 0
    # skip H1; PDF has its own title
    if lines and lines[0].startswith("# "):
        i = 1
        while i < len(lines) and not lines[i].strip():
            i += 1
    while i < len(lines):
        line = lines[i]
        if line.startswith("## "):
            blocks.append(("h", line[3:].strip()))
            i += 1
            continue
        if line.startswith("!["):
            i += 1
            continue
        if line.startswith("|"):
            rows = []
            while i < len(lines) and lines[i].startswith("|"):
                raw = lines[i].strip()
                cells = [c.strip() for c in raw.strip("|").split("|")]
                if not all(re.fullmatch(r":?-{3,}:?", c.replace(" ", "")) for c in cells):
                    rows.append(cells)
                i += 1
            blocks.append(("table", rows))
            continue
        if not line.strip():
            i += 1
            continue
        para = [line]
        i += 1
        while i < len(lines) and lines[i].strip() and not lines[i].startswith("#") and not lines[i].startswith("|"):
            para.append(lines[i])
            i += 1
        blocks.append(("p", " ".join(para)))
    return blocks


def header_footer(canvas, doc) -> None:
    canvas.saveState()
    canvas.setFont("Times-Roman", 8)
    canvas.drawString(inch, letter[1] - 0.55 * inch, "fly_icarus chain: note  (not a result)")
    canvas.drawRightString(letter[0] - inch, letter[1] - 0.55 * inch, DATE)
    canvas.line(inch, letter[1] - 0.62 * inch, letter[0] - inch, letter[1] - 0.62 * inch)
    canvas.drawCentredString(letter[0] / 2, 0.5 * inch, f"{doc.page}")
    canvas.restoreState()


def build() -> Path:
    st = styles()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    story = []
    story.append(Paragraph("The Icarus costume is not a hop-1 identity switch", st["PaperTitle"]))
    story.append(
        Paragraph(
            "A note on the fly_icarus chain. Not a result. Locks stay on the trees.",
            st["Meta"],
        )
    )
    story.append(Paragraph("Martial Systems LLC", st["Meta"]))
    story.append(Paragraph(DATE, st["Meta"]))
    story.append(
        Paragraph(
            "Index of locks: https://gist.github.com/martialsystems/12835f747d6360781f3cc7f91f243178",
            st["Meta"],
        )
    )

    blocks = parse_note()
    first_p = True
    for kind, payload in blocks:
        if kind == "h":
            title = str(payload)
            if title.lower() == "abstract":
                story.append(Paragraph("Abstract", st["AbsHead"]))
                first_p = True
                continue
            if title.startswith("1."):
                story.append(Paragraph("Keywords", st["H"]))
                story.append(
                    Paragraph(
                        "Drosophila melanogaster; P1; Icarus; cVA; 7,11-HD; LC10a; mAL; MaleCNS; hop-1; hop-2.",
                        st["Kw"],
                    )
                )
            story.append(Paragraph(inline(title), st["H"]))
            first_p = True
            continue
        if kind == "p":
            text = str(payload)
            style = st["AbsBody"] if first_p else st["BodyJ"]
            # abstract paragraphs: no indent
            if story and isinstance(story[-1], Paragraph) and story[-1].style.name == "AbsHead":
                style = st["AbsBody"]
            elif first_p:
                style = st["BodyJ0"]
            story.append(Paragraph(inline(text), style))
            first_p = False
            continue
        if kind == "table":
            rows = payload
            cell = st["Cell"]
            cellb = st["CellB"]
            data = []
            for r_i, row in enumerate(rows):
                data.append(
                    [Paragraph(inline(c), cellb if r_i == 0 else cell) for c in row]
                )
            n = len(rows[0])
            usable = 6.5 * inch
            if n == 3:
                widths = [1.25 * inch, 2.35 * inch, 2.9 * inch]
            elif n == 4:
                widths = [1.2 * inch, 0.72 * inch, 3.18 * inch, 1.4 * inch]
            else:
                widths = [usable / n] * n
            tbl = Table(data, colWidths=widths, repeatRows=1)
            tbl.setStyle(
                TableStyle(
                    [
                        ("GRID", (0, 0), (-1, -1), 0.4, colors.Color(0.4, 0.4, 0.4)),
                        ("BACKGROUND", (0, 0), (-1, 0), colors.Color(0.92, 0.92, 0.92)),
                        ("VALIGN", (0, 0), (-1, -1), "TOP"),
                        ("LEFTPADDING", (0, 0), (-1, -1), 4),
                        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
                        ("TOPPADDING", (0, 0), (-1, -1), 3),
                        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
                    ]
                )
            )
            story.append(tbl)
            story.append(Spacer(1, 8))
            first_p = True

    if FIG.is_file():
        from reportlab.lib.utils import ImageReader

        reader = ImageReader(str(FIG))
        iw, ih = reader.getSize()
        w = 6.5 * inch
        h = w * (ih / iw)
        img = Image(str(FIG), width=w, height=h)
        img.hAlign = "CENTER"
        story.append(
            KeepTogether(
                [
                    Paragraph(
                        "Figure 1. Object tags to schema row to hop-1 counts to hop-2 LH to the f table (2026-09-16).",
                        st["H"],
                    ),
                    img,
                    Paragraph(
                        "Pointer stack across the locked trees. Not a new measurement.",
                        st["Cap"],
                    ),
                ]
            )
        )

    story.append(Paragraph("Revisions (2026-09-16)", st["H"]))
    story.append(
        Paragraph(
            "2026-09-16: first note from the locked trees. Same day: dropped the Not-stack; sentences taken from the lock files. Index gist 12835f74 left unedited.",
            st["BodyJ0"],
        )
    )

    doc = SimpleDocTemplate(
        str(OUT),
        pagesize=letter,
        leftMargin=inch,
        rightMargin=inch,
        topMargin=0.85 * inch,
        bottomMargin=0.75 * inch,
        title="The Icarus costume is not a hop-1 identity switch",
        author="Martial Systems LLC",
        subject="Note on the fly_icarus chain. Not a result.",
    )
    doc.build(story, onFirstPage=header_footer, onLaterPages=header_footer)
    print("wrote", OUT)
    return OUT


if __name__ == "__main__":
    build()
