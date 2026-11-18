"""Download a public Google Drive book folder and convert every supported file to Markdown.

Text-layer PDFs use PyMuPDF. Image-only pages use Tesseract with Hindi and English.
The manifest makes the job resumable and records failures instead of silently skipping files.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from types import SimpleNamespace

import gdown
import fitz
from docx import Document
from gdown.download import _get_session
from gdown.download_folder import _GoogleDriveFile, _parse_embedded_folder_view
from striprtf.striprtf import rtf_to_text


ROOT = Path(__file__).resolve().parents[1]
BOOKS_DIR = ROOT / "books"
WORK_DIR = ROOT / "tmp" / "drive_books"
MANIFEST_PATH = BOOKS_DIR / "drive_book_conversion_manifest.jsonl"
SUPPORTED_EXTENSIONS = {".pdf", ".txt", ".md", ".doc", ".docx", ".rtf"}
TESSERACT = Path(r"C:\Program Files\Tesseract-OCR\tesseract.exe")
SOFFICE_CANDIDATES = (
    Path(r"C:\Program Files\LibreOffice\program\soffice.exe"),
    Path(r"C:\Program Files\LibreOffice 26\program\soffice.exe"),
)
ASSET_FOLDER_MARKERS = ("_files", "_data", "ads", "iframe", "index_data")


def slugify(name: str) -> str:
    stem = re.sub(r"[^\w.-]+", "_", name, flags=re.UNICODE).strip("._")
    return stem[:180] or "untitled"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def markdown_header(source: Path, source_id: str, extraction: str) -> str:
    return (
        f"# {source.stem}\n\n"
        f"- Source: Google Drive file `{source_id}`\n"
        f"- Original filename: `{source.name}`\n"
        f"- Extraction: {extraction}\n"
        f"- Converted (UTC): {datetime.now(timezone.utc).isoformat()}\n\n"
    )


def ocr_page(page: fitz.Page, page_number: int) -> str:
    if not TESSERACT.exists():
        raise RuntimeError("Hindi OCR requested but Tesseract is unavailable")
    image_path = WORK_DIR / f"ocr_{page_number}_{time.time_ns()}.png"
    output_base = image_path.with_suffix("")
    try:
        pixmap = page.get_pixmap(matrix=fitz.Matrix(2, 2), alpha=False)
        pixmap.save(image_path)
        completed = subprocess.run(
            [str(TESSERACT), str(image_path), str(output_base), "-l", "hin+eng", "--psm", "3"],
            capture_output=True,
            text=True,
            check=False,
        )
        output_path = output_base.with_suffix(".txt")
        if completed.returncode or not output_path.exists():
            raise RuntimeError(completed.stderr.strip() or "Tesseract produced no output")
        return output_path.read_text(encoding="utf-8", errors="replace").strip()
    finally:
        image_path.unlink(missing_ok=True)
        output_base.with_suffix(".txt").unlink(missing_ok=True)


def convert_pdf(source: Path, source_id: str) -> tuple[str, int, int]:
    document = fitz.open(source)
    pages, ocr_pages = [], 0
    for number, page in enumerate(document, start=1):
        text = page.get_text("text").strip()
        extraction = "text-layer"
        if len(re.sub(r"\s+", "", text)) < 80:
            text = ocr_page(page, number)
            extraction = "OCR (hin+eng)"
            ocr_pages += 1
        pages.append(f"## Page {number}\n\n<!-- {extraction} -->\n\n{text or '[No readable text extracted]'}")
    return markdown_header(source, source_id, "PDF text extraction with Hindi/English OCR fallback") + "\n\n".join(pages) + "\n", len(document), ocr_pages


def convert_file(source: Path, source_id: str) -> tuple[Path, int, int]:
    extension = source.suffix.lower()
    output = BOOKS_DIR / f"{slugify(source.stem)}__{source_id}.md"
    if extension == ".pdf":
        markdown, pages, ocr_pages = convert_pdf(source, source_id)
    elif extension in {".txt", ".md"}:
        body = source.read_text(encoding="utf-8", errors="replace")
        markdown = markdown_header(source, source_id, "direct text copy") + body + "\n"
        pages, ocr_pages = 0, 0
    elif extension == ".docx":
        document = Document(source)
        body = "\n\n".join(paragraph.text for paragraph in document.paragraphs if paragraph.text.strip())
        markdown = markdown_header(source, source_id, "DOCX text extraction") + body + "\n"
        pages, ocr_pages = 0, 0
    elif extension == ".rtf":
        body = rtf_to_text(source.read_text(encoding="utf-8", errors="replace"))
        markdown = markdown_header(source, source_id, "RTF text extraction") + body + "\n"
        pages, ocr_pages = 0, 0
    elif extension == ".doc":
        soffice = next((candidate for candidate in SOFFICE_CANDIDATES if candidate.exists()), None)
        if not soffice:
            raise RuntimeError("Legacy DOC conversion requires LibreOffice")
        conversion_dir = WORK_DIR / f"docx_{time.time_ns()}"
        conversion_dir.mkdir(parents=True, exist_ok=True)
        try:
            result = subprocess.run(
                [str(soffice), "--headless", "--convert-to", "docx", "--outdir", str(conversion_dir), str(source)],
                capture_output=True,
                text=True,
                check=False,
            )
            converted = conversion_dir / f"{source.stem}.docx"
            if result.returncode or not converted.exists():
                raise RuntimeError(result.stderr.strip() or "LibreOffice DOC conversion failed")
            document = Document(converted)
            body = "\n\n".join(paragraph.text for paragraph in document.paragraphs if paragraph.text.strip())
            markdown = markdown_header(source, source_id, "DOC to DOCX text extraction") + body + "\n"
            pages, ocr_pages = 0, 0
        finally:
            shutil.rmtree(conversion_dir, ignore_errors=True)
    else:
        raise RuntimeError(f"Unsupported input: {extension}")
    output.write_text(markdown, encoding="utf-8")
    return output, pages, ocr_pages


def existing_successes() -> set[str]:
    if not MANIFEST_PATH.exists():
        return set()
    successes = set()
    for line in MANIFEST_PATH.read_text(encoding="utf-8").splitlines():
        try:
            row = json.loads(line)
        except json.JSONDecodeError:
            continue
        if row.get("status") == "success":
            successes.add(row["drive_id"])
    return successes


def append_manifest(row: dict) -> None:
    with MANIFEST_PATH.open("a", encoding="utf-8") as target:
        target.write(json.dumps(row, ensure_ascii=False) + "\n")


def download_one(drive_file) -> Path:
    WORK_DIR.mkdir(parents=True, exist_ok=True)
    target = WORK_DIR / slugify(Path(drive_file.path).name)
    downloaded = gdown.download(id=drive_file.id, output=str(target), quiet=False)
    if not downloaded:
        raise RuntimeError("Google Drive download failed")
    return Path(downloaded)


def discover_books(folder_id: str):
    """Walk only document-bearing folders; Drive exports old web-page asset trees too."""
    session, _ = _get_session(proxy=None, use_cookies=True, user_agent=None, cookies_file=None)
    found = []
    seen = set()

    def walk(current_id: str, parent: Path) -> None:
        if current_id in seen:
            return
        seen.add(current_id)
        folder_name, children = _parse_embedded_folder_view(
            sess=session, folder_id=current_id, verify=True, timeout=(15, 120)
        )
        for child_id, child_name, child_type in children:
            child_path = parent / child_name
            if child_type == _GoogleDriveFile.TYPE_FOLDER:
                normalized = child_name.lower()
                if any(marker in normalized for marker in ASSET_FOLDER_MARKERS):
                    continue
                walk(child_id, child_path)
            elif Path(child_name).suffix.lower() in SUPPORTED_EXTENSIONS:
                found.append(SimpleNamespace(id=child_id, path=str(child_path)))

    try:
        walk(folder_id, Path(folder_id))
    finally:
        session.close()
    return found


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--folder-id", required=True)
    parser.add_argument("--limit", type=int, default=0, help="0 converts all discovered files")
    parser.add_argument("--keep-source", action="store_true")
    args = parser.parse_args()

    if not TESSERACT.exists():
        print("Hindi OCR engine missing:", TESSERACT, file=sys.stderr)
        return 2

    BOOKS_DIR.mkdir(exist_ok=True)
    WORK_DIR.mkdir(parents=True, exist_ok=True)
    completed = existing_successes()
    selected = discover_books(args.folder_id)
    if args.limit:
        selected = selected[: args.limit]
    print(f"Discovered {len(selected)} supported books; converting {len(selected)} files.")

    for index, drive_file in enumerate(selected, start=1):
        if drive_file.id in completed:
            print(f"[{index}/{len(selected)}] already converted: {drive_file.path}")
            continue
        source = None
        row = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "drive_id": drive_file.id,
            "drive_path": str(drive_file.path),
            "source_name": Path(drive_file.path).name,
        }
        try:
            print(f"[{index}/{len(selected)}] downloading: {drive_file.path}")
            source = download_one(drive_file)
            row["source_sha256"] = sha256(source)
            output, pages, ocr_pages = convert_file(source, drive_file.id)
            row.update({
                "status": "success",
                "output": str(output.relative_to(ROOT)),
                "output_sha256": sha256(output),
                "pages": pages,
                "ocr_pages": ocr_pages,
            })
            print(f"  converted: {output.name} ({pages} pages; OCR {ocr_pages})")
        except Exception as error:
            row.update({"status": "failed", "error": str(error)})
            print(f"  failed: {error}", file=sys.stderr)
        finally:
            append_manifest(row)
            if source and source.exists() and not args.keep_source:
                source.unlink()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
