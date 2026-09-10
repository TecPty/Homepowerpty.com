#!/usr/bin/env python3
"""
HP-SEO-AI-001D — deterministic grouped-product architecture migration.

Modes:
  --check  Full preflight only. Never writes files.
  --apply  Runs the same full preflight first, then writes only approved files.

The migration intentionally keeps existing individual PDPs authoritative.
ProductGroup membership is resolved from the current individual Product JSON-LD
and size values are resolved only from each grouped page's existing VARIANTS data.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PRODUCTS_ROOT = ROOT / "productos"
ORG_ID = "https://www.homepowerpty.com/#organization"
SIZE_TERM = "https://schema.org/size"
EXPECTED_TOTAL_PDP = 127
EXPECTED_INDIVIDUAL_PDP = 117
EXPECTED_GROUPS = 9
EXPECTED_VARIANTS = 46

GROUPS = {
    "productos/arroceras/arrocera-ht/index.html": ("capacity", 4),
    "productos/arroceras/arrocera-vaporera-hta/index.html": ("capacity", 3),
    "productos/calderos/caldero-aluminio/index.html": ("diameter", 5),
    "productos/calderos/caldero-vidrio/index.html": ("diameter", 5),
    "productos/extensiones/cable-extension/index.html": ("length", 5),
    "productos/extensiones/extension-naranja/index.html": ("length", 7),
    "productos/extensiones/extension-amarilla/index.html": ("length", 7),
    "productos/ollas/olla-presion-aluminio/index.html": ("capacity", 5),
    "productos/ollas/olla-presion-ck02/index.html": ("capacity", 5),
}

DUPLICATE = "productos/regletas/regleta-variantes/index.html"
GROUPED_ALL = set(GROUPS) | {DUPLICATE}
DUPLICATE_CANONICAL = "https://www.homepowerpty.com/productos/extensiones/extension-amarilla/"
DUPLICATE_SITEMAP_URL = "https://www.homepowerpty.com/productos/regletas/regleta-variantes/"
CATALOG_PATH = "scripts/modules/catalog.js"
SITEMAP_PATH = "sitemap.xml"
HTACCESS_PATH = ".htaccess"
REDIRECT_RULE = (
    "RewriteRule ^productos/regletas/regleta-variantes/?$ "
    "https://www.homepowerpty.com/productos/extensiones/extension-amarilla/ [R=301,L,NE]"
)

SCRIPT_RE = re.compile(
    r'<script[^>]+type=["\']application/ld\+json["\'][^>]*>([\s\S]*?)</script>',
    re.I,
)
CANONICAL_RE = re.compile(
    r'<link[^>]+rel=["\']canonical["\'][^>]+href=["\']([^"\']+)["\']',
    re.I,
)
ROBOTS_RE = re.compile(
    r'(<meta[^>]+name=["\']robots["\'][^>]+content=["\'])([^"\']+)(["\'][^>]*>)',
    re.I,
)
DESCRIPTION_RE = re.compile(
    r'<meta[^>]+name=["\']description["\'][^>]+content=["\']([^"\']+)["\']',
    re.I,
)
TITLE_RE = re.compile(r'<title>([\s\S]*?)</title>', re.I)
STYLESHEET_RE = re.compile(
    r'^[ \t]*<link[^>]+(?:rel=["\']stylesheet["\']|href=["\'][^"\']+\.css[^"\']*["\'])[^>]*>',
    re.I | re.M,
)
VARIANTS_START_RE = re.compile(r"\bconst\s+VARIANTS\s*=\s*\{", re.M)
STRING_FIELD_TEMPLATE = r"\b{field}\s*:\s*'([^']*)'"

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
    "sku",
    "productGroupID",
    "inProductGroupWithID",
}


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def read_text(path: Path) -> str:
    return path.read_bytes().decode("utf-8")


def write_text(path: Path, content: str) -> None:
    path.write_bytes(content.encode("utf-8"))


def newline_for(text: str) -> str:
    return "\r\n" if "\r\n" in text else "\n"


def clean_text(value: str | None) -> str | None:
    if value is None:
        return None
    value = re.sub(r"<[^>]+>", " ", value)
    value = re.sub(r"\s+", " ", value).strip()
    return value or None


def one_match(pattern: re.Pattern[str], text: str) -> str | None:
    match = pattern.search(text)
    return match.group(1).strip() if match else None


def jsonld_objects(html: str) -> list[dict]:
    objects = []
    for match in SCRIPT_RE.finditer(html):
        raw = match.group(1).strip()
        try:
            obj = json.loads(raw)
        except json.JSONDecodeError as exc:
            raise ValueError(f"invalid JSON-LD: {exc}") from exc
        if isinstance(obj, dict):
            objects.append(obj)
    return objects


def typed_entities(html: str, entity_type: str) -> list[dict]:
    found: list[dict] = []
    for obj in jsonld_objects(html):
        if obj.get("@type") == entity_type:
            found.append(obj)
        graph = obj.get("@graph")
        if isinstance(graph, list):
            found.extend(
                item for item in graph
                if isinstance(item, dict) and item.get("@type") == entity_type
            )
    return found


def matching_brace_end(text: str, open_index: int) -> int:
    depth = 0
    quote: str | None = None
    escaped = False
    for index in range(open_index, len(text)):
        ch = text[index]
        if quote is not None:
            if escaped:
                escaped = False
            elif ch == "\\":
                escaped = True
            elif ch == quote:
                quote = None
            continue
        if ch in ("'", '"', "`"):
            quote = ch
            continue
        if ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0:
                return index
    raise ValueError("unbalanced VARIANTS object")


def extract_variants_object(html: str) -> str:
    start = VARIANTS_START_RE.search(html)
    if not start:
        raise ValueError("const VARIANTS object not found")
    open_index = html.find("{", start.start())
    end_index = matching_brace_end(html, open_index)
    return html[open_index + 1:end_index]


def split_variant_entries(body: str) -> list[tuple[str, str]]:
    entries: list[tuple[str, str]] = []
    pos = 0
    key_re = re.compile(r"'([^']+)'\s*:\s*\{")
    while True:
        match = key_re.search(body, pos)
        if not match:
            break
        code = match.group(1)
        open_index = body.find("{", match.start())
        end_index = matching_brace_end(body, open_index)
        entries.append((code, body[open_index + 1:end_index]))
        pos = end_index + 1
    return entries


def extract_string_field(body: str, field: str) -> str | None:
    pattern = re.compile(STRING_FIELD_TEMPLATE.format(field=re.escape(field)))
    match = pattern.search(body)
    return match.group(1).strip() if match else None


def parse_group_variants(html: str, size_field: str) -> list[dict[str, str]]:
    body = extract_variants_object(html)
    variants = []
    for entry_key, entry_body in split_variant_entries(body):
        code = extract_string_field(entry_body, "code")
        size = extract_string_field(entry_body, size_field)
        if not code or code != entry_key:
            raise ValueError(f"variant key/code mismatch for {entry_key}")
        if not size:
            raise ValueError(f"{entry_key}: missing {size_field}")
        variants.append({"model": code, "size": size})
    return variants


def individual_product_index() -> tuple[dict[str, dict], list[str]]:
    errors: list[str] = []
    index: dict[str, dict] = {}
    all_pdps = sorted(PRODUCTS_ROOT.glob("*/*/index.html"), key=rel)
    if len(all_pdps) != EXPECTED_TOTAL_PDP:
        errors.append(f"expected {EXPECTED_TOTAL_PDP} total PDPs, got {len(all_pdps)}")

    individual = [path for path in all_pdps if rel(path) not in GROUPED_ALL]
    if len(individual) != EXPECTED_INDIVIDUAL_PDP:
        errors.append(
            f"expected {EXPECTED_INDIVIDUAL_PDP} individual PDPs, got {len(individual)}"
        )

    for path in individual:
        html = read_text(path)
        products = typed_entities(html, "Product")
        if len(products) != 1:
            errors.append(f"{rel(path)}: expected exactly one Product, got {len(products)}")
            continue
        product = products[0]
        canonical = one_match(CANONICAL_RE, html)
        model = product.get("model")
        if not canonical or not isinstance(model, str) or not model.strip():
            errors.append(f"{rel(path)}: missing canonical/model")
            continue
        model = model.strip()
        expected_id = f"{canonical}#product"
        if product.get("url") != canonical or product.get("@id") != expected_id:
            errors.append(f"{rel(path)}: Product identity does not match canonical")
            continue
        for required in ("name", "image"):
            if not isinstance(product.get(required), str) or not product[required].strip():
                errors.append(f"{rel(path)}: Product missing {required}")
        if model in index:
            errors.append(f"duplicate individual Product model: {model}")
            continue
        index[model] = {
            "path": rel(path),
            "canonical": canonical,
            "product": product,
        }
    return index, errors


def group_name(html: str) -> str | None:
    title = clean_text(one_match(TITLE_RE, html))
    if not title:
        return None
    return re.sub(r"\s+—\s+HomePower PTY\s*$", "", title).strip() or None


def expected_product_group(
    canonical: str,
    name: str,
    description: str,
    variants: list[dict[str, str]],
    product_index: dict[str, dict],
) -> dict:
    nested = []
    for variant in variants:
        model = variant["model"]
        source = product_index[model]["product"]
        nested.append({
            "@type": "Product",
            "@id": source["@id"],
            "url": source["url"],
            "name": source["name"],
            "image": source["image"],
            "model": source["model"],
            "size": variant["size"],
        })
    return {
        "@context": "https://schema.org",
        "@type": "ProductGroup",
        "@id": f"{canonical}#product-group",
        "url": canonical,
        "name": name,
        "description": description,
        "brand": {"@id": ORG_ID},
        "variesBy": SIZE_TERM,
        "hasVariant": nested,
    }


def forbidden_keys(obj) -> set[str]:
    found: set[str] = set()
    if isinstance(obj, dict):
        for key, value in obj.items():
            if key in FORBIDDEN_KEYS:
                found.add(key)
            found |= forbidden_keys(value)
    elif isinstance(obj, list):
        for value in obj:
            found |= forbidden_keys(value)
    return found


def render_jsonld(entity: dict, nl: str) -> str:
    body = json.dumps(entity, ensure_ascii=False, indent=2)
    body = body.replace("\n", nl)
    body = nl.join("    " + line for line in body.split(nl))
    return f'    <script type="application/ld+json">{nl}{body}{nl}    </script>{nl}{nl}'


def insert_group(html: str, entity: dict) -> str:
    anchor = STYLESHEET_RE.search(html)
    if not anchor:
        raise ValueError("stylesheet insertion anchor not found")
    block = render_jsonld(entity, newline_for(html))
    return html[:anchor.start()] + block + html[anchor.start():]


def normalize_duplicate(html: str) -> str:
    canonical_match = CANONICAL_RE.search(html)
    if not canonical_match:
        raise ValueError("duplicate endpoint canonical not found")
    html = html[:canonical_match.start(1)] + DUPLICATE_CANONICAL + html[canonical_match.end(1):]

    robots_match = ROBOTS_RE.search(html)
    if not robots_match:
        raise ValueError("duplicate endpoint robots meta not found")
    html = (
        html[:robots_match.start(2)]
        + "noindex, follow"
        + html[robots_match.end(2):]
    )
    return html


def normalize_catalog(text: str) -> str:
    old_href = "          href: `${templateBase}?mod=${encodeURIComponent(model)}`,"
    new_href = (
        "          href: item.querySelector('.product_image_wrapper')?.getAttribute('href') "
        "|| nameEl?.getAttribute('href') || '',"
    )
    if old_href in text:
        text = text.replace(old_href, new_href, 1)
    elif new_href not in text:
        raise ValueError("catalog variant href anchor not found")

    old_image = '        <a href="${primary.href}" class="product_image_wrapper">'
    new_image = '        <a href="${templateBase}" class="product_image_wrapper">'
    if old_image in text:
        text = text.replace(old_image, new_image, 1)
    elif new_image not in text:
        raise ValueError("catalog grouped image href anchor not found")

    old_title = '<h3 class="product_name"><a href="${primary.href}">${groupTitle}</a></h3>'
    new_title = '<h3 class="product_name"><a href="${templateBase}">${groupTitle}</a></h3>'
    if old_title in text:
        text = text.replace(old_title, new_title, 1)
    elif new_title not in text:
        raise ValueError("catalog grouped title href anchor not found")

    if "`${templateBase}?mod=${encodeURIComponent(model)}`" in text:
        raise ValueError("catalog still generates grouped ?mod= primary links")
    return text


def normalize_sitemap(text: str) -> str:
    nl = newline_for(text)
    block = (
        f"  <url>{nl}"
        f"    <loc>{DUPLICATE_SITEMAP_URL}</loc>{nl}"
        f"  </url>{nl}"
    )
    matches = text.count(block)
    if matches == 1:
        return text.replace(block, "", 1)
    if matches == 0 and DUPLICATE_SITEMAP_URL not in text:
        return text
    raise ValueError(f"expected one duplicate sitemap entry, got {matches}")


def normalize_htaccess(text: str) -> str:
    if REDIRECT_RULE in text:
        return text
    nl = newline_for(text)
    anchor = "RewriteEngine On"
    pos = text.find(anchor)
    if pos < 0:
        raise ValueError("RewriteEngine On anchor not found")
    end = pos + len(anchor)
    block = (
        f"{nl}{nl}# HP-SEO-AI-001D — normalize duplicate grouped endpoint{nl}"
        f"{REDIRECT_RULE}"
    )
    return text[:end] + block + text[end:]


def validate_group_after(html: str, expected: dict) -> None:
    groups = typed_entities(html, "ProductGroup")
    if len(groups) != 1 or groups[0] != expected:
        raise ValueError("generated ProductGroup does not match expected entity")
    forbidden = forbidden_keys(groups[0])
    if forbidden:
        raise ValueError("forbidden keys in ProductGroup: " + ", ".join(sorted(forbidden)))


def preflight() -> dict:
    errors: list[str] = []
    pending: dict[Path, str] = {}
    family_matrix: dict[str, list[str]] = {}

    product_index, product_errors = individual_product_index()
    errors.extend(product_errors)

    membership: dict[str, str] = {}
    total_variants = 0

    for path_rel, (size_field, expected_count) in GROUPS.items():
        path = ROOT / path_rel
        if not path.exists():
            errors.append(f"missing group: {path_rel}")
            continue
        html = read_text(path)
        canonical = one_match(CANONICAL_RE, html)
        name = group_name(html)
        description = one_match(DESCRIPTION_RE, html)
        robots = ROBOTS_RE.search(html)
        robots_value = robots.group(2).strip().lower() if robots else None
        if not canonical or not name or not description:
            errors.append(f"{path_rel}: missing canonical/name/description")
            continue
        if robots_value != "index, follow":
            errors.append(f"{path_rel}: expected robots index, follow")
            continue

        try:
            variants = parse_group_variants(html, size_field)
        except ValueError as exc:
            errors.append(f"{path_rel}: {exc}")
            continue

        if len(variants) != expected_count:
            errors.append(
                f"{path_rel}: expected {expected_count} variants, got {len(variants)}"
            )
            continue

        codes = [item["model"] for item in variants]
        family_matrix[path_rel] = codes
        total_variants += len(codes)

        for code in codes:
            if code in membership:
                errors.append(
                    f"variant {code} appears in both {membership[code]} and {path_rel}"
                )
            membership[code] = path_rel
            if code not in product_index:
                errors.append(f"{path_rel}: no individual Product identity for {code}")

        if any(code not in product_index for code in codes):
            continue

        expected = expected_product_group(
            canonical, name, description, variants, product_index
        )
        existing = typed_entities(html, "ProductGroup")
        if len(existing) == 0:
            updated = insert_group(html, expected)
            try:
                validate_group_after(updated, expected)
            except ValueError as exc:
                errors.append(f"{path_rel}: {exc}")
                continue
            pending[path] = updated
        elif len(existing) == 1 and existing[0] == expected and not forbidden_keys(existing[0]):
            pass
        else:
            errors.append(f"{path_rel}: unexpected existing ProductGroup state")

    if len(GROUPS) != EXPECTED_GROUPS:
        errors.append(f"configured group count is not {EXPECTED_GROUPS}")
    if total_variants != EXPECTED_VARIANTS:
        errors.append(f"expected {EXPECTED_VARIANTS} grouped variants, got {total_variants}")
    if len(membership) != EXPECTED_VARIANTS:
        errors.append(f"expected {EXPECTED_VARIANTS} unique memberships, got {len(membership)}")

    duplicate_path = ROOT / DUPLICATE
    if not duplicate_path.exists():
        errors.append(f"missing duplicate endpoint: {DUPLICATE}")
    else:
        duplicate_html = read_text(duplicate_path)
        normalized = normalize_duplicate(duplicate_html)
        if normalized != duplicate_html:
            pending[duplicate_path] = normalized

    catalog_path = ROOT / CATALOG_PATH
    sitemap_path = ROOT / SITEMAP_PATH
    htaccess_path = ROOT / HTACCESS_PATH
    for required in (catalog_path, sitemap_path, htaccess_path):
        if not required.exists():
            errors.append(f"missing required file: {rel(required)}")

    if not errors:
        catalog = read_text(catalog_path)
        sitemap = read_text(sitemap_path)
        htaccess = read_text(htaccess_path)
        try:
            catalog_updated = normalize_catalog(catalog)
            sitemap_updated = normalize_sitemap(sitemap)
            htaccess_updated = normalize_htaccess(htaccess)
        except ValueError as exc:
            errors.append(str(exc))
        else:
            if catalog_updated != catalog:
                pending[catalog_path] = catalog_updated
            if sitemap_updated != sitemap:
                pending[sitemap_path] = sitemap_updated
            if htaccess_updated != htaccess:
                pending[htaccess_path] = htaccess_updated

    return {
        "errors": errors,
        "pending": pending,
        "family_matrix": dict(sorted(family_matrix.items())),
        "group_count": len(family_matrix),
        "variant_count": total_variants,
        "unique_variant_count": len(membership),
        "individual_index_count": len(product_index),
    }


def print_summary(result: dict, mode: str) -> None:
    print(f"MODE={mode}")
    print(f"GROUPS={result['group_count']}")
    print(f"GROUPED_VARIANTS={result['variant_count']}")
    print(f"UNIQUE_GROUPED_VARIANTS={result['unique_variant_count']}")
    print(f"INDIVIDUAL_PRODUCT_INDEX={result['individual_index_count']}")
    print(f"DUPLICATE_ENDPOINTS=1")
    print(f"PENDING_WRITES={len(result['pending'])}")
    print(f"ERRORS={len(result['errors'])}")
    print("FAMILY_MATRIX=" + json.dumps(result["family_matrix"], ensure_ascii=False, sort_keys=True))
    if result["errors"]:
        for error in result["errors"]:
            print("ERROR=" + error)
    if result["pending"]:
        for path in sorted(result["pending"], key=rel):
            print("PENDING=" + rel(path))


def main() -> int:
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--check", action="store_true")
    group.add_argument("--apply", action="store_true")
    args = parser.parse_args()

    try:
        result = preflight()
    except (OSError, UnicodeError, ValueError) as exc:
        print(f"FATAL={exc}")
        return 1

    print_summary(result, "apply" if args.apply else "check")
    if result["errors"]:
        return 1
    if args.check:
        return 0

    # Atomic principle: no target write occurs until the complete preflight succeeds.
    for path in sorted(result["pending"], key=rel):
        write_text(path, result["pending"][path])

    print(f"WRITTEN={len(result['pending'])}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
