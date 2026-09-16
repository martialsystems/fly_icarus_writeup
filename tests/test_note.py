# Copyright (c) 2026 Martial Systems LLC
from __future__ import annotations

import re
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
NOTE = REPO / "NOTE.md"
README = REPO / "README.md"
SHAS = ("2cf5fd6", "45aa064", "e16856c", "41437dc", "de95257", "01155c3")
INDEX = "12835f747d6360781f3cc7f91f243178"


def test_note_is_not_a_finding_lede() -> None:
    text = NOTE.read_text(encoding="utf-8")
    assert text.startswith("# fly_icarus chain: note\n")
    body = text.split("\n", 1)[1].lstrip()
    assert body.startswith("Not a finding.")
    lede = "\n".join(text.splitlines()[:12])
    assert not any(ln.startswith("| condition") for ln in lede.splitlines())
    assert "What this is not" in text
    assert "What was never run" in text
    assert "unfreeze" in text.lower()
    assert "n=1000" in text or "`--n 1000`" in text
    assert "—" not in text
    assert INDEX in text
    for sha in SHAS:
        assert sha in text
    assert "hd_on_cva_off_ns=true" in text
    # that token is only allowed as a denied map result
    idx = text.find("hd_on_cva_off_ns=true")
    window = text[max(0, idx - 80) : idx + 80]
    assert "map result" in window or "Not" in window
    words = re.findall(r"[A-Za-z0-9][A-Za-z0-9'./_-]*", text)
    assert 800 <= len(words) <= 1400


def test_readme_points_at_note_and_index() -> None:
    text = README.read_text(encoding="utf-8")
    assert text.startswith("# fly_icarus_writeup\n")
    assert "Not a finding" in text
    assert "NOTE.md" in text
    assert INDEX in text
    assert "—" not in text
    desc = (REPO / "description.txt").read_text(encoding="utf-8")
    assert "Not a finding" in desc
    assert "—" not in desc


def test_pdf_and_figure_exist() -> None:
    import pypdfium2 as pdfium

    pdf_path = REPO / "docs" / "fly_icarus_chain_note.pdf"
    fig = REPO / "figures" / "stack.png"
    assert pdf_path.is_file() and pdf_path.stat().st_size > 1000
    assert fig.is_file() and fig.stat().st_size > 1000
    pdf = pdfium.PdfDocument(str(pdf_path))
    text = "\n".join(pdf[i].get_textpage().get_text_bounded() for i in range(len(pdf)))
    assert "Abstract" in text
    assert "2cf5fd6" in text
    assert "01155c3" in text
    assert "Revisions" in text
    assert "2026-09-16" in text
    assert "Keywords" in text
    assert len(pdf) >= 2
