#!/usr/bin/env python3
"""
verify_memo.py — prove the memo says what the workbook says.

    python verify_memo.py memo.json source.xlsx [--strict]

This is the gate that makes "no orphan numbers" a fact instead of a promise.
FAIL blocks delivery; WARN is a judgment call you must consciously accept.

Checks
  F1  every figure carries a resolvable Sheet!Cell trace          FAIL
  F2  every figure's value still matches its traced cell          FAIL
  F3  every [[token]] used in prose is defined in figures         FAIL
  F4  no bare numeric literal typed into prose (the orphan test)  FAIL
  S1  a BLUF exists and is <= 45 words                            FAIL
  S2  a decision/ask is present                                   WARN
  S3  every exhibit is cited by a section                         WARN
  S4  every defined figure is actually used                       WARN
  S5  hedging language in the BLUF                                WARN
"""
import argparse, json, re, sys
from openpyxl import load_workbook

TOKEN = re.compile(r'\[\[([A-Za-z0-9_.\-]+)\]\]')
# A bare figure typed into prose. Deliberately permits lone digits, so ordinals and
# spelled positions ("Year 1", "month six", "Years 1-3") read naturally; anything
# shaped like an actual measurement is caught.
LITERAL = re.compile(
    r'(?<![\w\[])('
    r'\$\s?\d[\d,]*(?:\.\d+)?'          # $340,000
    r'|\d[\d,]*(?:\.\d+)?\s?%'          # 62%
    r'|\d{1,3}(?:,\d{3})+(?:\.\d+)?'    # 1,234
    r'|\d+\.\d+'                        # 12.5
    r'|\d{2,}'                          # 19, 2026
    r')(?![\w\]])')
HEDGE = re.compile(r'\b(we believe|it appears|it seems|may possibly|arguably|'
                   r'it should be noted|in our opinion|somewhat|fairly confident)\b', re.I)
TOL = 0.005


def prose_strings(spec):
    """(location, text) for every model-authored string that renders as prose."""
    out = []
    if spec.get("bluf"):
        out.append(("bluf", spec["bluf"]))
    if spec.get("ask", {}).get("action"):
        out.append(("ask.action", spec["ask"]["action"]))
    for i, s in enumerate(spec.get("sections", [])):
        for j, p in enumerate(s.get("paragraphs", [])):
            out.append((f"sections[{i}].paragraphs[{j}]", p))
        for j, b in enumerate(s.get("bullets", [])):
            out.append((f"sections[{i}].bullets[{j}]", b))
    for i, r in enumerate(spec.get("risks", [])):
        out.append((f"risks[{i}].risk", r.get("risk", "")))
        out.append((f"risks[{i}].response", r.get("response", "")))
    for i, r in enumerate(spec.get("reconciliation", [])):
        out.append((f"reconciliation[{i}].detail", r.get("detail", "")))
    return out


def resolve(wb, trace):
    if not trace or "!" not in trace:
        return None, "no Sheet!Cell trace"
    sheet, cell = trace.rsplit("!", 1)
    sheet = sheet.strip("'")
    if sheet not in wb.sheetnames:
        return None, f"sheet '{sheet}' not in workbook"
    try:
        return wb[sheet][cell].value, None
    except Exception as e:
        return None, f"bad reference ({e})"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("spec")
    ap.add_argument("xlsx")
    ap.add_argument("--strict", action="store_true", help="treat WARN as FAIL")
    a = ap.parse_args()

    spec = json.load(open(a.spec))
    wb = load_workbook(a.xlsx, data_only=True)
    figures = spec.get("figures", {})
    allow = set(str(x) for x in spec.get("allow_literals", []))

    fails, warns = [], []

    # F1 / F2 -------------------------------------------------------------
    for key, f in figures.items():
        val, err = resolve(wb, f.get("trace"))
        if err:
            fails.append(f"F1 [{key}] {err}")
            continue
        want, got = f.get("value"), val
        if isinstance(want, (int, float)) and isinstance(got, (int, float)):
            denom = max(abs(want), abs(got), 1e-9)
            if abs(want - got) / denom > TOL:
                fails.append(f"F2 [{key}] memo says {want}, {f['trace']} holds {got}")
        elif got is None:
            fails.append(f"F2 [{key}] {f['trace']} is empty "
                         f"(recalc the workbook if it holds a formula)")
        elif str(want).strip() != str(got).strip():
            fails.append(f"F2 [{key}] memo says {want!r}, {f['trace']} holds {got!r}")

    # F3 / F4 -------------------------------------------------------------
    used = set()
    for loc, text in prose_strings(spec):
        toks = TOKEN.findall(text)
        used.update(toks)
        for t in toks:
            if t not in figures:
                fails.append(f"F3 {loc}: [[{t}]] is not defined in figures")
        stripped = TOKEN.sub("", text)
        for lit in LITERAL.findall(stripped):
            if lit.strip() in allow:
                continue
            fails.append(f"F4 {loc}: bare literal {lit.strip()!r} — bind it to a "
                         f"figure token or add it to allow_literals")

    # S1 / S2 -------------------------------------------------------------
    bluf = spec.get("bluf", "").strip()
    if not bluf:
        fails.append("S1 no BLUF — a memo without a bottom line is a status report")
    else:
        n = len(TOKEN.sub("X", bluf).split())
        if n > 45:
            fails.append(f"S1 BLUF is {n} words; the ceiling is 45")
        if HEDGE.search(bluf):
            warns.append("S5 BLUF hedges — state the claim and own it")
    if not spec.get("ask", {}).get("action"):
        warns.append("S2 no decision requested — confirm this is informational by design")

    # S3 / S4 -------------------------------------------------------------
    cite_order = [x for s in spec.get("sections", []) for x in s.get("exhibits", [])]
    cited = set(cite_order)
    for e in spec.get("exhibits", []):
        if e.get("id") not in cited:
            warns.append(f"S3 Exhibit {e.get('id')} is never cited by a section")
    if cite_order != sorted(cite_order):
        warns.append(f"S6 exhibit labels do not ascend in citation order "
                     f"(reader meets them as {', '.join(cite_order)}) — relabel them")
    for k in figures:
        if k not in used and k not in {x.get("token") for x in spec.get("kpis", [])} \
                and k != spec.get("ask", {}).get("amount_token"):
            warns.append(f"S4 figure [{k}] is defined but never used")

    # report ---------------------------------------------------------------
    for f in fails:
        print(f"FAIL  {f}")
    for w in warns:
        print(f"WARN  {w}")
    ok = len(figures) - len([f for f in fails if f.startswith(("F1", "F2"))])
    print(f"\n{ok}/{len(figures)} figures tie to {a.xlsx} · "
          f"{len(fails)} failures, {len(warns)} warnings")

    if fails or (a.strict and warns):
        sys.exit(1)
    print("PASS")


if __name__ == "__main__":
    main()
