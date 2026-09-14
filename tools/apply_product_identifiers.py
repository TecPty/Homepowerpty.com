#!/usr/bin/env python3
"""
HP-SEO-AI-001F-1R1 -- deterministic applier for validated product identifiers.

Reads data/product-identifiers.json (already built and validated by
validate_product_identifiers.py) and inserts gtin12/gtin13 into the existing
Product JSON-LD block of each PDP, but ONLY for records whose
publishing_status is exactly "validated" and gtin_publishable is true.

Defense-in-depth (Section 19): this applier does NOT blindly trust that the
registry never contains conflicting records. Before any write, it builds an
index by matched_product_id across every "validated" record. If more than one
record targets the same Product -- even with different GTIN types (gtin12 vs
gtin13) -- this is FATAL and nothing is written. A defective validator must
never be able to silently publish two conflicting identifiers to one Product.

SKU is never applied by this script: sku_publishable is always false under
this contract, and this applier enforces that as a hard defensive check
regardless of what the registry says.

Modes:
  --check  Full preflight/dry-run. Reports what WOULD change. Never writes.
  --apply  Runs the same preflight, then writes only the approved PDP files.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = ROOT / "data" / "product-identifiers.json"

SCRIPT_RE = re.compile(
    r'<script[^>]+type=["\']application/ld\+json["\'][^>]*>([\s\S]*?)</script>',
    re.I,
)


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def read_text(path: Path) -> str:
    return path.read_bytes().decode("utf-8")


def write_text(path: Path, content: str) -> None:
    path.write_bytes(content.encode("utf-8"))


def newline_for(text: str) -> str:
    return "\r\n" if "\r\n" in text else "\n"


def find_product_block(html: str, product_id: str) -> tuple[int, int, dict] | None:
    """Ubica el bloque <script ld+json> cuyo objeto es exactamente el Product
    con el @id esperado. Devuelve (start, end, objeto) del bloque de script
    completo, o None si no se encuentra."""
    for match in SCRIPT_RE.finditer(html):
        raw = match.group(1).strip()
        try:
            obj = json.loads(raw)
        except json.JSONDecodeError:
            continue
        if isinstance(obj, dict) and obj.get("@type") == "Product" and obj.get("@id") == product_id:
            return match.start(), match.end(), obj
    return None


def render_jsonld(entity: dict, nl: str) -> str:
    body = json.dumps(entity, ensure_ascii=False, indent=2)
    body = body.replace("\n", nl)
    body = nl.join("    " + line for line in body.split(nl))
    return f'<script type="application/ld+json">{nl}{body}{nl}    </script>'


def insert_gtin(entity: dict, gtin_key: str, gtin_value: str) -> dict:
    """Reconstruye el dict preservando el orden original, insertando la key
    gtin inmediatamente despues de 'model' (o al final si no hay 'model')."""
    if gtin_key in entity:
        raise ValueError(f"Product already has '{gtin_key}'; refusing to overwrite")
    new_entity: dict = {}
    inserted = False
    for key, value in entity.items():
        new_entity[key] = value
        if key == "model":
            new_entity[gtin_key] = gtin_value
            inserted = True
    if not inserted:
        new_entity[gtin_key] = gtin_value
    return new_entity


def load_registry() -> dict:
    with open(REGISTRY_PATH, encoding="utf-8") as f:
        return json.load(f)


def defense_in_depth_conflict_check(records: list[dict]) -> list[str]:
    """Seccion 19. Construye un indice por matched_product_id sobre TODOS los
    records validated/publishable, sin asumir que el validator los produjo
    correctamente. Mas de un record apuntando al mismo Product es FATAL, sin
    importar si los tipos de GTIN son distintos (gtin12 vs gtin13) -- ese es
    exactamente el modo de fallo silencioso que este chequeo existe para
    cerrar."""
    by_product: dict[str, list[dict]] = {}
    for record in records:
        if record.get("publishing_status") != "validated" or not record.get("gtin_publishable"):
            continue
        product_id = record.get("matched_product_id")
        if not product_id:
            continue
        by_product.setdefault(product_id, []).append(record)

    errors: list[str] = []
    for product_id, group in by_product.items():
        if len(group) > 1:
            details = ", ".join(
                f"{r['record_id']} ({r.get('gtin_type')}={r['barcode_raw']})" for r in group
            )
            errors.append(
                f"CONFLICTING PUBLISHABLE RECORDS for matched_product_id={product_id!r}: {details}"
            )
    return errors


def preflight(registry: dict) -> dict:
    records = registry["records"]

    # Defense-in-depth: corre ANTES que cualquier otra cosa. Si falla, no se
    # procesa ni se escribe absolutamente nada.
    conflict_errors = defense_in_depth_conflict_check(records)
    if conflict_errors:
        return {
            "errors": conflict_errors,
            "pending": {},
            "applied": 0,
            "already_applied": 0,
            "blocked": 0,
        }

    errors: list[str] = []
    pending: dict[Path, str] = {}
    already_applied = 0
    blocked = 0
    applied = 0

    for record in records:
        if record["sku_publishable"]:
            errors.append(
                f"{record['record_id']}: sku_publishable=true is forbidden under this contract"
            )
            continue

        if not (record["publishing_status"] == "validated" and record["gtin_publishable"]):
            blocked += 1
            continue

        gtin_type = record["gtin_type"]
        if gtin_type not in ("gtin12", "gtin13"):
            errors.append(
                f"{record['record_id']}: validated but gtin_type is '{gtin_type}'"
            )
            continue

        canonical_url = record["matched_canonical_url"]
        product_id = record["matched_product_id"]
        if not canonical_url or not product_id:
            errors.append(f"{record['record_id']}: validated but missing canonical_url/product_id")
            continue

        pdp_path = ROOT / "productos" / canonical_url.split("/productos/", 1)[1].strip("/")
        pdp_path = pdp_path / "index.html"

        if not pdp_path.exists():
            errors.append(f"{record['record_id']}: PDP not found at {rel(pdp_path)}")
            continue

        html = read_text(pdp_path)
        located = find_product_block(html, product_id)
        if located is None:
            errors.append(f"{record['record_id']}: Product block with @id={product_id} not found in {rel(pdp_path)}")
            continue

        start, end, entity = located
        barcode = record["barcode_raw"]

        if entity.get(gtin_type) == barcode:
            already_applied += 1
            continue
        if gtin_type in entity:
            errors.append(
                f"{record['record_id']}: {rel(pdp_path)} already has {gtin_type}="
                f"{entity.get(gtin_type)!r}, conflicts with validated {barcode!r}"
            )
            continue
        # Defensa adicional: si el PDP ya tiene CUALQUIER otro gtin (del tipo
        # que sea) proveniente de una escritura previa, no lo pisamos ni lo
        # ignoramos silenciosamente.
        existing_gtin_keys = [k for k in ("gtin12", "gtin13") if k in entity]
        if existing_gtin_keys:
            errors.append(
                f"{record['record_id']}: {rel(pdp_path)} already has {existing_gtin_keys}, "
                f"refusing to add a second gtin identifier to the same Product"
            )
            continue

        try:
            updated_entity = insert_gtin(entity, gtin_type, barcode)
        except ValueError as exc:
            errors.append(f"{record['record_id']}: {exc}")
            continue

        new_block = render_jsonld(updated_entity, newline_for(html))
        new_html = html[:start] + new_block + html[end:]

        # Validacion before/after: ninguna otra propiedad del Product cambio.
        relocated = find_product_block(new_html, product_id)
        if relocated is None:
            errors.append(f"{record['record_id']}: Product block missing after edit in {rel(pdp_path)}")
            continue
        _, _, after_entity = relocated
        expected_after = dict(entity)
        expected_after[gtin_type] = barcode
        if after_entity != expected_after:
            errors.append(f"{record['record_id']}: unexpected diff in Product entity after edit in {rel(pdp_path)}")
            continue

        pending[pdp_path] = pending.get(pdp_path, html)
        pending[pdp_path] = new_html
        applied += 1

    return {
        "errors": errors,
        "pending": pending,
        "applied": applied,
        "already_applied": already_applied,
        "blocked": blocked,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--check", action="store_true")
    group.add_argument("--apply", action="store_true")
    args = parser.parse_args()

    if not REGISTRY_PATH.exists():
        print(f"FATAL=registry not found at {rel(REGISTRY_PATH)}; run validate_product_identifiers.py --build first")
        return 1

    registry = load_registry()
    result = preflight(registry)

    mode = "apply" if args.apply else "check"
    print(f"MODE={mode}")
    print(f"TO_APPLY={result['applied']}")
    print(f"ALREADY_APPLIED={result['already_applied']}")
    print(f"BLOCKED={result['blocked']}")
    print(f"ERRORS={len(result['errors'])}")

    for error in result["errors"]:
        print("ERROR=" + error)

    if result["errors"]:
        return 1

    if args.check:
        for path in sorted(result["pending"], key=rel):
            print("PENDING=" + rel(path))
        return 0

    for path in sorted(result["pending"], key=rel):
        write_text(path, result["pending"][path])

    print(f"WRITTEN={len(result['pending'])}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
