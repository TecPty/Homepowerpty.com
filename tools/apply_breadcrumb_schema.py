#!/usr/bin/env python3
"""
HP-SEO-AI-001E — deterministic BreadcrumbList migration.

Modes:
  --check  Full preflight only. Never writes files.
  --apply  Runs the same full preflight first, then writes only approved PDP files.

Approved semantic path:
  Catálogo -> current page

The current-page name is resolved exclusively from the canonical Product or
ProductGroup entity already present in each indexable PDP.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PRODUCTS_ROOT = ROOT / "productos"

EXPECTED_TOTAL_PDP = 127
EXPECTED_INDEXABLE_PDP = 126
EXPECTED_NOINDEX_PDP = 1
EXPECTED_PRODUCT_PDP = 117
EXPECTED_PRODUCTGROUP_PDP = 9
EXPECTED_TARGET_BREADCRUMBS = 126
EXPECTED_EXCLUDED_BREADCRUMBS = 1

EXCLUDED_PATH = "productos/regletas/regleta-variantes/index.html"
CATALOG_URL = "https://www.homepowerpty.com/#catalogo"

SCRIPT_RE = re.compile(
    r'<script[^>]+type=["\']application/ld\+json["\'][^>]*>([\s\S]*?)</script>',
    re.I,
)
CANONICAL_RE = re.compile(
    r'<link[^>]+rel=["\']canonical["\'][^>]+href=["\']([^"\']+)["\']',
    re.I,
)
ROBOTS_RE = re.compile(
    r'<meta[^>]+name=["\']robots["\'][^>]+content=["\']([^"\']+)["\']',
    re.I,
)
STYLESHEET_RE = re.compile(
    r'^[ \t]*<link[^>]+(?:rel=["\']stylesheet["\']|href=["\'][^"\']+\.css[^"\']*["\'])[^>]*>',
    re.I | re.M,
)


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def read_text(path: Path) -> str:
    return path.read_bytes().decode("utf-8")


def write_text(path: Path, content: str) -> None:
    path.write_bytes(content.encode("utf-8"))


def newline_for(text: str) -> str:
    return "\r\n" if "\r\n" in text else "\n"


def one_match(pattern: re.Pattern[str], text: str) -> str | None:
    match = pattern.search(text)
    return match.group(1).strip() if match else None


def jsonld_objects(html: str) -> list[dict]:
    objects: list[dict] = []

    for match in SCRIPT_RE.finditer(html):
        raw = match.group(1).strip()

        try:
            obj = json.loads(raw)
        except json.JSONDecodeError as exc:
            raise ValueError(f"invalid JSON-LD: {exc}") from exc

        if isinstance(obj, dict):
            objects.append(obj)
        elif isinstance(obj, list):
            objects.extend(
                item for item in obj
                if isinstance(item, dict)
            )

    return objects


def typed_entities(html: str, entity_type: str) -> list[dict]:
    found: list[dict] = []

    for obj in jsonld_objects(html):
        if obj.get("@type") == entity_type:
            found.append(obj)

        graph = obj.get("@graph")

        if isinstance(graph, list):
            found.extend(
                item
                for item in graph
                if isinstance(item, dict)
                and item.get("@type") == entity_type
            )

    return found


def robots_value(html: str) -> str:
    value = one_match(ROBOTS_RE, html)
    return value.lower() if value else ""


def is_noindex(html: str) -> bool:
    tokens = {
        token.strip().lower()
        for token in robots_value(html).split(",")
        if token.strip()
    }

    return "noindex" in tokens


def expected_breadcrumb(canonical: str, name: str) -> dict:
    return {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "@id": f"{canonical}#breadcrumb",
        "itemListElement": [
            {
                "@type": "ListItem",
                "position": 1,
                "name": "Catálogo",
                "item": CATALOG_URL,
            },
            {
                "@type": "ListItem",
                "position": 2,
                "name": name,
            },
        ],
    }


def render_jsonld(entity: dict, nl: str) -> str:
    body = json.dumps(
        entity,
        ensure_ascii=False,
        indent=2,
    )

    body = body.replace("\n", nl)
    body = nl.join(
        "    " + line
        for line in body.split(nl)
    )

    return (
        f'    <script type="application/ld+json">{nl}'
        f'{body}{nl}'
        f'    </script>{nl}{nl}'
    )


def insert_breadcrumb(html: str, entity: dict) -> str:
    anchor = STYLESHEET_RE.search(html)

    if not anchor:
        raise ValueError(
            "stylesheet insertion anchor not found"
        )

    block = render_jsonld(
        entity,
        newline_for(html),
    )

    return (
        html[:anchor.start()]
        + block
        + html[anchor.start():]
    )


def entity_for_canonical(
    html: str,
    canonical: str,
) -> tuple[str, dict]:
    products = typed_entities(
        html,
        "Product",
    )

    groups = typed_entities(
        html,
        "ProductGroup",
    )

    matching_products = [
        entity
        for entity in products
        if entity.get("url") == canonical
        and entity.get("@id")
        == f"{canonical}#product"
    ]

    matching_groups = [
        entity
        for entity in groups
        if entity.get("url") == canonical
        and entity.get("@id")
        == f"{canonical}#product-group"
    ]

    matches: list[tuple[str, dict]] = [
        ("Product", entity)
        for entity in matching_products
    ] + [
        ("ProductGroup", entity)
        for entity in matching_groups
    ]

    if len(matches) != 1:
        raise ValueError(
            "expected exactly one canonical "
            "Product/ProductGroup identity, "
            f"got {len(matches)}"
        )

    entity_type, entity = matches[0]

    name = entity.get("name")

    if (
        not isinstance(name, str)
        or not name.strip()
    ):
        raise ValueError(
            f"{entity_type} missing non-empty name"
        )

    return entity_type, entity


def validate_expected_breadcrumb(
    entity: dict,
    expected: dict,
) -> None:
    if entity != expected:
        raise ValueError(
            "BreadcrumbList does not match "
            "deterministic expected entity"
        )

    items = entity.get("itemListElement")

    if (
        not isinstance(items, list)
        or len(items) != 2
    ):
        raise ValueError(
            "BreadcrumbList must contain "
            "exactly two ListItem nodes"
        )

    first, second = items

    if first != {
        "@type": "ListItem",
        "position": 1,
        "name": "Catálogo",
        "item": CATALOG_URL,
    }:
        raise ValueError(
            "BreadcrumbList position 1 is invalid"
        )

    if (
        second.get("@type") != "ListItem"
        or second.get("position") != 2
    ):
        raise ValueError(
            "BreadcrumbList position 2 is invalid"
        )

    if set(second) != {
        "@type",
        "position",
        "name",
    }:
        raise ValueError(
            "BreadcrumbList position 2 "
            "must omit item"
        )


def preflight() -> dict:
    errors: list[str] = []
    pending: dict[Path, str] = {}

    pdps = sorted(
        PRODUCTS_ROOT.glob("*/*/index.html"),
        key=rel,
    )

    indexable_count = 0
    noindex_count = 0
    product_count = 0
    product_group_count = 0
    excluded_count = 0
    target_count = 0

    if len(pdps) != EXPECTED_TOTAL_PDP:
        errors.append(
            f"expected {EXPECTED_TOTAL_PDP} "
            f"total PDPs, got {len(pdps)}"
        )

    all_paths = {
        rel(path)
        for path in pdps
    }

    if EXCLUDED_PATH not in all_paths:
        errors.append(
            f"missing excluded endpoint: "
            f"{EXCLUDED_PATH}"
        )

    for path in pdps:
        path_rel = rel(path)

        try:
            html = read_text(path)

            canonical = one_match(
                CANONICAL_RE,
                html,
            )

            if not canonical:
                raise ValueError(
                    "missing canonical"
                )

            breadcrumbs = typed_entities(
                html,
                "BreadcrumbList",
            )

            if is_noindex(html):
                noindex_count += 1

                if path_rel != EXCLUDED_PATH:
                    errors.append(
                        f"{path_rel}: unexpected "
                        "noindex PDP; only "
                        f"{EXCLUDED_PATH} is allowed"
                    )

                if breadcrumbs:
                    errors.append(
                        f"{path_rel}: excluded "
                        "noindex PDP must have zero "
                        "BreadcrumbList"
                    )

                if path_rel == EXCLUDED_PATH:
                    excluded_count += 1

                continue

            indexable_count += 1
            target_count += 1

            if path_rel == EXCLUDED_PATH:
                errors.append(
                    f"{path_rel}: approved excluded "
                    "endpoint unexpectedly indexable"
                )

            entity_type, entity = (
                entity_for_canonical(
                    html,
                    canonical,
                )
            )

            if entity_type == "Product":
                product_count += 1
            elif entity_type == "ProductGroup":
                product_group_count += 1

            name = entity["name"].strip()

            expected = expected_breadcrumb(
                canonical,
                name,
            )

            if len(breadcrumbs) == 0:
                updated = insert_breadcrumb(
                    html,
                    expected,
                )

                generated = typed_entities(
                    updated,
                    "BreadcrumbList",
                )

                if len(generated) != 1:
                    raise ValueError(
                        "generated BreadcrumbList "
                        f"count is {len(generated)}, "
                        "expected 1"
                    )

                validate_expected_breadcrumb(
                    generated[0],
                    expected,
                )

                after_type, after_entity = (
                    entity_for_canonical(
                        updated,
                        canonical,
                    )
                )

                if (
                    after_type != entity_type
                    or after_entity != entity
                ):
                    raise ValueError(
                        f"{entity_type} changed "
                        "during BreadcrumbList insertion"
                    )

                pending[path] = updated

            elif len(breadcrumbs) == 1:
                validate_expected_breadcrumb(
                    breadcrumbs[0],
                    expected,
                )

            else:
                raise ValueError(
                    "expected zero or one "
                    "BreadcrumbList, "
                    f"got {len(breadcrumbs)}"
                )

        except (
            OSError,
            UnicodeError,
            ValueError,
        ) as exc:
            errors.append(
                f"{path_rel}: {exc}"
            )

    if (
        indexable_count
        != EXPECTED_INDEXABLE_PDP
    ):
        errors.append(
            f"expected "
            f"{EXPECTED_INDEXABLE_PDP} "
            "indexable PDPs, got "
            f"{indexable_count}"
        )

    if (
        noindex_count
        != EXPECTED_NOINDEX_PDP
    ):
        errors.append(
            f"expected "
            f"{EXPECTED_NOINDEX_PDP} "
            "noindex PDP, got "
            f"{noindex_count}"
        )

    if product_count != EXPECTED_PRODUCT_PDP:
        errors.append(
            f"expected {EXPECTED_PRODUCT_PDP} "
            f"Product PDPs, got {product_count}"
        )

    if (
        product_group_count
        != EXPECTED_PRODUCTGROUP_PDP
    ):
        errors.append(
            f"expected "
            f"{EXPECTED_PRODUCTGROUP_PDP} "
            "ProductGroup PDPs, got "
            f"{product_group_count}"
        )

    if (
        target_count
        != EXPECTED_TARGET_BREADCRUMBS
    ):
        errors.append(
            f"expected "
            f"{EXPECTED_TARGET_BREADCRUMBS} "
            "target BreadcrumbLists, got "
            f"{target_count}"
        )

    if (
        excluded_count
        != EXPECTED_EXCLUDED_BREADCRUMBS
    ):
        errors.append(
            f"expected "
            f"{EXPECTED_EXCLUDED_BREADCRUMBS} "
            "excluded BreadcrumbList PDP, got "
            f"{excluded_count}"
        )

    return {
        "errors": errors,
        "pending": pending,
        "total_pdp": len(pdps),
        "indexable_pdp": indexable_count,
        "noindex_pdp": noindex_count,
        "product_pdp": product_count,
        "productgroup_pdp": product_group_count,
        "target_breadcrumbs": target_count,
        "excluded_breadcrumbs": excluded_count,
    }


def print_summary(
    result: dict,
    mode: str,
) -> None:
    print(f"MODE={mode}")
    print(
        f"PDP_TOTAL="
        f"{result['total_pdp']}"
    )
    print(
        f"INDEXABLE_PDP="
        f"{result['indexable_pdp']}"
    )
    print(
        f"NOINDEX_PDP="
        f"{result['noindex_pdp']}"
    )
    print(
        f"PRODUCT_PDP="
        f"{result['product_pdp']}"
    )
    print(
        f"PRODUCTGROUP_PDP="
        f"{result['productgroup_pdp']}"
    )
    print(
        f"TARGET_BREADCRUMBS="
        f"{result['target_breadcrumbs']}"
    )
    print(
        f"EXCLUDED_BREADCRUMBS="
        f"{result['excluded_breadcrumbs']}"
    )
    print(
        f"PENDING_WRITES="
        f"{len(result['pending'])}"
    )
    print(
        f"ERRORS="
        f"{len(result['errors'])}"
    )

    if result["errors"]:
        for error in result["errors"]:
            print("ERROR=" + error)

    if result["pending"]:
        for path in sorted(
            result["pending"],
            key=rel,
        ):
            print(
                "PENDING=" + rel(path)
            )


def main() -> int:
    parser = argparse.ArgumentParser()

    group = (
        parser.add_mutually_exclusive_group(
            required=True
        )
    )

    group.add_argument(
        "--check",
        action="store_true",
    )

    group.add_argument(
        "--apply",
        action="store_true",
    )

    args = parser.parse_args()

    try:
        result = preflight()
    except (
        OSError,
        UnicodeError,
        ValueError,
    ) as exc:
        print(f"FATAL={exc}")
        return 1

    mode = (
        "apply"
        if args.apply
        else "check"
    )

    print_summary(
        result,
        mode,
    )

    if result["errors"]:
        return 1

    if args.check:
        return 0

    # No target write occurs until the complete
    # preflight succeeds.
    for path in sorted(
        result["pending"],
        key=rel,
    ):
        write_text(
            path,
            result["pending"][path],
        )

    print(
        f"WRITTEN="
        f"{len(result['pending'])}"
    )

    return 0


if __name__ == "__main__":
    sys.exit(main())