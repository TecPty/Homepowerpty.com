#!/usr/bin/env python3
"""
HP-SEO-AI-001F-1R1 -- deterministic product identifier registry builder/validator.

Five independent, sequential gates, per contract Section 4:

  Gate 1  Source manifest integrity   (data/product-identifiers-source-manifest.json)
  Gate 2  Source conflict / dedup     (barcode collisions AND model collisions)
  Gate 3  Identity reconciliation     (does the record map to exactly one Product?)
  Gate 4  GTIN structural validation  (numeric / length / checksum / type)
  Gate 5  PDP corroboration           (does the visible pdp-barcode agree?)

None of these gates may answer for another. A Product match is never treated
as business provenance; a missing PDP barcode never becomes a false "matched";
identity reconciliation never reports on checksum or provenance.

Determinism policy (Section 20): the registry must not depend on checkout
depth, git log, current time, network access, or Google Drive availability.
All business-source metadata comes from the static, versioned manifest --
never from `git log`.

Modes:
  --build   Runs all five gates and writes data/product-identifiers.json.
            Fails closed: never writes a registry that violates a structural,
            manifest-integrity, or negative-assertion invariant.
  --check   Re-derives the registry from the same sources and verifies it is
            byte-for-byte identical to the committed data/product-identifiers.json.
            Never writes. Used as the idempotency/CI/determinism gate.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PRODUCTS_ROOT = ROOT / "productos"
EXCEL_JSON_PATH = ROOT / "tools" / "products_from_excel.json"
REPLACE_CODES_PATH = ROOT / "tools" / "replace_codes.py"
REGISTRY_PATH = ROOT / "data" / "product-identifiers.json"
MANIFEST_PATH = ROOT / "data" / "product-identifiers-source-manifest.json"

BASELINE_COMMIT = "d917c6e4e4900317d685b44024602b69f8f9b4df"
SUPPORTED_MANIFEST_SCHEMA_VERSION = 1

EXPECTED_TOTAL_PDP = 127
EXPECTED_INDEXABLE_PDP = 126
EXPECTED_NOINDEX_PDP = 1
EXPECTED_PRODUCT_COUNT = 117
EXPECTED_PRODUCTGROUP_COUNT = 9
EXPECTED_VARIANT_COUNT = 46

# Casos de conflicto conocidos obligatorios (Seccion 10 del Acceptance Contract
# R1 / Seccion 8 del contrato F-1 original). El barcode "current" es el que
# aparece en el source empresarial vigente; el resto son alternates hallados
# unicamente en el tooling historico (tools/replace_codes.py), clasificados
# aparte y sin publishing_eligible.
KNOWN_MULTI_BARCODE_MODELS = {"JR-A101", "JR-LD8", "HP-017"}

SCRIPT_RE = re.compile(
    r'<script[^>]+type=["\']application/ld\+json["\'][^>]*>([\s\S]*?)</script>',
    re.I,
)
ROBOTS_RE = re.compile(
    r'<meta[^>]+name=["\']robots["\'][^>]+content=["\']([^"\']+)["\']',
    re.I,
)
PDP_BARCODE_RE = re.compile(
    r'<p class="pdp-barcode">C[ÓO]D\.?\s*BARRAS:\s*([0-9]+)</p>',
    re.I,
)
FORBIDDEN_KEYS = {
    "offer", "aggregateoffer", "price", "lowprice", "highprice",
    "pricecurrency", "availability", "seller", "review", "aggregaterating",
    "shippingdetails", "returnpolicy", "mpn", "sku",
}


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def read_text(path: Path) -> str:
    return path.read_bytes().decode("utf-8")


def normalized_bytes(path: Path) -> bytes:
    """Lee un archivo y normaliza line-endings a LF antes de cualquier uso
    canonico (hashing). Un checkout local puede materializar CRLF (p.ej.
    Windows con core.autocrlf) mientras el blob almacenado en git es LF; sin
    esta normalizacion, el mismo contenido logico produce hashes distintos
    segun el entorno de checkout -- exactamente la clase de no-determinismo
    que la Seccion 20 prohibe. Esto NO invoca git: es normalizacion de bytes
    pura en Python, independiente de cualquier configuracion de checkout."""
    raw = path.read_bytes()
    text = raw.decode("utf-8")
    normalized = text.replace("\r\n", "\n").replace("\r", "\n")
    return normalized.encode("utf-8")


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
    comerciales prohibidos (negative assertions, Seccion 27)."""
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
    modelo canonico nunca se publica concatenado con su alias."""
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
    """Gate 4. Independiente de reconciliation y de source authority."""
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
    elif gtin_type is None:
        status = "unsupported_type"
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
    tools/replace_codes.py. Fuente de provenance de 'tooling historico'
    unicamente; nunca cuenta como current-source collision (Seccion 10)."""
    spec = importlib.util.spec_from_file_location("replace_codes_frozen", REPLACE_CODES_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)  # solo define CODE_TO_SKU; run() esta bajo __main__ guard
    model_to_barcodes: dict[str, list[str]] = {}
    for barcode, model in module.CODE_TO_SKU.items():
        model_to_barcodes.setdefault(normalize_model(model), []).append(barcode)
    return model_to_barcodes


def extract_pdp_barcode(html: str) -> str | None:
    match = PDP_BARCODE_RE.search(html)
    return match.group(1) if match else None


def extract_site_inventory() -> dict:
    """Enumera las 117 entidades Product reales del sitio (una por PDP propio),
    detecta cuales son variantes de algun ProductGroup, y confirma los
    invariantes estructurales del baseline."""
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


# ---------------------------------------------------------------------------
# Gate 1 -- Source manifest integrity
# ---------------------------------------------------------------------------

def load_manifest() -> dict:
    with open(MANIFEST_PATH, encoding="utf-8") as f:
        return json.load(f)


def verify_manifest_integrity(manifest: dict) -> dict:
    """Gate 1. No depende de git/red/reloj. FATAL si el hash no coincide;
    nunca se reconstruye el manifest automaticamente para hacer desaparecer
    el error (Seccion 8)."""
    errors: list[str] = []

    schema_version = manifest.get("manifest_schema_version")
    if schema_version != SUPPORTED_MANIFEST_SCHEMA_VERSION:
        errors.append(f"unsupported manifest_schema_version: {schema_version!r}")

    snapshot_info = manifest.get("derived_snapshot", {})
    snapshot_rel_path = snapshot_info.get("path")
    snapshot_path = ROOT / snapshot_rel_path if snapshot_rel_path else None

    if snapshot_path is None or not snapshot_path.exists():
        errors.append(f"derived snapshot not found: {snapshot_rel_path!r}")
        return {"status": "fatal", "errors": errors}

    snapshot_bytes = normalized_bytes(snapshot_path)
    actual_sha256 = hashlib.sha256(snapshot_bytes).hexdigest()
    expected_sha256 = snapshot_info.get("sha256")
    if actual_sha256 != expected_sha256:
        errors.append(
            f"snapshot hash mismatch: manifest declares {expected_sha256!r}, "
            f"actual is {actual_sha256!r}"
        )

    source_records = json.loads(snapshot_bytes.decode("utf-8"))

    expected_count = manifest.get("business_source", {}).get("expected_record_count")
    actual_count = len(source_records)
    if actual_count != expected_count:
        errors.append(
            f"record count mismatch: manifest declares {expected_count!r}, "
            f"snapshot has {actual_count!r}"
        )

    return {
        "status": "fatal" if errors else "pass",
        "errors": errors,
        "expected_sha256": expected_sha256,
        "actual_sha256": actual_sha256,
        "expected_record_count": expected_count,
        "actual_record_count": actual_count,
        "source_records": source_records if not errors else None,
    }


# ---------------------------------------------------------------------------
# Gate 2 -- Source conflict / dedup (barcode AND model, independently)
# ---------------------------------------------------------------------------

def detect_source_conflicts(source_records: list[dict]) -> list[dict]:
    """Gate 2. Un mismo model_normalized con mas de un barcode DISTINTO en el
    source bloquea TODOS los records de ese modelo, incluso si cada barcode es
    individualmente unico y estructuralmente valido (D1)."""
    barcode_count: dict[str, int] = {}
    model_to_barcodes: dict[str, set[str]] = {}
    parsed: list[dict] = []

    for raw in source_records:
        model_raw, alias = split_raw_sku(raw["sku"])
        model_normalized = normalize_model(model_raw)
        barcode_raw = raw["barcode"]
        parsed.append({
            "raw": raw,
            "model_raw": model_raw,
            "model_alias": alias,
            "model_normalized": model_normalized,
            "barcode_raw": barcode_raw,
        })
        barcode_count[barcode_raw] = barcode_count.get(barcode_raw, 0) + 1
        model_to_barcodes.setdefault(model_normalized, set()).add(barcode_raw)

    for p in parsed:
        barcode_collision = barcode_count[p["barcode_raw"]] > 1
        model_collision = len(model_to_barcodes[p["model_normalized"]]) > 1
        if barcode_collision:
            status = "barcode_collision"
        elif model_collision:
            status = "model_collision"
        else:
            status = "none"
        p["source_conflict_status"] = status

    return parsed


# ---------------------------------------------------------------------------
# Gate 3 -- Identity reconciliation (answers ONLY matched/unmatched/ambiguous)
# ---------------------------------------------------------------------------

def reconcile_identity(model_normalized: str, products: dict) -> tuple[str, dict | None]:
    matches = [k for k in products if k == model_normalized]
    if len(matches) == 1:
        return "matched", products[matches[0]]
    if len(matches) == 0:
        return "unmatched", None
    return "ambiguous", None


# ---------------------------------------------------------------------------
# Gate 5 -- PDP corroboration (reads the real PDP; never inferred)
# ---------------------------------------------------------------------------

def pdp_corroboration(match_info: dict | None, barcode_raw: str) -> dict:
    if match_info is None:
        return {"status": "not_applicable", "pdp_barcode": None}
    pdp_path = ROOT / match_info["path"]
    html = read_text(pdp_path)
    pdp_barcode = extract_pdp_barcode(html)
    if pdp_barcode is None:
        return {"status": "absent", "pdp_barcode": None}
    if pdp_barcode == barcode_raw:
        return {"status": "matched", "pdp_barcode": pdp_barcode}
    return {"status": "mismatch", "pdp_barcode": pdp_barcode}


# ---------------------------------------------------------------------------
# Publication gate -- combines the five gates; never lets one gate answer
# for another (Section 18).
# ---------------------------------------------------------------------------

def determine_publishing_status(
    source_conflict_status: str,
    reconciliation_status: str,
    gtin_struct: dict,
    pdp_corrob: dict,
) -> tuple[str, bool, list[str]]:
    notes: list[str] = []

    if source_conflict_status == "barcode_collision":
        notes.append("source_conflict_status=barcode_collision")
        return "blocked", False, notes
    if source_conflict_status == "model_collision":
        notes.append("source_conflict_status=model_collision (multiples barcodes distintos para el mismo modelo)")
        return "blocked", False, notes
    if reconciliation_status != "matched":
        notes.append(f"identity_reconciliation_status={reconciliation_status}")
        return "blocked", False, notes
    if gtin_struct["structural_status"] != "structurally_valid":
        notes.append(f"gtin_structural_status={gtin_struct['structural_status']}")
        return "blocked", False, notes
    if pdp_corrob["status"] == "mismatch":
        notes.append(
            f"pdp_corroboration_status=mismatch (pdp_barcode={pdp_corrob['pdp_barcode']!r})"
        )
        return "blocked", False, notes

    # pdp_corroboration_status == absent NO bloquea por si solo (Seccion 16).
    return "validated", True, notes


def build_records(manifest_result: dict, inventory: dict, history: dict[str, list[str]]) -> list[dict]:
    source_records = manifest_result["source_records"]
    products = inventory["products"]

    conflicts = detect_source_conflicts(source_records)
    records: list[dict] = []

    for idx, parsed in enumerate(conflicts, start=1):
        model_raw = parsed["model_raw"]
        model_normalized = parsed["model_normalized"]
        barcode_raw = parsed["barcode_raw"]
        raw = parsed["raw"]

        reconciliation_status, match_info = reconcile_identity(model_normalized, products)
        gtin_struct = classify_gtin_structure(barcode_raw)
        pdp_corrob = pdp_corroboration(match_info, barcode_raw)

        alternates = []
        historical = history.get(model_normalized, [])
        confirmed_by_historical_tooling = False
        for alt_barcode in historical:
            if alt_barcode == barcode_raw:
                confirmed_by_historical_tooling = True
                continue
            alternates.append({
                "barcode": alt_barcode,
                "classification": "alternate",
                "source": ["historical_tooling:tools/replace_codes.py"],
                "publishing_eligible": False,
                "reason": "sin provenance empresarial vigente (solo tooling historico)",
            })

        historical_conflict_status = (
            "known_conflict"
            if (
                model_raw.strip().upper() in KNOWN_MULTI_BARCODE_MODELS
                or model_normalized in {normalize_model(m) for m in KNOWN_MULTI_BARCODE_MODELS}
            )
            else "none"
        )

        publishing_status, gtin_publishable, notes = determine_publishing_status(
            parsed["source_conflict_status"],
            reconciliation_status,
            gtin_struct,
            pdp_corrob,
        )

        record = {
            "record_id": f"excel-{idx:03d}",
            "raw_sku_field": raw["sku"],
            "model_raw": model_raw,
            "model_alias": parsed["model_alias"],
            "model_normalized": model_normalized,
            "es_nuevo": raw.get("es_nuevo", False),
            "barcode_raw": barcode_raw,
            "gates": {
                "source_conflict_status": parsed["source_conflict_status"],
                "identity_reconciliation_status": reconciliation_status,
                "gtin_structural_status": gtin_struct["structural_status"],
                "pdp_corroboration_status": pdp_corrob["status"],
                "historical_conflict_status": historical_conflict_status,
            },
            "gtin_structural": gtin_struct,
            "pdp_corroboration": pdp_corrob,
            "matched_model": match_info["model"] if match_info else None,
            "matched_product_id": match_info["product_id"] if match_info else None,
            "matched_canonical_url": match_info["canonical_url"] if match_info else None,
            "is_variant": match_info["is_variant"] if match_info else None,
            "product_group_url": match_info["product_group_url"] if match_info else None,
            "confirmed_by_historical_tooling": confirmed_by_historical_tooling,
            "alternate_barcodes": alternates,
            "publishing_status": publishing_status,
            "gtin_publishable": gtin_publishable,
            "gtin_type": gtin_struct["gtin_type_candidate"] if gtin_publishable else None,
            "sku_candidate": model_raw,
            "sku_status": "candidate",
            "sku_publishable": False,
            "sku_publish_reason": "requiere decision empresarial explicita; no otorgada bajo este contrato",
            "notes": notes,
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
        "model_collisions": count(lambda r: r["gates"]["source_conflict_status"] == "model_collision"),
        "barcode_collisions": count(lambda r: r["gates"]["source_conflict_status"] == "barcode_collision"),
        "matched": count(lambda r: r["gates"]["identity_reconciliation_status"] == "matched"),
        "ambiguous": count(lambda r: r["gates"]["identity_reconciliation_status"] == "ambiguous"),
        "unmatched": count(lambda r: r["gates"]["identity_reconciliation_status"] == "unmatched"),
        "gtin12_candidates": count(lambda r: r["gtin_structural"]["gtin_type_candidate"] == "gtin12"),
        "gtin13_candidates": count(lambda r: r["gtin_structural"]["gtin_type_candidate"] == "gtin13"),
        "checksum_pass": count(lambda r: r["gtin_structural"]["checksum_valid"]),
        "checksum_fail": count(lambda r: not r["gtin_structural"]["checksum_valid"]),
        "pdp_match": count(lambda r: r["gates"]["pdp_corroboration_status"] == "matched"),
        "pdp_mismatch": count(lambda r: r["gates"]["pdp_corroboration_status"] == "mismatch"),
        "pdp_absent": count(lambda r: r["gates"]["pdp_corroboration_status"] == "absent"),
        "known_multi_barcode_conflicts": count(lambda r: r["gates"]["historical_conflict_status"] == "known_conflict"),
        "gtin_validated": count(lambda r: r["publishing_status"] == "validated"),
        "gtin_blocked": count(lambda r: r["publishing_status"] == "blocked"),
        "sku_validated": count(lambda r: r["sku_status"] == "validated"),
        "sku_published": count(lambda r: r["sku_publishable"]),
    }


def build_registry() -> dict:
    manifest = load_manifest()
    manifest_result = verify_manifest_integrity(manifest)
    if manifest_result["status"] == "fatal":
        raise ValueError("manifest integrity FATAL: " + "; ".join(manifest_result["errors"]))

    inventory = extract_site_inventory()
    if inventory["errors"]:
        raise ValueError("site inventory errors: " + "; ".join(inventory["errors"]))

    negative_findings = check_negative_assertions()
    if negative_findings:
        raise ValueError("negative assertion violations found: " + "; ".join(negative_findings))

    history = load_replace_codes_history()
    records = build_records(manifest_result, inventory, history)
    aliases = build_alias_registry(records)
    summary = build_summary(records)

    mismatches = [r for r in records if r["gates"]["pdp_corroboration_status"] == "mismatch"]
    if mismatches:
        details = "; ".join(
            f"{r['model_raw']} ({r['matched_canonical_url']}): source={r['barcode_raw']} "
            f"pdp={r['pdp_corroboration']['pdp_barcode']}"
            for r in mismatches
        )
        raise ValueError(
            "HIGH-SEVERITY: pdp_corroboration_status=mismatch detected -- STOP, do not publish, "
            "do not modify PDP within this contract: " + details
        )

    return {
        "schema_version": 2,
        "contract": "HP-SEO-AI-001F-1R1",
        "baseline_commit": BASELINE_COMMIT,
        "manifest": {
            "path": rel(MANIFEST_PATH),
            "business_source_status": "pass",
            "snapshot_integrity_status": manifest_result["status"],
            "expected_sha256": manifest_result["expected_sha256"],
            "actual_sha256": manifest_result["actual_sha256"],
            "expected_record_count": manifest_result["expected_record_count"],
            "actual_record_count": manifest_result["actual_record_count"],
        },
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
    s = data["summary"]
    print(f"{prefix}SOURCE_RECORDS={s['total_source_records']}")
    print(f"{prefix}MODEL_COLLISIONS={s['model_collisions']}")
    print(f"{prefix}BARCODE_COLLISIONS={s['barcode_collisions']}")
    print(f"{prefix}MATCHED={s['matched']}")
    print(f"{prefix}AMBIGUOUS={s['ambiguous']}")
    print(f"{prefix}UNMATCHED={s['unmatched']}")
    print(f"{prefix}GTIN12={s['gtin12_candidates']}")
    print(f"{prefix}GTIN13={s['gtin13_candidates']}")
    print(f"{prefix}CHECKSUM_PASS={s['checksum_pass']}")
    print(f"{prefix}CHECKSUM_FAIL={s['checksum_fail']}")
    print(f"{prefix}PDP_MATCH={s['pdp_match']}")
    print(f"{prefix}PDP_MISMATCH={s['pdp_mismatch']}")
    print(f"{prefix}PDP_ABSENT={s['pdp_absent']}")
    print(f"{prefix}KNOWN_MULTI_BARCODE_CONFLICTS={s['known_multi_barcode_conflicts']}")
    print(f"{prefix}GTIN_VALIDATED={s['gtin_validated']}")
    print(f"{prefix}GTIN_BLOCKED={s['gtin_blocked']}")
    print(f"{prefix}SKU_VALIDATED={s['sku_validated']}")
    print(f"{prefix}SKU_PUBLISHED={s['sku_published']}")
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
    except (OSError, UnicodeError, ValueError, AttributeError, json.JSONDecodeError) as exc:
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
