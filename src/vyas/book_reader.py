"""Classical Astrology Book Reader & Knowledge Engine for VYAS.

Automatically discovers, indexes, and searches PDF/text astrology treatises
in the `books/` repository using `pdfplumber`.
"""
import os
import re
from pathlib import Path
from typing import List, Dict, Optional, Tuple
import pdfplumber

BOOKS_DIR = Path(__file__).resolve().parents[2] / "books"

def get_books_dir() -> Path:
    BOOKS_DIR.mkdir(parents=True, exist_ok=True)
    return BOOKS_DIR

def list_available_books() -> List[Dict]:
    """Lists all astrology book files found in books/ directory."""
    b_dir = get_books_dir()
    books = []
    for f in sorted(b_dir.iterdir()):
        if f.is_file() and f.suffix.lower() in [".pdf", ".txt", ".md"]:
            size_mb = f.stat().st_size / (1024 * 1024)
            num_pages = None
            if f.suffix.lower() == ".pdf":
                try:
                    with pdfplumber.open(f) as pdf:
                        num_pages = len(pdf.pages)
                except Exception:
                    num_pages = "Error reading"
            books.append({
                "filename": f.name,
                "path": str(f),
                "extension": f.suffix.lower(),
                "size_mb": round(size_mb, 2),
                "pages": num_pages
            })
    return books

def search_books(query: str, book_filename: Optional[str] = None, max_results: int = 15) -> List[Dict]:
    """
    Searches across PDF books in the books/ folder for query terms (case-insensitive & Devanagari).
    Returns list of dicts with book title, page number, and snippet.
    """
    if not query or not query.strip():
        return []
    
    query = query.strip()
    b_dir = get_books_dir()
    results = []
    
    target_files = []
    if book_filename:
        p = b_dir / book_filename
        if p.is_file():
            target_files = [p]
    else:
        target_files = [f for f in sorted(b_dir.iterdir()) if f.is_file() and f.suffix.lower() in [".pdf", ".txt"]]
        
    for f in target_files:
        if f.suffix.lower() == ".pdf":
            try:
                with pdfplumber.open(f) as pdf:
                    for page_idx, page in enumerate(pdf.pages):
                        text = page.extract_text()
                        if not text:
                            continue
                        if re.search(re.escape(query), text, re.IGNORECASE):
                            # Extract context snippet around the match
                            match_idx = text.lower().find(query.lower())
                            start_snip = max(0, match_idx - 120)
                            end_snip = min(len(text), match_idx + len(query) + 180)
                            snippet = text[start_snip:end_snip].strip().replace("\n", " ")
                            results.append({
                                "book": f.name,
                                "page": page_idx + 1,
                                "snippet": f"... {snippet} ..."
                            })
                            if len(results) >= max_results:
                                return results
            except Exception as e:
                print(f"Error reading {f.name}: {e}")
        elif f.suffix.lower() in [".txt", ".md"]:
            try:
                with open(f, "r", encoding="utf-8", errors="ignore") as txt_f:
                    lines = txt_f.readlines()
                    for line_idx, line in enumerate(lines):
                        if re.search(re.escape(query), line, re.IGNORECASE):
                            results.append({
                                "book": f.name,
                                "page": f"Line {line_idx + 1}",
                                "snippet": line.strip()
                            })
                            if len(results) >= max_results:
                                return results
            except Exception as e:
                print(f"Error reading {f.name}: {e}")

    return results

def save_uploaded_book(filename: str, data: bytes) -> str:
    """Saves an uploaded book file into the books/ folder."""
    b_dir = get_books_dir()
    safe_name = os.path.basename(filename)
    dest_path = b_dir / safe_name
    with open(dest_path, "wb") as f:
        f.write(data)
    return str(dest_path)
