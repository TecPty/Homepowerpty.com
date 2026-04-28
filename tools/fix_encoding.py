"""
fix_encoding.py — Fix mojibake in HTML files.

Root cause: text was UTF-8, treated as Latin-1/cp1252, stored as-is.
The browser reads the file as UTF-8 (per meta charset) and shows garbled chars.

Strategy: targeted find-replace of known mojibake sequences.
Ordered longest-first to avoid partial replacements.
"""

import pathlib
import sys

# Patterns sorted longest-first
FIXES = [
    # em-dash, en-dash
    # em dash — (U+2014): UTF-8 E2 80 94 → cp1252: â+€+\u201d (right double quote, cp1252 0x94)
    ("\u00e2\u20ac\u201d", "\u2014"),   # â€\u201d → —
    # en dash – (U+2013): UTF-8 E2 80 93 → cp1252: â+€+\u201c (left double quote, cp1252 0x93)
    ("\u00e2\u20ac\u201c", "\u2013"),   # â€\u201c → –
    # smart quotes
    ("\u00e2\u20ac\u0153", "\u201c"),   # â€œ → "
    ("\u00e2\u20ac\u009d", "\u201d"),   # â€\x9d → "
    ("\u00e2\u20ac\u02dc", "\u2018"),   # â€˜ → '
    ("\u00e2\u20ac\u2122", "\u2019"),   # â€™ → '
    ("\u00e2\u20ac\u00a6", "\u2026"),   # â€¦ → …
    ("\u00e2\u20ac\u00ba", "\u203a"),   # â€º → ›
    ("\u00e2\u20ac\u00b9", "\u2039"),   # â€¹ → ‹
    # lowercase accented vowels
    ("\u00c3\u00a1", "\u00e1"),   # Ã¡ → á
    ("\u00c3\u00a9", "\u00e9"),   # Ã© → é
    ("\u00c3\u00ad", "\u00ed"),   # Ã­ → í
    ("\u00c3\u00b3", "\u00f3"),   # Ã³ → ó
    ("\u00c3\u00ba", "\u00fa"),   # Ãº → ú
    ("\u00c3\u00b1", "\u00f1"),   # Ã± → ñ
    ("\u00c3\u00a0", "\u00e0"),   # Ã  → à
    ("\u00c3\u00a8", "\u00e8"),   # Ã¨ → è
    ("\u00c3\u00b2", "\u00f2"),   # Ã² → ò
    ("\u00c3\u00b9", "\u00f9"),   # Ã¹ → ù
    ("\u00c3\u00a7", "\u00e7"),   # Ã§ → ç
    ("\u00c3\u00bc", "\u00fc"),   # Ã¼ → ü
    # uppercase accented
    ("\u00c3\u0081", "\u00c1"),   # Ã\x81 → Á
    ("\u00c3\u0089", "\u00c9"),   # Ã\x89 → É
    ("\u00c3\u008d", "\u00cd"),   # Ã\x8d → Í
    ("\u00c3\u0093", "\u00d3"),   # Ã\x93 → Ó
    ("\u00c3\u009a", "\u00da"),   # Ã\x9a → Ú
    ("\u00c3\u0091", "\u00d1"),   # Ã\x91 → Ñ
    ("\u00c3\u0087", "\u00c7"),   # Ã\x87 → Ç
    ("\u00c3\u009c", "\u00dc"),   # Ã\x9c → Ü
    # misc symbols
    ("\u00c2\u00b7", "\u00b7"),   # Â· → ·
    ("\u00c2\u00a9", "\u00a9"),   # Â© → ©
    ("\u00c2\u00b0", "\u00b0"),   # Â° → °
    ("\u00c2\u00ba", "\u00ba"),   # Âº → º
    ("\u00c2\u00ab", "\u00ab"),   # Â« → «
    ("\u00c2\u00bb", "\u00bb"),   # Â» → »
    ("\u00c2\u00a0", "\u00a0"),   # Â\xa0 → NBSP
    ("\u00c2\u00ae", "\u00ae"),   # Â® → ®
    ("\u00c2\u00bf", "\u00bf"),   # Â¿ → ¿
    ("\u00c2\u00a1", "\u00a1"),   # Â¡ → ¡
]


def fix_file(path: pathlib.Path, dry_run: bool = False) -> int:
    text = path.read_text(encoding="utf-8-sig")  # strips BOM if present
    fixed = text
    for bad, good in FIXES:
        fixed = fixed.replace(bad, good)
    if fixed == text:
        return 0
    changes = sum(1 for a, b in zip(text.splitlines(), fixed.splitlines()) if a != b)
    if not dry_run:
        path.write_text(fixed, encoding="utf-8")
    return changes


def main():
    dry = "--dry" in sys.argv
    root = pathlib.Path(".")

    targets = list(root.glob("productos/**/*.html")) + [root / "index.html"]
    targets = [p for p in targets if "backup" not in str(p) and "index-backup" not in p.name]

    total_files = 0
    total_changes = 0
    for path in sorted(targets):
        n = fix_file(path, dry_run=dry)
        if n:
            total_files += 1
            total_changes += n
            print(f"  {'[DRY] ' if dry else ''}fixed {n:3d} lines  {path}")

    print(f"\n{'DRY RUN — ' if dry else ''}Fixed {total_changes} lines across {total_files} files.")


if __name__ == "__main__":
    main()
