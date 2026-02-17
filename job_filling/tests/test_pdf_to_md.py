import os
from pathlib import Path

import pytest


def test_pdf_path_to_md_path_preserves_name_and_directory():
    from pdf_to_md import pdf_path_to_md_path

    pdf_path = Path("/tmp/A Taxonomy for Human-LLM Interaction Modes.pdf")
    md_path = pdf_path_to_md_path(pdf_path, output_dir=None)

    assert md_path.parent == pdf_path.parent
    assert md_path.name == "A Taxonomy for Human-LLM Interaction Modes.md"


def test_convert_dir_writes_markdown_files(tmp_path: Path):
    from pdf_to_md import convert_dir

    materials_dir = tmp_path / "materials"
    materials_dir.mkdir()

    (materials_dir / "a.pdf").write_bytes(b"%PDF-1.4\n%fake\n")
    (materials_dir / "b with space.pdf").write_bytes(b"%PDF-1.4\n%fake\n")

    written_paths = convert_dir(
        materials_dir,
        output_dir=None,
        overwrite=True,
        converter=lambda p: f"# {p.stem}\n\nhello\n",
    )

    assert {p.name for p in written_paths} == {"a.md", "b with space.md"}
    for md_path in written_paths:
        assert md_path.exists()
        assert md_path.read_text(encoding="utf-8").strip()


def test_convert_dir_skips_existing_files_by_default(tmp_path: Path):
    from pdf_to_md import convert_dir

    materials_dir = tmp_path / "materials"
    materials_dir.mkdir()

    (materials_dir / "a.pdf").write_bytes(b"%PDF-1.4\n%fake\n")
    (materials_dir / "a.md").write_text("existing", encoding="utf-8")

    written_paths = convert_dir(
        materials_dir,
        output_dir=None,
        overwrite=False,
        converter=lambda p: "new",
    )

    assert written_paths == []
    assert (materials_dir / "a.md").read_text(encoding="utf-8") == "existing"
