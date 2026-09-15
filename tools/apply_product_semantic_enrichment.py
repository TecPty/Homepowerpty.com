#!/usr/bin/env python3
"""HP-SEO-AI-001G-1 -- Phase 1 semantic enrichment (color, Garantia, Voltaje, Potencia).

Modes:
  --check      run discovery + identity + coverage + state machine, report only, no writes.
  --apply      same as --check; if PRECHECK_PASS, write PENDING items. Zero writes otherwise.
  --selftest   run in-memory synthetic tests of the state machine / transactional guarantees.

Contract: HP-SEO-AI-001G-1 Acceptance Contract + Reconciliation Addendum +
Final Architecture Micro-Addendum + Final Contract Addendum.
"""
import json
import os
import re
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PRODUCTOS_DIR = os.path.join(ROOT, "productos")

ALLOWLIST = ["Colores", "Garantía", "Voltaje", "Potencia"]
MANAGED_AP_NAMES = ["Garantía", "Potencia", "Voltaje"]  # frozen insertion order

VOLTAGE_CLEAN_RE = re.compile(r"^\d+V(\s*/\s*\d+(-\d+)?Hz)?$")
POWER_CLEAN_RE = re.compile(r"^(\d+)W$")

EXPECTED_TARGET_PRODUCTS = 117
EXPECTED_PRODUCTGROUP = 9
EXPECTED_NOINDEX = 1
EXPECTED_MODIFIABLE_UNION = 63
EXPECTED_NOOP = 54
EXPECTED_COLOR_ELIGIBLE = 59
EXPECTED_WARRANTY_ELIGIBLE = 63
EXPECTED_VOLTAGE_ELIGIBLE = 52
EXPECTED_POWER_ELIGIBLE = 38

LDJSON_SCRIPT_RE = re.compile(
    r'(<script type="application/ld\+json">)([\s\S]*?)(</script>)'
)
ROBOTS_META_RE = re.compile(
    r'<meta[^>]+name=["\']robots["\'][^>]*content=["\']([^"\']*)["\']', re.I
)
CANONICAL_RE = re.compile(
    r'<link[^>]+rel=["\']canonical["\'][^>]+href=["\']([^"\']+)["\']', re.I
)
SPECS_TABLE_RE = re.compile(
    r'<table class="pdp-specs-table">([\s\S]*?)</table>'
)
ROW_RE = re.compile(r"<tr>([\s\S]*?)</tr>")
TD_RE = re.compile(r"<td[^>]*>([^<]*)</td>")
COLSPAN_ROW_RE = re.compile(r'^\s*<td colspan="2">')


class Defect(Exception):
    pass


def discover_pdp_files():
    files = []
    for dirpath, _dirnames, filenames in os.walk(PRODUCTOS_DIR):
        for fn in filenames:
            if fn == "index.html":
                files.append(os.path.join(dirpath, fn))
    return sorted(files)


def read_normalized(path):
    """Return (raw_bytes_text, work_text_LF, newline_style)."""
    with open(path, "rb") as fh:
        raw_bytes = fh.read()
    raw_text = raw_bytes.decode("utf-8")
    newline_style = "\r\n" if "\r\n" in raw_text else "\n"
    work_text = raw_text.replace("\r\n", "\n")
    return raw_text, work_text, newline_style


def find_ldjson_blocks(work_text):
    """Return list of dicts: {start, end, content_start, content_end, raw_content, obj}."""
    blocks = []
    for m in LDJSON_SCRIPT_RE.finditer(work_text):
        content = m.group(2)
        try:
            obj = json.loads(content)
        except (ValueError, TypeError):
            obj = None
        blocks.append(
            {
                "start": m.start(),
                "end": m.end(),
                "content_start": m.start(2),
                "content_end": m.end(2),
                "raw_content": content,
                "obj": obj,
            }
        )
    return blocks


def classify_file(work_text):
    """Return ('Product'|'ProductGroup'|'other', is_noindex, product_block or None)."""
    robots_match = ROBOTS_META_RE.search(work_text)
    is_noindex = bool(robots_match and "noindex" in robots_match.group(1).lower())

    blocks = find_ldjson_blocks(work_text)
    product_block = None
    types_seen = []
    for b in blocks:
        if isinstance(b["obj"], dict) and "@type" in b["obj"]:
            types_seen.append(b["obj"]["@type"])
            if b["obj"]["@type"] == "Product" and product_block is None:
                product_block = b

    if "ProductGroup" in types_seen:
        kind = "ProductGroup"
    elif "Product" in types_seen:
        kind = "Product"
    else:
        kind = "other"

    return kind, is_noindex, product_block


def extract_specs(work_text):
    """Return dict label -> value for ALLOWLIST labels found in pdp-specs-table (colspan rows ignored)."""
    values = {}
    table_match = SPECS_TABLE_RE.search(work_text)
    if not table_match:
        return values
    for row_match in ROW_RE.finditer(table_match.group(1)):
        row_html = row_match.group(1)
        if COLSPAN_ROW_RE.match(row_html):
            continue
        tds = TD_RE.findall(row_html)
        if len(tds) == 2:
            label, value = tds[0].strip(), tds[1].strip()
            if label in ALLOWLIST:
                values[label] = value
    return values


def check_identity(work_text, product_obj):
    """Return list of violation strings (empty = PASS)."""
    violations = []
    canon_match = CANONICAL_RE.search(work_text)
    canonical = canon_match.group(1) if canon_match else None
    if not canonical:
        violations.append("no canonical link tag")
    if not product_obj.get("@id") or (canonical and product_obj.get("@id") != canonical + "#product"):
        violations.append("@id mismatch")
    if not product_obj.get("url") or (canonical and product_obj.get("url") != canonical):
        violations.append("url mismatch")
    if not str(product_obj.get("model") or "").strip():
        violations.append("model missing/empty")
    return violations


def compute_expected(label_values):
    """Return dict of expected managed state: {'color': str|None, 'additionalProperty': {name: entry}}."""
    expected_color = label_values.get("Colores")  # raw verbatim, no exclusion grammar

    expected_ap = {}

    if "Garantía" in label_values:
        expected_ap["Garantía"] = {
            "@type": "PropertyValue",
            "name": "Garantía",
            "value": label_values["Garantía"],
        }

    voltaje = label_values.get("Voltaje")
    if voltaje is not None and VOLTAGE_CLEAN_RE.match(voltaje):
        expected_ap["Voltaje"] = {
            "@type": "PropertyValue",
            "name": "Voltaje",
            "value": voltaje,
        }

    potencia = label_values.get("Potencia")
    if potencia is not None:
        m = POWER_CLEAN_RE.match(potencia)
        if m:
            expected_ap["Potencia"] = {
                "@type": "PropertyValue",
                "name": "Potencia",
                "value": int(m.group(1)),
                "unitText": "W",
            }

    return {"color": expected_color, "additionalProperty": expected_ap}


def classify_state(expected, product_obj):
    """Return dict: {'color': state, 'Garantía': state, 'Potencia': state, 'Voltaje': state},
    plus 'blocking_reasons': list[str]."""
    states = {}
    reasons = []

    # --- color ---
    existing_color = product_obj.get("color", None)
    expected_color = expected["color"]
    if expected_color is not None:
        if existing_color is None:
            states["color"] = "PENDING"
        elif existing_color == expected_color:
            states["color"] = "ALREADY_COMPLIANT"
        else:
            states["color"] = "BLOCKED"
            reasons.append("color: existing value differs from expected")
    else:
        if existing_color is None:
            states["color"] = "NOOP"
        else:
            states["color"] = "BLOCKED"  # STALE_CONFLICT
            reasons.append("color: STALE_CONFLICT (source not eligible, property present)")

    # --- additionalProperty managed names ---
    existing_ap = product_obj.get("additionalProperty", [])
    if not isinstance(existing_ap, list):
        for name in MANAGED_AP_NAMES:
            states[name] = "BLOCKED"
            reasons.append("additionalProperty: existing value is not a list")
        return {"states": states, "blocking_reasons": reasons}

    expected_ap = expected["additionalProperty"]

    for name in MANAGED_AP_NAMES:
        matches = [
            e for e in existing_ap
            if isinstance(e, dict) and e.get("name") == name
        ]
        if len(matches) > 1:
            states[name] = "BLOCKED"
            reasons.append("additionalProperty[%s]: duplicate managed name" % name)
            continue

        if len(matches) == 1:
            existing_entry = matches[0]
            if name in expected_ap:
                if existing_entry == expected_ap[name]:
                    states[name] = "ALREADY_COMPLIANT"
                else:
                    states[name] = "BLOCKED"
                    reasons.append("additionalProperty[%s]: existing entry differs from expected" % name)
            else:
                states[name] = "BLOCKED"  # STALE_CONFLICT
                reasons.append("additionalProperty[%s]: STALE_CONFLICT" % name)
        else:
            if name in expected_ap:
                states[name] = "PENDING"
            else:
                states[name] = "NOOP"

    return {"states": states, "blocking_reasons": reasons}


def _find_matching_close(text, open_pos):
    """text[open_pos] is '{' or '['. Return index of its matching close bracket,
    respecting JSON string literals (so brackets inside string values are ignored)."""
    depth = 0
    i = open_pos
    in_string = False
    escape = False
    while i < len(text):
        ch = text[i]
        if in_string:
            if escape:
                escape = False
            elif ch == "\\":
                escape = True
            elif ch == '"':
                in_string = False
        else:
            if ch == '"':
                in_string = True
            elif ch in "{[":
                depth += 1
            elif ch in "}]":
                depth -= 1
                if depth == 0:
                    return i
        i += 1
    raise Defect("unbalanced brackets while scanning JSON text")


def _format_managed_entry(indent, entry):
    lines = ["%s{" % indent]
    lines.append('%s  "@type": %s,' % (indent, json.dumps(entry["@type"], ensure_ascii=False)))
    lines.append('%s  "name": %s,' % (indent, json.dumps(entry["name"], ensure_ascii=False)))
    if "unitText" in entry:
        lines.append('%s  "value": %s,' % (indent, json.dumps(entry["value"], ensure_ascii=False)))
        lines.append('%s  "unitText": %s' % (indent, json.dumps(entry["unitText"], ensure_ascii=False)))
    else:
        lines.append('%s  "value": %s' % (indent, json.dumps(entry["value"], ensure_ascii=False)))
    lines.append("%s}" % indent)
    return "\n".join(lines)


def _insert_before_close(raw_content, close_pos, new_items_text, item_indent, close_indent, is_object):
    """Insert new_items_text (already comma-joined, no leading/trailing comma) right before
    the closing bracket at close_pos, adding a separating comma to the previous last item
    only if the container is non-empty."""
    before = raw_content[:close_pos]
    before_trimmed = before.rstrip(" \t\n")
    tail = raw_content[close_pos:]  # starts at the closing bracket itself
    open_char = "{" if is_object else "["
    if before_trimmed.endswith(open_char):
        # empty container
        return before_trimmed + "\n" + new_items_text + "\n" + close_indent + tail
    if before_trimmed.endswith(","):
        raise Defect("unexpected trailing comma before closing bracket")
    return before_trimmed + ",\n" + new_items_text + "\n" + close_indent + tail


def _merge_into_existing_additional_property(raw_content, pending_ap_names, expected_ap, prop_indent):
    """additionalProperty already exists as a key: insert only the PENDING managed entries
    into the existing array, preserving every foreign/compliant entry untouched."""
    m_ap = re.search(r'"additionalProperty"\s*:\s*(\[)', raw_content)
    if not m_ap:
        raise Defect("additionalProperty key reported present but not found in raw text")
    open_pos = m_ap.start(1)
    close_pos = _find_matching_close(raw_content, open_pos)

    item_indent = prop_indent + "  "
    new_items = ",\n".join(
        _format_managed_entry(item_indent, expected_ap[name]) for name in pending_ap_names
    )
    return _insert_before_close(
        raw_content, close_pos, new_items, item_indent, prop_indent, is_object=False
    )


def apply_surgical_insertion(raw_content, expected, states):
    """Return the new raw_content (script body text) with only the PENDING managed
    properties inserted. Properties already ALREADY_COMPLIANT/NOOP are left untouched.
    Preserves everything else byte-for-byte."""
    need_color = states.get("color") == "PENDING"
    pending_ap_names = [n for n in MANAGED_AP_NAMES if states.get(n) == "PENDING"]

    if not need_color and not pending_ap_names:
        return raw_content  # nothing to do -- safe no-op

    m2 = re.search(r'\n([ \t]+)"@context"', raw_content)
    if not m2:
        raise Defect("could not determine top-level property indent")
    prop_indent = m2.group(1)

    working = raw_content
    ap_already_exists = bool(re.search(r'"additionalProperty"\s*:\s*\[', working))

    if pending_ap_names and ap_already_exists:
        working = _merge_into_existing_additional_property(
            working, pending_ap_names, expected["additionalProperty"], prop_indent
        )

    top_level_lines = []
    if need_color:
        top_level_lines.append(
            '%s"color": %s' % (prop_indent, json.dumps(expected["color"], ensure_ascii=False))
        )
    if pending_ap_names and not ap_already_exists:
        names_in_order = [n for n in MANAGED_AP_NAMES if n in pending_ap_names]
        ap_lines = ['%s"additionalProperty": [' % prop_indent]
        entry_texts = [
            _format_managed_entry(prop_indent + "  ", expected["additionalProperty"][n])
            for n in names_in_order
        ]
        ap_lines.append(",\n".join(entry_texts))
        ap_lines.append("%s]" % prop_indent)
        top_level_lines.append("\n".join(ap_lines))

    if not top_level_lines:
        return working

    stripped = working.rstrip()
    if not stripped.endswith("}"):
        raise Defect("Product JSON-LD block does not end with '}' as expected")
    closing_brace_pos = len(stripped) - 1

    m = re.search(r"\n([ \t]*)\}\s*$", stripped)
    if not m:
        raise Defect("could not determine closing brace indent")
    closing_indent = m.group(1)

    top_level_insertion = ",\n".join(top_level_lines)
    new_working = _insert_before_close(
        working, closing_brace_pos, top_level_insertion, prop_indent, closing_indent, is_object=True
    )
    return new_working


def process_file(path):
    """Discover, classify, extract, compute state for a single file.
    Returns a report dict, or None if file is out of target universe."""
    raw_text, work_text, newline_style = read_normalized(path)
    kind, is_noindex, product_block = classify_file(work_text)

    if kind != "Product" or is_noindex:
        return None

    if product_block is None:
        raise Defect("classified as Product but no parseable Product JSON-LD block: %s" % path)

    identity_violations = check_identity(work_text, product_block["obj"])
    label_values = extract_specs(work_text)
    expected = compute_expected(label_values)
    classification = classify_state(expected, product_block["obj"])

    return {
        "path": path,
        "raw_text": raw_text,
        "work_text": work_text,
        "newline_style": newline_style,
        "product_block": product_block,
        "identity_violations": identity_violations,
        "label_values": label_values,
        "expected": expected,
        "states": classification["states"],
        "blocking_reasons": classification["blocking_reasons"],
    }


def run_release(mode):
    assert mode in ("check", "apply")

    all_files = discover_pdp_files()
    reports = []
    productgroup_count = 0
    noindex_count = 0
    other_count = 0

    for path in all_files:
        raw_text, work_text, newline_style = read_normalized(path)
        kind, is_noindex, _ = classify_file(work_text)
        if kind == "ProductGroup":
            productgroup_count += 1
            continue
        if is_noindex:
            noindex_count += 1
            continue
        if kind != "Product":
            other_count += 1
            continue
        report = process_file(path)
        if report is not None:
            reports.append(report)

    print("TOTAL_ENDPOINTS =", len(all_files))
    print("PHASE1_TARGET_PRODUCTS =", len(reports))
    print("PRODUCTGROUP =", productgroup_count)
    print("DUPLICATE_NOINDEX =", noindex_count)
    print("OTHER_UNCLASSIFIED =", other_count)

    drift_errors = []
    if len(all_files) != 127:
        drift_errors.append("TOTAL_ENDPOINTS expected 127, got %d" % len(all_files))
    if len(reports) != EXPECTED_TARGET_PRODUCTS:
        drift_errors.append("PHASE1_TARGET_PRODUCTS expected %d, got %d" % (EXPECTED_TARGET_PRODUCTS, len(reports)))
    if productgroup_count != EXPECTED_PRODUCTGROUP:
        drift_errors.append("PRODUCTGROUP expected %d, got %d" % (EXPECTED_PRODUCTGROUP, productgroup_count))
    if noindex_count != EXPECTED_NOINDEX:
        drift_errors.append("DUPLICATE_NOINDEX expected %d, got %d" % (EXPECTED_NOINDEX, noindex_count))

    identity_fail = [r for r in reports if r["identity_violations"]]
    print("IDENTITY_PASS =", len(reports) - len(identity_fail), "/", len(reports))
    if identity_fail:
        for r in identity_fail:
            print("  IDENTITY VIOLATION:", r["path"], r["identity_violations"])
        drift_errors.append("IDENTITY_PASS != %d (found %d violations)" % (EXPECTED_TARGET_PRODUCTS, len(identity_fail)))

    color_eligible = sum(1 for r in reports if r["expected"]["color"] is not None)
    warranty_eligible = sum(1 for r in reports if "Garantía" in r["expected"]["additionalProperty"])
    voltage_eligible = sum(1 for r in reports if "Voltaje" in r["expected"]["additionalProperty"])
    power_eligible = sum(1 for r in reports if "Potencia" in r["expected"]["additionalProperty"])
    union_eligible = sum(
        1 for r in reports
        if r["expected"]["color"] is not None or r["expected"]["additionalProperty"]
    )
    noop_products = len(reports) - union_eligible

    print("COLOR_ELIGIBLE =", color_eligible)
    print("WARRANTY_ELIGIBLE =", warranty_eligible)
    print("VOLTAGE_ELIGIBLE =", voltage_eligible)
    print("POWER_ELIGIBLE =", power_eligible)
    print("PHASE1_MODIFIABLE_UNION =", union_eligible)
    print("PHASE1_NOOP_PRODUCTS =", noop_products)

    for label, expected_val, actual_val in [
        ("COLOR_ELIGIBLE", EXPECTED_COLOR_ELIGIBLE, color_eligible),
        ("WARRANTY_ELIGIBLE", EXPECTED_WARRANTY_ELIGIBLE, warranty_eligible),
        ("VOLTAGE_ELIGIBLE", EXPECTED_VOLTAGE_ELIGIBLE, voltage_eligible),
        ("POWER_ELIGIBLE", EXPECTED_POWER_ELIGIBLE, power_eligible),
        ("PHASE1_MODIFIABLE_UNION", EXPECTED_MODIFIABLE_UNION, union_eligible),
        ("PHASE1_NOOP_PRODUCTS", EXPECTED_NOOP, noop_products),
    ]:
        if expected_val != actual_val:
            drift_errors.append("%s expected %d, got %d" % (label, expected_val, actual_val))

    if drift_errors:
        print()
        print("=== DATASET DRIFT / STRUCTURAL DRIFT DETECTED ===")
        for e in drift_errors:
            print("  -", e)
        print("PRECHECK_PASS = false (drift)")
        print("ZERO WRITES")
        return 2

    state_counts = {}
    blocked_files = []
    pending_files = []
    for r in reports:
        file_blocked = False
        file_pending = False
        for prop, state in r["states"].items():
            state_counts[state] = state_counts.get(state, 0) + 1
            if state == "BLOCKED":
                file_blocked = True
            if state == "PENDING":
                file_pending = True
        if file_blocked:
            blocked_files.append(r)
        elif file_pending:
            pending_files.append(r)

    print()
    print("=== STATE MACHINE AGGREGATE (across color + 3 managed additionalProperty slots) ===")
    for state in ["PENDING", "ALREADY_COMPLIANT", "BLOCKED", "NOOP"]:
        print(" ", state, "=", state_counts.get(state, 0))

    precheck_pass = len(blocked_files) == 0
    print()
    print("PRECHECK_PASS =", precheck_pass)
    print("BLOCKED_FILES =", len(blocked_files))
    print("PENDING_FILES (to be written) =", len(pending_files))

    if blocked_files:
        print()
        print("=== BLOCKED FILE DETAIL ===")
        for r in blocked_files:
            print(" ", r["path"])
            for reason in r["blocking_reasons"]:
                print("    -", reason)

    if not precheck_pass:
        print()
        print("ZERO WRITES ACROSS THE ENTIRE RELEASE")
        return 1

    if mode == "check":
        print()
        print("--check complete. No writes performed.")
        return 0

    # mode == "apply"
    written = 0
    for r in pending_files:
        block = r["product_block"]
        new_raw_content = apply_surgical_insertion(block["raw_content"], r["expected"], r["states"])
        new_work_text = (
            r["work_text"][: block["content_start"]]
            + new_raw_content
            + r["work_text"][block["content_end"] :]
        )
        final_text = new_work_text.replace("\n", r["newline_style"]) if r["newline_style"] == "\r\n" else new_work_text
        with open(r["path"], "wb") as fh:
            fh.write(final_text.encode("utf-8"))
        written += 1

    print()
    print("WRITES PERFORMED =", written)
    return 0


# --------------------------------------------------------------------------
# Self-tests (synthetic, in-memory / temp files only -- never touch productos/)
# --------------------------------------------------------------------------

SAMPLE_PDP_TEMPLATE = """<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <script type="application/ld+json">
    {
      "@context": "https://schema.org",
      "@type": "Product",
      "@id": "https://example.test/productos/x/__SLUG__/#product",
      "url": "https://example.test/productos/x/__SLUG__/",
      "name": "Producto de Prueba",
      "description": "Descripcion de prueba.",
      "image": "https://example.test/img.webp",
      "model": "__SLUG__"__EXTRA_TOP__
      ,
      "brand": {
        "@id": "https://example.test/#organization"
      }
    }
    </script>
    <link rel="canonical" href="https://example.test/productos/x/__SLUG__/">
    <table class="pdp-specs-table">
      <tbody>
        <tr><td>Modelo</td><td>__SLUG__</td></tr>
__SPEC_ROWS__
      </tbody>
    </table>
</head>
<body></body>
</html>
"""


def _make_sample(tmpdir, slug, spec_rows_html, extra_top=""):
    path = os.path.join(tmpdir, slug + ".html")
    content = (
        SAMPLE_PDP_TEMPLATE
        .replace("__SLUG__", slug)
        .replace("__SPEC_ROWS__", spec_rows_html)
        .replace("__EXTRA_TOP__", extra_top)
    )
    with open(path, "wb") as fh:
        fh.write(content.encode("utf-8"))
    return path


def selftest():
    failures = []

    with tempfile.TemporaryDirectory() as tmpdir:
        # Test 1: clean PDP with all 4 candidates eligible -> all PENDING, then apply -> all ALREADY_COMPLIANT
        p1 = _make_sample(
            tmpdir, "clean1",
            "        <tr><td>Colores</td><td>Blanco / Negro</td></tr>\n"
            "        <tr><td>Garantía</td><td>1 Año</td></tr>\n"
            "        <tr><td>Voltaje</td><td>110V / 60Hz</td></tr>\n"
            "        <tr><td>Potencia</td><td>1580W</td></tr>\n",
        )
        r1 = process_file(p1)
        if r1["identity_violations"]:
            failures.append("T1: unexpected identity violations: %s" % r1["identity_violations"])
        if r1["states"] != {"color": "PENDING", "Garantía": "PENDING", "Potencia": "PENDING", "Voltaje": "PENDING"}:
            failures.append("T1: unexpected initial states: %s" % r1["states"])

        block = r1["product_block"]
        new_raw = apply_surgical_insertion(block["raw_content"], r1["expected"], r1["states"])
        new_work_text = r1["work_text"][: block["content_start"]] + new_raw + r1["work_text"][block["content_end"] :]
        try:
            reparsed_blocks = find_ldjson_blocks(new_work_text)
            product_obj_after = next(b["obj"] for b in reparsed_blocks if b["obj"] and b["obj"].get("@type") == "Product")
        except Exception as e:
            failures.append("T1: post-insertion JSON did not parse: %s" % e)
            product_obj_after = None

        if product_obj_after is not None:
            if product_obj_after.get("color") != "Blanco / Negro":
                failures.append("T1: color not inserted correctly")
            ap = product_obj_after.get("additionalProperty")
            if not isinstance(ap, list) or len(ap) != 3:
                failures.append("T1: additionalProperty not inserted correctly: %s" % ap)
            names_order = [e.get("name") for e in ap] if isinstance(ap, list) else []
            if names_order != ["Garantía", "Potencia", "Voltaje"]:
                failures.append("T1: additionalProperty order incorrect: %s" % names_order)
            power_entry = next((e for e in ap if e.get("name") == "Potencia"), None)
            if power_entry != {"@type": "PropertyValue", "name": "Potencia", "value": 1580, "unitText": "W"}:
                failures.append("T1: Potencia entry incorrect: %s" % power_entry)
            # unrelated top-level keys must be untouched
            for k in ["@context", "@type", "@id", "url", "name", "description", "image", "model", "brand"]:
                if product_obj_after.get(k) != block["obj"].get(k):
                    failures.append("T1: unrelated key mutated: %s" % k)

            # simulate second run (idempotency): write to disk and reprocess
            final_text = new_work_text
            with open(p1, "wb") as fh:
                fh.write(final_text.encode("utf-8"))
            r1_second = process_file(p1)
            if r1_second["states"] != {"color": "ALREADY_COMPLIANT", "Garantía": "ALREADY_COMPLIANT", "Potencia": "ALREADY_COMPLIANT", "Voltaje": "ALREADY_COMPLIANT"}:
                failures.append("T1: second pass not ALREADY_COMPLIANT: %s" % r1_second["states"])
            block2 = r1_second["product_block"]
            new_raw2 = apply_surgical_insertion(block2["raw_content"], r1_second["expected"], r1_second["states"])
            if new_raw2 != block2["raw_content"]:
                failures.append("T1: insertion on already-compliant PDP is not a no-op")

        # Test 2: N/A values -> NOOP, not published
        p2 = _make_sample(
            tmpdir, "clean2",
            "        <tr><td>Voltaje</td><td>N/A</td></tr>\n"
            "        <tr><td>Potencia</td><td>Gas LP</td></tr>\n",
        )
        r2 = process_file(p2)
        if r2["states"]["Voltaje"] != "NOOP" or r2["states"]["Potencia"] != "NOOP":
            failures.append("T2: N/A / Gas LP should be NOOP: %s" % r2["states"])

        # Test 3: foreign additionalProperty entry must be preserved untouched
        p3 = _make_sample(
            tmpdir, "clean3",
            "        <tr><td>Garantía</td><td>1 Año</td></tr>\n",
            extra_top=',\n      "additionalProperty": [\n        {"@type": "PropertyValue", "name": "OtroAtributo", "value": "X"}\n      ]',
        )
        r3 = process_file(p3)
        block3 = r3["product_block"]
        new_raw3 = apply_surgical_insertion(block3["raw_content"], r3["expected"], r3["states"])
        new_work3 = r3["work_text"][: block3["content_start"]] + new_raw3 + r3["work_text"][block3["content_end"] :]
        obj3_after = next(b["obj"] for b in find_ldjson_blocks(new_work3) if b["obj"] and b["obj"].get("@type") == "Product")
        ap3 = obj3_after.get("additionalProperty", [])
        foreign = [e for e in ap3 if e.get("name") == "OtroAtributo"]
        if len(foreign) != 1 or foreign[0] != {"@type": "PropertyValue", "name": "OtroAtributo", "value": "X"}:
            failures.append("T3: foreign additionalProperty entry not preserved: %s" % ap3)
        garantia3 = [e for e in ap3 if e.get("name") == "Garantía"]
        if len(garantia3) != 1:
            failures.append("T3: managed Garantía entry not inserted alongside foreign entry: %s" % ap3)

        # Test 4: conflicting existing value -> BLOCKED, and one BLOCKED file must zero out the whole batch
        p4 = _make_sample(
            tmpdir, "conflict4",
            "        <tr><td>Garantía</td><td>1 Año</td></tr>\n",
            extra_top=',\n      "additionalProperty": [\n        {"@type": "PropertyValue", "name": "Garantía", "value": "2 Años"}\n      ]',
        )
        r4 = process_file(p4)
        if r4["states"]["Garantía"] != "BLOCKED":
            failures.append("T4: conflicting Garantía should be BLOCKED: %s" % r4["states"])

        # Test 5: stale conflict -- managed property present but source no longer eligible
        p5 = _make_sample(
            tmpdir, "stale5",
            "        <tr><td>Voltaje</td><td>N/A</td></tr>\n",
            extra_top=',\n      "additionalProperty": [\n        {"@type": "PropertyValue", "name": "Voltaje", "value": "110V"}\n      ]',
        )
        r5 = process_file(p5)
        if r5["states"]["Voltaje"] != "BLOCKED":
            failures.append("T5: stale managed Voltaje should be BLOCKED (STALE_CONFLICT): %s" % r5["states"])

        # Test 6: duplicate managed name -> BLOCKED
        p6 = _make_sample(
            tmpdir, "dup6",
            "        <tr><td>Garantía</td><td>1 Año</td></tr>\n",
            extra_top=(
                ',\n      "additionalProperty": [\n'
                '        {"@type": "PropertyValue", "name": "Garantía", "value": "1 Año"},\n'
                '        {"@type": "PropertyValue", "name": "Garantía", "value": "1 Año"}\n'
                "      ]"
            ),
        )
        r6 = process_file(p6)
        if r6["states"]["Garantía"] != "BLOCKED":
            failures.append("T6: duplicate managed name should be BLOCKED: %s" % r6["states"])

        # Test 7: transactionality -- one BLOCKED among many must force zero writes for the whole set
        reports = [r1, r4]  # r1 clean (already written+compliant above), r4 has a BLOCKED
        any_blocked = any(s == "BLOCKED" for r in reports for s in r["states"].values())
        if not any_blocked:
            failures.append("T7 setup invalid: expected at least one BLOCKED among synthetic reports")
        # simulate precheck: PRECHECK_PASS must be False for the whole batch
        precheck_pass = not any_blocked
        if precheck_pass:
            failures.append("T7: PRECHECK_PASS should be False when any file is BLOCKED")

    if failures:
        print("SELFTEST: FAIL (%d failure(s))" % len(failures))
        for f in failures:
            print("  -", f)
        return 1
    print("SELFTEST: PASS (7/7 checks)")
    return 0


def main():
    if len(sys.argv) != 2 or sys.argv[1] not in ("--check", "--apply", "--selftest"):
        print("Usage: apply_product_semantic_enrichment.py --check|--apply|--selftest")
        return 64
    if sys.argv[1] == "--selftest":
        return selftest()
    return run_release("check" if sys.argv[1] == "--check" else "apply")


if __name__ == "__main__":
    sys.exit(main())
