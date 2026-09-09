#!/usr/bin/env python3
"""
HP-SEO-AI-001C — deterministic Product JSON-LD rollout for static PDPs.

Modes:
  --check  Preflight only. Never writes files.
  --apply  Preflight all targets first; writes only if the complete set is valid.

Source of truth is the current PDP HTML only:
  canonical, .pdp-name, .pdp-model, .pdp-short-desc, og:image
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PRODUCTS_ROOT = ROOT / "productos"
EXPECTED_PENDING = 112
ORG_ID = "https://www.homepowerpty.com/#organization"

GROUPED_FROZEN = {
    "productos/arroceras/arrocera-ht/index.html",
    "productos/arroceras/arrocera-vaporera-hta/index.html",
    "productos/calderos/caldero-aluminio/index.html",
    "productos/calderos/caldero-vidrio/index.html",
    "productos/extensiones/cable-extension/index.html",
    "productos/extensiones/extension-amarilla/index.html",
    "productos/extensiones/extension-naranja/index.html",
    "productos/ollas/olla-presion-aluminio/index.html",
    "productos/ollas/olla-presion-ck02/index.html",
    "productos/regletas/regleta-variantes/index.html",
}

PILOT_FROZEN = {
    "productos/procesador de alimento/hp-022/index.html",
    "productos/freidoras-de-aire/af3201/index.html",
    "productos/licuadoras/vb-999/index.html",
    "productos/extensiones/hp-054/index.html",
    "productos/soportes-tv/hp-041/index.html",
}

FROZEN = GROUPED_FROZEN | PILOT_FROZEN

SCRIPT_RE = re.compile(
    r'<script[^>]+type=["\']application/ld\+json["\'][^>]*>([\s\S]*?)</script>',
    re.I,
)
CANONICAL_RE = re.compile(
    r'<link[^>]+rel=["\']canonical["\'][^>]+href=["\']([^"\']+)["\']',
    re.I,
)
NAME_RE = re.compile(
    r'<h1[^>]*class=["\'][^"\']*\bpdp-name\b[^"\']*["\'][^>]*>([\s\S]*?)</h1>',
    re.I,
)
MODEL_RE = re.compile(
    r'<[^>]+class=["\'][^"\']*\bpdp-model\b[^"\']*["\'][^>]*>([\s\S]*?)</[^>]+>',
    re.I,
)
DESC_RE = re.compile(
    r'<[^>]+class=["\'][^"\']*\bpdp-short-desc\b[^"\']*["\'][^>]*>([\s\S]*?)</[^>]+>',
    re.I,
)
OG_IMAGE_RE = re.compile(
    r'<meta[^>]+property=["\']og:image["\'][^>]+content=["\']([^"\']+)["\']',
    re.I,
)
STYLESHEET_RE = re.compile(
    r'^[ \t]*<link[^>]+(?:rel=["\']stylesheet["\']|href=["\'][^"\']+\.css[^"\']*["\'])[^>]*>',
    re.I | re.M,
)

FORBIDDEN_KEYS = {
    "offers",
    "price",
    "priceCurrency",
    "availability",
    "seller",
    "review",
    "aggregateRating",
    "manufacturer",
    "gtin",
    "gtin8",
    "gtin12",
    "gtin13",
    "gtin14",
    "hasVariant",
}

def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()

def clean_html_text(value: str | None) -> str | None:
    if value is None:
        return None
    value = re.sub(r"<[^>]+>", " ", value)
    value = re.sub(r"\s+", " ", value).strip()
    return value or None

def one_match(pattern: re.Pattern[str], html: str) -> str | None:
    match = pattern.search(html)
    return match.group(1).strip() if match else None

def discover_pdps() -> list[Path]:
    return sorted(PRODUCTS_ROOT.glob("*/*/index.html"), key=lambda p: rel(p))

def extract_required(html: str) -> dict[str, str | None]:
    return {
        "canonical": one_match(CANONICAL_RE, html),
        "name": clean_html_text(one_match(NAME_RE, html)),
        "model": clean_html_text(one_match(MODEL_RE, html)),
        "description": clean_html_text(one_match(DESC_RE, html)),
        "image": one_match(OG_IMAGE_RE, html),
    }

def iter_jsonld(html: str):
    for match in SCRIPT_RE.finditer(html):
        raw = match.group(1).strip()
        yield match, raw

def product_entities(obj):
    found = []
    if isinstance(obj, dict):
        if obj.get("@type") == "Product":
            found.append(obj)
        graph = obj.get("@graph")
        if isinstance(graph, list):
            found.extend(
                item for item in graph
                if isinstance(item, dict) and item.get("@type") == "Product"
            )
    return found

def get_products(html: str):
    products = []
    blocks = []
    for match, raw in iter_jsonld(html):
        try:
            obj = json.loads(raw)
        except json.JSONDecodeError as exc:
            raise ValueError(f"invalid JSON-LD: {exc}") from exc
        entities = product_entities(obj)
        if entities:
            products.extend(entities)
            blocks.append((match, obj, entities))
    return products, blocks

def expected_product(fields: dict[str, str]) -> dict:
    canonical = fields["canonical"]
    return {
        "@context": "https://schema.org",
        "@type": "Product",
        "@id": f"{canonical}#product",
        "url": canonical,
        "name": fields["name"],
        "description": fields["description"],
        "image": fields["image"],
        "model": fields["model"],
        "brand": {"@id": ORG_ID},
    }

def compliant(product: dict, expected: dict) -> bool:
    if product != expected:
        return False
    serialized = json.dumps(product, ensure_ascii=False)
    return not any(
        re.search(rf'"{re.escape(key)}"\s*:', serialized)
        for key in FORBIDDEN_KEYS
    )

def render_block(product: dict) -> str:
    body = json.dumps(product, ensure_ascii=False, indent=2)
    body = "\n".join("    " + line for line in body.splitlines())
    return f'    <script type="application/ld+json">\n{body}\n    </script>\n\n'

def insert_product(html: str, block: str) -> str:
    anchor = STYLESHEET_RE.search(html)
    if not anchor:
        raise ValueError("stylesheet insertion anchor not found")
    return html[:anchor.start()] + block + html[anchor.start():]

def validate_after(before_fields: dict[str, str], updated: str) -> None:
    after_fields = extract_required(updated)
    if after_fields != before_fields:
        raise ValueError("visible/meta source fields changed after insertion")

    products, _ = get_products(updated)
    if len(products) != 1:
        raise ValueError(f"expected exactly one Product after insertion, got {len(products)}")

    expected = expected_product(before_fields)
    if not compliant(products[0], expected):
        raise ValueError("generated Product does not match approved architecture")

def preflight():
    all_pdps = discover_pdps()
    all_rel = {rel(p) for p in all_pdps}

    missing_frozen = sorted(FROZEN - all_rel)
    if missing_frozen:
        raise ValueError("frozen PDPs missing from repository: " + ", ".join(missing_frozen))

    targets = [p for p in all_pdps if rel(p) not in FROZEN]
    if len(all_pdps) != 127:
        raise ValueError(f"expected 127 total PDPs, got {len(all_pdps)}")
    if len(targets) != EXPECTED_PENDING:
        raise ValueError(f"expected {EXPECTED_PENDING} target PDPs, got {len(targets)}")

    errors = []
    pending = []
    compliant_count = 0
    category_counts = {}

    for path in targets:
        path_rel = rel(path)
        category = path_rel.split("/")[1]
        category_counts[category] = category_counts.get(category, 0) + 1

        html = path.read_text(encoding="utf-8")
        fields = extract_required(html)
        missing = [key for key, value in fields.items() if not value]
        if missing:
            errors.append(f"{path_rel}: missing {','.join(missing)}")
            continue

        products, _ = get_products(html)
        expected = expected_product(fields)

        if len(products) == 0:
            updated = insert_product(html, render_block(expected))
            try:
                validate_after(fields, updated)
            except ValueError as exc:
                errors.append(f"{path_rel}: {exc}")
                continue
            pending.append((path, html, updated))
        elif len(products) == 1 and compliant(products[0], expected):
            compliant_count += 1
        else:
            errors.append(
                f"{path_rel}: unexpected Product state "
                f"(count={len(products)}, compliant={len(products) == 1 and compliant(products[0], expected)})"
            )

    return {
        "all_pdps": all_pdps,
        "targets": targets,
        "pending": pending,
        "compliant": compliant_count,
        "errors": errors,
        "category_counts": dict(sorted(category_counts.items())),
    }

def print_summary(result, mode: str) -> None:
    print(f"MODE={mode}")
    print(f"TOTAL_PDP={len(result['all_pdps'])}")
    print(f"FROZEN_GROUPED={len(GROUPED_FROZEN)}")
    print(f"FROZEN_PILOT={len(PILOT_FROZEN)}")
    print(f"TARGET_PDP={len(result['targets'])}")
    print(f"PENDING_WRITES={len(result['pending'])}")
    print(f"ALREADY_COMPLIANT={result['compliant']}")
    print(f"ERRORS={len(result['errors'])}")
    print("CATEGORY_COUNTS=" + json.dumps(result["category_counts"], ensure_ascii=False, sort_keys=True))
    if result["errors"]:
        for error in result["errors"]:
            print("ERROR=" + error)

def main() -> int:
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--check", action="store_true")
    group.add_argument("--apply", action="store_true")
    args = parser.parse_args()

    try:
        result = preflight()
    except (OSError, ValueError) as exc:
        print(f"FATAL={exc}")
        return 1

    print_summary(result, "apply" if args.apply else "check")

    if result["errors"]:
        return 1

    if args.check:
        return 0

    # Atomic principle: no writes occur before the complete preflight succeeds.
    for path, _before, updated in result["pending"]:
        path.write_text(updated, encoding="utf-8", newline="")

    print(f"WRITTEN={len(result['pending'])}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
