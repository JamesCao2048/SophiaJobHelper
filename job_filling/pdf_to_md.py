from __future__ import annotations

import argparse
from collections.abc import Callable
from pathlib import Path


def list_pdfs(pdf_dir: Path) -> list[Path]:
    if not pdf_dir.exists():
        raise FileNotFoundError(str(pdf_dir))
    if not pdf_dir.is_dir():
        raise NotADirectoryError(str(pdf_dir))

    return sorted(
        [p for p in pdf_dir.iterdir() if p.is_file() and p.suffix.lower() == ".pdf"],
        key=lambda p: p.name.lower(),
    )


def pdf_path_to_md_path(pdf_path: Path, output_dir: Path | None) -> Path:
    if output_dir is None:
        return pdf_path.with_suffix(".md")
    return output_dir / f"{pdf_path.stem}.md"


def convert_pdf_to_markdown(pdf_path: Path) -> str:
    try:
        import fitz
    except ImportError as e:
        raise RuntimeError(
            "缺少依赖 PyMuPDF：请先运行 `python3 -m pip install pymupdf`"
        ) from e

    doc = fitz.open(pdf_path)
    try:
        parts: list[str] = []
        for page in doc:
            text = (page.get_text("text") or "").rstrip()
            if text:
                parts.append(text)
        body = "\n\n".join(parts).strip()
    finally:
        doc.close()

    title = pdf_path.stem
    if body:
        return f"# {title}\n\n{body}\n"
    return f"# {title}\n"


def convert_dir(
    pdf_dir: Path,
    output_dir: Path | None = None,
    overwrite: bool = False,
    converter: Callable[[Path], str] | None = None,
) -> list[Path]:
    converter = converter or convert_pdf_to_markdown

    written: list[Path] = []
    for pdf_path in list_pdfs(pdf_dir):
        md_path = pdf_path_to_md_path(pdf_path, output_dir=output_dir)
        md_path.parent.mkdir(parents=True, exist_ok=True)

        if md_path.exists() and not overwrite:
            continue

        md_text = converter(pdf_path)
        md_path.write_text(md_text, encoding="utf-8")
        written.append(md_path)

    return written


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Convert PDFs in a directory to .md")
    parser.add_argument("pdf_dir", type=Path)
    parser.add_argument("--output-dir", type=Path, default=None)
    parser.add_argument("--overwrite", action="store_true")
    args = parser.parse_args(argv)

    written = convert_dir(
        args.pdf_dir,
        output_dir=args.output_dir,
        overwrite=args.overwrite,
    )
    print(f"written {len(written)} files")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
