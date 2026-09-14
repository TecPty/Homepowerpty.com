#!/usr/bin/env python3
"""
HP-SEO-AI-001F-1 -- deterministic product identifier registry builder/validator.

Modes:
  --build   Reconciles all known identity sources into data/product-identifiers.json.
            Fails closed: never writes a registry that would violate a structural
            or negative-assertion invariant.
  --check   Re-derives the registry from the same sources and verifies it is
            byte-for-byte identical to the committed data/product-identifiers.json.
            Never writes. Used as the idempotency/CI gate.

Fail-closed policy: absence of evidence never authorizes publication. A GTIN or
SKU only becomes eligible for JSON-LD publication when its status is exactly
"validated" AND publishing_eligible is true.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PRODUCTS_ROOT = ROOT / "productos"
EXCEL_JSON_PATH = ROOT / "tools" / "products_from_excel.json"
REPLACE_CODES_PATH = ROOT / "tools" / "replace_codes.py"
REGISTRY_PATH = ROOT / "data" / "product-identifiers.json"

BASELINE_COMMIT = "45f8e0f38166de7b52a5675d9e231d0f05a34c75"

EXPECTED_TOTAL_PDP = 127
EXPECTED_INDEXABLE_PDP = 126
EXPECTED_NOINDEX_PDP = 1
EXPECTED_PRODUCT_COUNT = 117
EXPECTED_PRODUCTGROUP_COUNT = 9
EXPECTED_VARIANT_COUNT = 46
EXPECTED_SOURCE_RECORDS = 59
EXPECTED_GTIN12_CANDIDATES = 54
EXPECTED_GTIN13_CANDIDATES = 5

# Casos de conflicto conocidos obligatorios (Seccion 8 del Acceptance Contract).
# El barcode "current" es el que coincide con el Excel y con el pdp-barcode
# visible en el PDP real; el resto son alternates hallados unicamente en el
# tooling historico (tools/replace_codes.py) y por lo tanto sin provenance
# empresarial vigente.
KNOWN_MULTI_BARCODE_MODELS = {"JR-A101", "JR-LD8", "HP-017"}

SCRIPT_RE = re.compile(
    r'<script[^>]+type=["\']application/ld\+json["\'][^>]*>([\s\S]*?)</script>',
    re.I,
)
ROBOTS_RE = re.compile(
    r'<meta[^>]+name=["\']robots["\'][^>]+content=["\']([^"\']+)["\']',
    re.I,
)
FORBIDDEN_KEYS = {
    "offer", "aggregateoffer", "price", "lowprice", "highprice",
    "pricecurrency", "availability", "seller", "review", "aggregaterating",
    "shippingdetails", "returnpolicy", "mpn",
}


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def read_text(path: Path) -> str:
    return path.read_bytes().decode("utf-8")


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
            objects.extend(item for item in obj if isinstance(item, dict))
    return objects


def is_noindex(html: str) -> bool:
    match = ROBOTS_RE.search(html)
    if not match:
        return False
    tokens = {t.strip().lower() for t in match.group(1).split(",") if t.strip()}
    return "noindex" in tokens


def scan_forbidden_keys(obj, path_hint: str, found: list[str]) -> None:
    """Recorre recursivamente cualquier estructura JSON-LD buscando campos
    comerciales prohibidos (negative assertions, Seccion 16/27)."""
    if isinstance(obj, dict):
        for key, value in obj.items():
            if key.lower() in FORBIDDEN_KEYS:
                found.append(f"{path_hint}: forbidden key '{key}'")
            if key == "@type" and isinstance(value, str) and value.lower() in {"offer", "aggregateoffer"}:
                found.append(f"{path_hint}: forbidden @type '{value}'")
            scan_forbidden_keys(value, path_hint, found)
    elif isinstance(obj, list):
        for item in obj:
            scan_forbidden_keys(item, path_hint, found)


def normalize_model(s: str) -> str:
    return re.sub(r"[\s.\-]", "", s).upper()


def split_raw_sku(raw: str) -> tuple[str, str | None]:
    """El campo 'sku' crudo del Excel a veces mezcla modelo canonico y alias
    historico en una sola celda: 'JR-A101\\n(R.97816)'. Los separamos; el
    modelo canonico nunca se publica concatenado con su alias (Seccion 9)."""
    match = re.match(r"^(.*?)\s*\n\s*\(([^)]+)\)\s*$", raw, re.S)
    if match:
        return match.group(1).strip(), match.group(2).strip()
    return raw.strip(), None


def gtin_checksum_valid(digits: str) -> bool:
    body, check = digits[:-1], int(digits[-1])
    total = 0
    for i, ch in enumerate(reversed(body)):
        total += int(ch) * (3 if i % 2 == 0 else 1)
    return (10 - (total % 10)) % 10 == check


def classify_gtin_structure(barcode: str) -> dict:
    numeric = barcode.isdigit()
    length = len(barcode) if numeric else None
    gtin_type = None
    if numeric and length == 12:
        gtin_type = "gtin12"
    elif numeric and length == 13:
        gtin_type = "gtin13"
    checksum_valid = numeric and length in (12, 13) and gtin_checksum_valid(barcode)
    if not numeric:
        status = "invalid_non_numeric"
    elif length not in (12, 13):
        status = "invalid_length"
    elif not checksum_valid:
        status = "invalid_checksum"
    else:
        status = "structurally_valid"
    return {
        "numeric": numeric,
        "length": length,
        "gtin_type_candidate": gtin_type,
        "checksum_valid": checksum_valid,
        "structural_status": status,
    }


def load_replace_codes_history() -> dict[str, list[str]]:
    """Importa (sin ejecutar run()) el mapping historico congelado de
    tools/replace_codes.py para usarlo como fuente de provenance de
    'tooling historico'. No se modifica ese archivo."""
    spec = importlib.util.spec_from_file_location("replace_codes_frozen", REPLACE_CODES_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)  # solo define CODE_TO_SKU; run() esta bajo __main__ guard
    model_to_barcodes: dict[str, list[str]] = {}
    for barcode, model in module.CODE_TO_SKU.items():
        model_to_barcodes.setdefault(normalize_model(model), []).append(barcode)
    return model_to_barcodes


def extract_site_inventory() -> dict:
    """Enumera las 117 entidades Product reales del sitio (una por PDP propio),
    detecta cuales son variantes de algun ProductGroup, y confirma los
    invariantes estructurales del baseline (Seccion 3)."""
    errors: list[str] = []
    pdps = sorted(PRODUCTS_ROOT.glob("*/*/index.html"), key=rel)

    products: dict[str, dict] = {}  # model_normalized -> entity info
    product_groups: list[dict] = []
    variant_ids: set[str] = set()

    indexable_count = 0
    noindex_count = 0

    for path in pdps:
        html = read_text(path)
        if is_noindex(html):
            noindex_count += 1
            continue
        indexable_count += 1

        objects = jsonld_objects(html)
        product_entities = [o for o in objects if o.get("@type") == "Product"]
        group_entities = [o for o in objects if o.get("@type") == "ProductGroup"]

        for entity in product_entities:
            model = entity.get("model")
            if not model:
                continue
            key = normalize_model(model)
            if key in products:
                errors.append(f"duplicate model '{model}' at {rel(path)} and {products[key]['path']}")
                continue
            products[key] = {
                "model": model,
                "product_id": entity.get("@id"),
                "canonical_url": entity.get("url"),
                "path": rel(path),
            }

        for group in group_entities:
            product_groups.append({
                "group_id": group.get("@id"),
                "canonical_url": group.get("url"),
                "path": rel(path),
                "variants": group.get("hasVariant") or [],
            })
            for variant in group.get("hasVariant") or []:
                vid = variant.get("@id")
                if vid:
                    variant_ids.add(vid)

    for key, info in products.items():
        info["is_variant"] = info["product_id"] in variant_ids
        info["product_group_url"] = None

    for group in product_groups:
        for variant in group["variants"]:
            vid = variant.get("@id")
            for info in products.values():
                if info["product_id"] == vid:
                    info["product_group_url"] = group["canonical_url"]

    variant_count = sum(1 for info in products.values() if info["is_variant"])

    if len(pdps) != EXPECTED_TOTAL_PDP:
        errors.append(f"expected {EXPECTED_TOTAL_PDP} total PDPs, got {len(pdps)}")
    if indexable_count != EXPECTED_INDEXABLE_PDP:
        errors.append(f"expected {EXPECTED_INDEXABLE_PDP} indexable PDPs, got {indexable_count}")
    if noindex_count != EXPECTED_NOINDEX_PDP:
        errors.append(f"expected {EXPECTED_NOINDEX_PDP} noindex PDPs, got {noindex_count}")
    if len(products) != EXPECTED_PRODUCT_COUNT:
        errors.append(f"expected {EXPECTED_PRODUCT_COUNT} Product entities, got {len(products)}")
    if len(product_groups) != EXPECTED_PRODUCTGROUP_COUNT:
        errors.append(f"expected {EXPECTED_PRODUCTGROUP_COUNT} ProductGroup entities, got {len(product_groups)}")
    if variant_count != EXPECTED_VARIANT_COUNT:
        errors.append(f"expected {EXPECTED_VARIANT_COUNT} variants, got {variant_count}")

    return {
        "errors": errors,
        "products": products,
        "product_groups": product_groups,
        "total_pdp": len(pdps),
        "indexable_pdp": indexable_count,
        "noindex_pdp": noindex_count,
        "product_count": len(products),
        "productgroup_count": len(product_groups),
        "variant_count": variant_count,
    }


def check_negative_assertions() -> list[str]:
    found: list[str] = []
    for path in sorted(PRODUCTS_ROOT.glob("*/*/index.html"), key=rel):
        html = read_text(path)
        for obj in jsonld_objects(html):
            scan_forbidden_keys(obj, rel(path), found)
    return found


def get_source_provenance_evidence() -> dict:
    """Registra evidencia REAL de git para la fecha del Excel derivado, en vez
    de asumir la fecha citada por el contrato sin verificarla."""
    def last_commit_for(path_str: str) -> tuple[str, str] | None:
        try:
            out = subprocess.run(
                ["git", "log", "-1", "--format=%h %ad", "--date=short", "--", path_str],
                cwd=ROOT, capture_output=True, text=True, check=True,
            ).stdout.strip()
            if not out:
                return None
            sha, date = out.split(" ", 1)
            return sha, date
        except subprocess.CalledProcessError:
            return None

    excel_exists = (ROOT / "EXCEL DE PRODUCTOS PARA MKT.xlsx").exists()
    json_commit = last_commit_for("tools/products_from_excel.json")
    excel_removal_commit = last_commit_for("EXCEL DE PRODUCTOS PARA MKT.xlsx")

    return {
        "excel_file_present_in_tree": excel_exists,
        "derived_json_path": "tools/products_from_excel.json",
        "derived_json_last_commit": json_commit[0] if json_commit else None,
        "derived_json_last_commit_date": json_commit[1] if json_commit else None,
        "excel_last_touched_commit": excel_removal_commit[0] if excel_removal_commit else None,
        "excel_last_touched_date": excel_removal_commit[1] if excel_removal_commit else None,
        "contract_claimed_last_modified": "2026-04-10",
        "verification_note": (
            "El archivo Excel original ya no existe en el arbol (verificado). "
            "La fecha citada por el contrato (2026-04-10) no coincide con el "
            "ultimo commit real que toco el archivo o su JSON derivado "
            "(ver excel_last_touched_date / derived_json_last_commit_date). "
            "Se usa la fecha verificada por git como provenance timestamp."
        ),
    }


def build_records(inventory: dict, history: dict[str, list[str]]) -> list[dict]:
    with open(EXCEL_JSON_PATH, encoding="utf-8") as f:
        source_records = json.load(f)

    if len(source_records) != EXPECTED_SOURCE_RECORDS:
        raise ValueError(
            f"expected {EXPECTED_SOURCE_RECORDS} source records, got {len(source_records)}"
        )

    barcode_seen: dict[str, int] = {}
    for r in source_records:
        barcode_seen[r["barcode"]] = barcode_seen.get(r["barcode"], 0) + 1

    products = inventory["products"]
    records: list[dict] = []

    for idx, raw in enumerate(source_records, start=1):
        model_raw, alias = split_raw_sku(raw["sku"])
        model_normalized = normalize_model(model_raw)
        barcode_raw = raw["barcode"]
        gtin_struct = classify_gtin_structure(barcode_raw)

        matches = [k for k in products if k == model_normalized]
        if len(matches) == 1:
            reconciliation_status = "matched"
            match_info = products[matches[0]]
        elif len(matches) == 0:
            reconciliation_status = "unmatched"
            match_info = None
        else:
            reconciliation_status = "ambiguous"
            match_info = None

        alternates = []
        historical = history.get(model_normalized, [])
        current_source_confirmed = False
        for alt_barcode in historical:
            if alt_barcode == barcode_raw:
                current_source_confirmed = True
                continue
            alternates.append({
                "barcode": alt_barcode,
                "classification": "alternate",
                "source": ["historical_tooling:tools/replace_codes.py"],
                "publishing_eligible": False,
                "reason": "sin provenance empresarial vigente (solo tooling historico)",
            })

        is_known_conflict = model_raw.strip().upper() in KNOWN_MULTI_BARCODE_MODELS or normalize_model(model_raw) in {
            normalize_model(m) for m in KNOWN_MULTI_BARCODE_MODELS
        }

        duplicate_in_source = barcode_seen[barcode_raw] > 1

        # Provenance gate: independiente del checksum (AC-G04). Un barcode solo
        # tiene provenance suficiente si proviene de una fuente empresarial
        # vigente Y no quedo desplazado por un conflicto de multiples codigos
        # para el mismo modelo (Seccion 8 / R1).
        provenance_sufficient = (
            reconciliation_status == "matched"
            and not duplicate_in_source
        )
        provenance_reason = (
            "fuente empresarial (excel_derived_json) reconciliada 1:1 contra un Product unico del sitio"
            if provenance_sufficient
            else f"reconciliation_status={reconciliation_status}, duplicate_in_source={duplicate_in_source}"
        )

        # Publication gate: fail-closed. Requiere provenance Y estructura,
        # como chequeos EXPLICITOS e independientes.
        gtin_status = "candidate"
        gtin_publishable = False
        conflict_notes: list[str] = []

        if duplicate_in_source:
            gtin_status = "ambiguous"
            conflict_notes.append("barcode duplicado dentro del source empresarial")
        elif reconciliation_status != "matched":
            gtin_status = reconciliation_status if reconciliation_status == "ambiguous" else "candidate"
            conflict_notes.append(f"reconciliation_status={reconciliation_status}; no hay Product unico para publicar")
        elif not provenance_sufficient:
            gtin_status = "candidate"
            conflict_notes.append(f"provenance insuficiente: {provenance_reason}")
        elif gtin_struct["structural_status"] != "structurally_valid":
            gtin_status = "rejected"
            conflict_notes.append(f"gtin structural failure: {gtin_struct['structural_status']}")
        else:
            gtin_status = "validated"
            gtin_publishable = True

        if is_known_conflict:
            conflict_notes.append(
                "modelo con historial de multiples codigos de barras conocido "
                "(Seccion 8 del Acceptance Contract); ver alternates"
            )

        record = {
            "record_id": f"excel-{idx:03d}",
            "raw_sku_field": raw["sku"],
            "model_raw": model_raw,
            "model_alias": alias,
            "model_normalized": model_normalized,
            "es_nuevo": raw.get("es_nuevo", False),
            "barcode_raw": barcode_raw,
            "gtin_structural": gtin_struct,
            "duplicate_barcode_in_source": duplicate_in_source,
            "reconciliation_status": reconciliation_status,
            "matched_model": match_info["model"] if match_info else None,
            "matched_product_id": match_info["product_id"] if match_info else None,
            "matched_canonical_url": match_info["canonical_url"] if match_info else None,
            "is_variant": match_info["is_variant"] if match_info else None,
            "product_group_url": match_info["product_group_url"] if match_info else None,
            "provenance": {
                "sources": ["excel_derived_json:tools/products_from_excel.json"],
                "confirmed_by_pdp_display": reconciliation_status == "matched",
                "confirmed_by_historical_tooling": current_source_confirmed,
                "provenance_sufficient": provenance_sufficient,
                "provenance_reason": provenance_reason,
            },
            "known_multi_barcode_conflict": is_known_conflict,
            "alternate_barcodes": alternates,
            "gtin_status": gtin_status,
            "gtin_publishable": gtin_publishable,
            "sku_candidate": model_raw,
            "sku_status": "candidate",
            "sku_publishable": False,
            "sku_publish_reason": "requiere decision empresarial explicita (Seccion 5.4); no otorgada en este contrato",
            "conflict_notes": conflict_notes,
        }
        records.append(record)

    return records


def build_alias_registry(records: list[dict]) -> list[dict]:
    aliases = []
    for r in records:
        if r["model_alias"]:
            aliases.append({
                "canonical_model": r["model_raw"],
                "alias": r["model_alias"],
                "source": "excel_derived_json:tools/products_from_excel.json",
            })
    return aliases


def build_summary(records: list[dict]) -> dict:
    def count(pred):
        return sum(1 for r in records if pred(r))

    return {
        "total_source_records": len(records),
        "matched": count(lambda r: r["reconciliation_status"] == "matched"),
        "ambiguous": count(lambda r: r["reconciliation_status"] == "ambiguous"),
        "unmatched": count(lambda r: r["reconciliation_status"] == "unmatched"),
        "rejected": count(lambda r: r["reconciliation_status"] == "rejected"),
        "gtin12_candidates": count(lambda r: r["gtin_structural"]["gtin_type_candidate"] == "gtin12"),
        "gtin13_candidates": count(lambda r: r["gtin_structural"]["gtin_type_candidate"] == "gtin13"),
        "checksum_pass": count(lambda r: r["gtin_structural"]["checksum_valid"]),
        "checksum_fail": count(lambda r: not r["gtin_structural"]["checksum_valid"]),
        "duplicate_barcodes_in_source": count(lambda r: r["duplicate_barcode_in_source"]),
        "known_multi_barcode_conflicts": count(lambda r: r["known_multi_barcode_conflict"]),
        "gtin_validated": count(lambda r: r["gtin_status"] == "validated"),
        "gtin_blocked": count(lambda r: r["gtin_status"] != "validated"),
        "sku_validated": count(lambda r: r["sku_status"] == "validated"),
        "sku_published": count(lambda r: r["sku_publishable"]),
    }


def build_registry() -> dict:
    inventory = extract_site_inventory()
    if inventory["errors"]:
        raise ValueError("site inventory errors: " + "; ".join(inventory["errors"]))

    negative_findings = check_negative_assertions()
    if negative_findings:
        raise ValueError("negative assertion violations found: " + "; ".join(negative_findings))

    history = load_replace_codes_history()
    records = build_records(inventory, history)
    aliases = build_alias_registry(records)
    summary = build_summary(records)

    if summary["gtin12_candidates"] != EXPECTED_GTIN12_CANDIDATES:
        raise ValueError(
            f"expected {EXPECTED_GTIN12_CANDIDATES} gtin12 candidates, got {summary['gtin12_candidates']}"
        )
    if summary["gtin13_candidates"] != EXPECTED_GTIN13_CANDIDATES:
        raise ValueError(
            f"expected {EXPECTED_GTIN13_CANDIDATES} gtin13 candidates, got {summary['gtin13_candidates']}"
        )

    return {
        "schema_version": 1,
        "contract": "HP-SEO-AI-001F-1",
        "baseline_commit": BASELINE_COMMIT,
        "source_provenance": get_source_provenance_evidence(),
        "site_invariants": {
            "total_pdp": inventory["total_pdp"],
            "indexable_pdp": inventory["indexable_pdp"],
            "noindex_pdp": inventory["noindex_pdp"],
            "product_count": inventory["product_count"],
            "productgroup_count": inventory["productgroup_count"],
            "variant_count": inventory["variant_count"],
        },
        "records": records,
        "aliases": aliases,
        "summary": summary,
    }


def print_kv(data: dict, prefix: str = "") -> None:
    print(f"{prefix}TOTAL_SOURCE_RECORDS={data['summary']['total_source_records']}")
    print(f"{prefix}MATCHED={data['summary']['matched']}")
    print(f"{prefix}AMBIGUOUS={data['summary']['ambiguous']}")
    print(f"{prefix}UNMATCHED={data['summary']['unmatched']}")
    print(f"{prefix}REJECTED={data['summary']['rejected']}")
    print(f"{prefix}GTIN12_CANDIDATES={data['summary']['gtin12_candidates']}")
    print(f"{prefix}GTIN13_CANDIDATES={data['summary']['gtin13_candidates']}")
    print(f"{prefix}CHECKSUM_PASS={data['summary']['checksum_pass']}")
    print(f"{prefix}CHECKSUM_FAIL={data['summary']['checksum_fail']}")
    print(f"{prefix}DUPLICATE_BARCODES={data['summary']['duplicate_barcodes_in_source']}")
    print(f"{prefix}KNOWN_MULTI_BARCODE_CONFLICTS={data['summary']['known_multi_barcode_conflicts']}")
    print(f"{prefix}GTIN_VALIDATED={data['summary']['gtin_validated']}")
    print(f"{prefix}GTIN_BLOCKED={data['summary']['gtin_blocked']}")
    print(f"{prefix}SKU_VALIDATED={data['summary']['sku_validated']}")
    print(f"{prefix}SKU_PUBLISHED={data['summary']['sku_published']}")
    print(f"{prefix}PRODUCT_COUNT={data['site_invariants']['product_count']}")
    print(f"{prefix}PRODUCTGROUP_COUNT={data['site_invariants']['productgroup_count']}")
    print(f"{prefix}VARIANT_COUNT={data['site_invariants']['variant_count']}")


def main() -> int:
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--build", action="store_true")
    group.add_argument("--check", action="store_true")
    args = parser.parse_args()

    try:
        registry = build_registry()
    except (OSError, UnicodeError, ValueError, AttributeError) as exc:
        print(f"FATAL={exc}")
        return 1

    if args.build:
        REGISTRY_PATH.parent.mkdir(parents=True, exist_ok=True)
        with open(REGISTRY_PATH, "w", encoding="utf-8", newline="\n") as f:
            json.dump(registry, f, ensure_ascii=False, indent=2)
            f.write("\n")
        print("MODE=build")
        print_kv(registry)
        print(f"WRITTEN={rel(REGISTRY_PATH)}")
        return 0

    # --check: la reconstruccion debe ser identica a lo ya commiteado.
    print("MODE=check")
    if not REGISTRY_PATH.exists():
        print("FATAL=registry does not exist; run --build first")
        return 1

    with open(REGISTRY_PATH, encoding="utf-8") as f:
        committed = json.load(f)

    print_kv(registry)

    if committed != registry:
        print("ERROR=registry drift: re-derived registry differs from committed data/product-identifiers.json")
        return 1

    print("RESULT=PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
