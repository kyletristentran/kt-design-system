#!/usr/bin/env python3
"""
render_memo.py — memo spec (JSON) -> corporate memo PDF.

    python render_memo.py memo.json -o memo.pdf [--html-out memo.html] [--keep-html]

Second deterministic half of the kt-corporate-memo pipeline.

The contract that makes this skill worth using: prose never contains a typed
number. It contains [[token]] references into `figures`, each of which carries the
A1 cell it came from. This script substitutes the formatted value, stamps a
superscript trace mark, and builds the appendix index. verify_memo.py then proves
each one still matches the workbook.
"""
import argparse, json, os, re, sys
from pathlib import Path
from jinja2 import Environment, FileSystemLoader, select_autoescape
from markupsafe import Markup, escape

TOKEN = re.compile(r'\[\[([A-Za-z0-9_.\-]+)\]\]')
HERE = Path(__file__).resolve().parent


# ---------------------------------------------------------------- formatting
def fmt(value, kind="number", display=None, decimals=None):
    """
    `decimals` forces a fixed precision. A rate column that renders $22 beside
    $20.50 reads as an error, so any column whose values share a unit should
    pin it rather than let each cell decide.
    """
    if display is not None:
        return str(display)
    if value is None:
        return "—"
    if isinstance(value, str):
        return value
    v = float(value)
    if kind == "currency":
        neg = v < 0
        a = abs(v)
        if decimals is not None:
            s = f"${a:,.{decimals}f}"
        else:
            s = f"${a:,.2f}" if 0 < a < 1000 and a != int(a) else f"${a:,.0f}"
        return f"({s})" if neg else s
    if kind == "percent":
        return f"{v * 100:,.{1 if decimals is None else decimals}f}%"
    if kind == "multiple":
        return f"{v:,.2f}x"
    if kind == "date":
        return str(value)
    if v == int(v):
        return f"{int(v):,}"
    return f"{v:,.2f}"


class Tracer:
    """Assigns stable superscript marks to unique source cells."""

    def __init__(self):
        self.order, self.seen = [], {}

    def mark(self, trace, label, value_str):
        if not trace:
            return ""
        if trace not in self.seen:
            self.seen[trace] = len(self.order) + 1
            self.order.append({"mark": len(self.order) + 1, "trace": trace,
                               "label": label, "value": value_str})
        return self.seen[trace]

    def index(self):
        return self.order


def substitute(text, figures, tracer, show_marks=True):
    """Escape prose, then swap [[token]] for a formatted, traced figure."""
    out, missing = [], []
    pos = 0
    raw = str(text)
    for m in TOKEN.finditer(raw):
        out.append(str(escape(raw[pos:m.start()])))
        key = m.group(1)
        f = figures.get(key)
        if not f:
            missing.append(key)
            out.append(f'<span style="background:#ffe0e0">[[{escape(key)}]]</span>')
        else:
            s = fmt(f.get("value"), f.get("kind", "number"), f.get("display"))
            n = tracer.mark(f.get("trace"), f.get("label", key), s)
            # .fig keeps prose in the body serif with tabular figures; mono is for
            # tables and tiles, where columns must align, not for running text.
            out.append(f'<span class="fig">{escape(s)}</span>'
                       + (f'<span class="trace">{n}</span>' if n and show_marks else ""))
        pos = m.end()
    out.append(str(escape(raw[pos:])))
    return Markup("".join(out)), missing


# ---------------------------------------------------------------- exhibits
def _cellclass(kind):
    return "n" if kind in ("currency", "percent", "number", "multiple") else ""


def _sched_cell(v, kind, decimals=None):
    """A schedule cell: number formatted and signed, or a literal like 'N/A'."""
    if v is None or v == "":
        return "", ""
    if isinstance(v, str):
        return escape(v), ""
    if isinstance(v, bool):
        return escape(str(v)), ""
    # A bare "0" is right in a count column and wrong in a currency column, where
    # it has to match the unit its neighbours carry.
    if v == 0 and kind == "number":
        return "0", ""
    return escape(fmt(v, kind, decimals=decimals)), " neg" if v < 0 else ""


def build_schedule(ex):
    """
    The ARGUS report shape — label column, right-aligned value columns, blocks
    with subtotals. Drives both a 13-period tenant cash flow and a two-column
    market-leasing comparison; the only difference is how many columns and
    whether the values are numbers or literals.

    Row `kind`: detail (default) | sub | net | grp | spacer | dtl | dtlhdr
    """
    cols = ex.get("periods", [])
    total_label = ex.get("total_label")
    kind_default = ex.get("value_kind", "number")
    wide = len(cols) + (1 if total_label else 0) > 8

    head = (f'<th class="lab">{escape(ex.get("stub", ""))}</th>'
            + "".join(f"<th>{escape(str(c))}</th>" for c in cols)
            + (f'<th class="tot">{escape(total_label)}</th>' if total_label else ""))

    body, z = [], False
    for g in ex.get("groups", []):
        if g.get("label"):
            span = len(cols) + (2 if total_label else 1)
            body.append(f'<tr class="grp"><td class="lab" colspan="{span}">'
                        f'{escape(g["label"])}</td></tr>')
        for r in g.get("rows", []):
            k = r.get("kind", "detail")
            if k == "spacer":
                body.append('<tr class="spacer"><td></td></tr>')
                continue
            rk = r.get("value_kind", kind_default)
            dp = r.get("decimals", ex.get("decimals"))
            vals = list(r.get("values", []))
            vals += [None] * (len(cols) - len(vals))
            tds = []
            for v in vals[:len(cols)]:
                txt, cls = _sched_cell(v, rk, dp)
                tds.append(f'<td class="{cls.strip()}">{txt}</td>')
            if total_label:
                txt, cls = _sched_cell(r.get("total"), rk, dp)
                tds.append(f'<td class="tot{cls}">{txt}</td>')
            z = not z if k == "detail" else z
            cls = f"{k}{' zebra' if k == 'detail' and z else ''}"
            body.append(f'<tr class="{cls}"><td class="lab">{escape(r.get("label",""))}</td>'
                        f'{"".join(tds)}</tr>')

    lines = "<br>".join(escape(l) for l in ex.get("meta_lines", []))
    note = f'<div class="sched-note">{escape(ex["note"])}</div>' if ex.get("note") else ""
    src = (f'<span class="src" style="float:right">{escape(ex["source"])}</span>'
           if ex.get("source") else "")
    block = (
        f'<div class="sched-head">{src}<div class="ttl">'
        f'<span class="id">Exhibit {escape(ex.get("id",""))}</span> · '
        f'{escape(ex.get("title",""))}</div>'
        + (f'<div class="lines">{lines}</div>' if lines else "") + '</div>'
        # A two- or three-column schedule stretched to full width leaves a canyon
        # between label and value; narrow it so the eye can track the row.
        f'<table class="sched{"" if len(cols) > 4 else " narrow"}">'
        f'<thead><tr>{head}</tr></thead>'
        f'<tbody>{"".join(body)}</tbody></table>{note}')
    return Markup(f'<div class="sched-page">{block}</div>' if wide
                  else f'<div class="exhibit">{block}</div>')


def build_exhibit(ex):
    """Exhibit -> HTML: caption, data table, optional CSS bar chart, note."""
    if ex.get("type") == "schedule":
        return build_schedule(ex)
    cols = ex.get("columns", [])
    kinds = ex.get("column_kinds") or ["text"] + ["number"] * (len(cols) - 1)
    kinds = (kinds + ["text"] * len(cols))[:len(cols)]
    total_rows = {int(i) for i in ex.get("total_rows", [])}

    head = "".join(
        f'<th class="{_cellclass(k)}">{escape(c)}</th>' for c, k in zip(cols, kinds))
    body = []
    for ri, row in enumerate(ex.get("rows", [])):
        cls = ' class="total"' if ri in total_rows else ""
        tds = []
        for ci, cell in enumerate(row):
            k = kinds[ci] if ci < len(kinds) else "text"
            if isinstance(cell, (int, float)) and not isinstance(cell, bool):
                neg = " neg" if cell < 0 else ""
                tds.append(f'<td class="n{neg}">{escape(fmt(cell, k))}</td>')
            else:
                tds.append(f'<td class="{_cellclass(k)}">'
                           f'{escape("—" if cell in (None, "") else cell)}</td>')
        body.append(f"<tr{cls}>{''.join(tds)}</tr>")

    chart = ""
    ch = ex.get("chart")
    if ch:
        li, vi = int(ch.get("label_col", 0)), int(ch.get("value_col", 1))
        pts = [(r[li], r[vi]) for ri, r in enumerate(ex.get("rows", []))
               if ri not in total_rows and len(r) > max(li, vi)
               and isinstance(r[vi], (int, float)) and not isinstance(r[vi], bool)]
        if pts:
            hi = max(abs(v) for _, v in pts) or 1
            k = kinds[vi] if vi < len(kinds) else "number"
            rows = "".join(
                f'<div class="row"><div class="lab">{escape(str(l))}</div>'
                f'<div class="track"><div class="fill" style="width:{abs(v)/hi*100:.1f}%"></div></div>'
                f'<div class="val">{escape(fmt(v, k))}</div></div>'
                for l, v in pts)
            col = escape(cols[vi]) if vi < len(cols) else ""
            src = escape(ex.get("source", "")) or "the source workbook"
            chart = (f'<div class="bars">{rows}'
                     f'<div class="srcline">{col} · source: {src}</div></div>')

    note = f'<div class="note">{escape(ex["note"])}</div>' if ex.get("note") else ""
    src = f'<span class="src">{escape(ex["source"])}</span>' if ex.get("source") else ""
    # thead/tbody rather than bare rows: Chromium repeats a table-header-group on
    # every page a table spans, which is what the document rules require of a
    # table that breaks. Without it the continuation page has unlabelled columns.
    return Markup(
        f'<div class="exhibit"><div class="cap">'
        f'<span class="t"><span class="id">Exhibit {escape(ex.get("id", ""))}</span> · '
        f'{escape(ex.get("title", ""))}</span>{src}</div>'
        f'<table class="data"><thead><tr>{head}</tr></thead>'
        f'<tbody>{"".join(body)}</tbody></table>{chart}{note}</div>')


# ---------------------------------------------------------------- render
def render_html(spec, show_marks=None):
    figures = spec.get("figures", {})
    tracer = Tracer()
    missing = []

    # Superscript trace marks are off by default. The type floor puts them at 9pt,
    # which peppers running prose; the appendix already carries the full audit
    # trail. Turn them on for an audit copy ("trace_marks": true, or --marks).
    if show_marks is None:
        show_marks = bool(spec.get("trace_marks", False))

    def sub(t):
        html, miss = substitute(t, figures, tracer, show_marks=show_marks)
        missing.extend(miss)
        return html

    # Order matters: trace marks are assigned on first substitution, so they must be
    # generated in reading order (BLUF -> tiles -> ask -> sections), not code order.
    bluf = sub(spec.get("bluf", "")) if spec.get("bluf") else ""

    kpis = []
    for k in spec.get("kpis", []):
        f = figures.get(k.get("token"), {})
        s = fmt(f.get("value"), f.get("kind", "number"), f.get("display"))
        tracer.mark(f.get("trace"), f.get("label", k.get("label", "")), s)
        kpis.append({"label": k.get("label", f.get("label", "")), "value": s})

    ask = spec.get("ask")
    if ask:
        ask = dict(ask)
        ask["action"] = sub(ask.get("action", ""))
        if ask.get("amount_token"):
            f = figures.get(ask["amount_token"], {})
            ask["amount"] = fmt(f.get("value"), f.get("kind", "currency"), f.get("display"))

    ex_by_id = {e.get("id"): e for e in spec.get("exhibits", [])}
    placed = set()

    sections = []
    for i, s in enumerate(spec.get("sections", []), start=1):
        ids = s.get("exhibits", [])
        placed.update(ids)
        sections.append({
            "n": f"{i:02d}",
            "heading": s.get("heading", ""),
            "paragraphs": [sub(p) for p in s.get("paragraphs", [])],
            "bullets": [sub(b) for b in s.get("bullets", [])],
            "exhibits": [build_exhibit(ex_by_id[x]) for x in ids if x in ex_by_id],
        })

    # Identity defaults come from the KT CRE brand.json identity block, so a spec
    # that omits them still renders a complete letterhead.
    meta = {"org": "KTFORD", "mark": "KT", "doc_class": "Internal memorandum",
            "address_line1": "1801 Century Park East, Suite 1400",
            "address_line2": "Los Angeles, CA 90067", "web": "ktford.com",
            "confidentiality": "Confidential — internal distribution only",
            "classification": "Privileged and confidential",
            "ref": "", "to": "", "from": "", "date": "", "re": ""}
    meta.update(spec.get("meta", {}))

    ctx = {
        "meta": meta,
        "source_file": spec.get("source_file", "the source workbook"),
        "bluf": bluf,
        "kpis": kpis,
        "ask": ask,
        "sections": sections,
        "risks": [{"risk": sub(r.get("risk", "")), "response": sub(r.get("response", ""))}
                  for r in spec.get("risks", [])],
        "reconciliation": [{"issue": sub(r.get("issue", "")), "detail": sub(r.get("detail", ""))}
                           for r in spec.get("reconciliation", [])],
        "loose_exhibits": [build_exhibit(e) for e in spec.get("exhibits", [])
                           if e.get("id") not in placed],
        "attest": spec.get("attest", []),
        "traces": tracer.index(),
    }

    env = Environment(loader=FileSystemLoader(str(HERE)),
                      autoescape=select_autoescape(["html"]))
    return env.get_template("memo_template.html").render(**ctx), sorted(set(missing))


# The repeating page frame. Chromium ignores CSS margin-box content and does not
# repeat position:fixed elements in print, so the full-bleed band and the footer
# rule have to live in these templates. Styles must be inline — the templates do
# not see the document's stylesheet — and colour needs print-color-adjust:exact.
HEADER = """<div style="-webkit-print-color-adjust:exact;print-color-adjust:exact;
 margin:0;padding:0;width:100%;">
 <div style="background:{ink};color:#FFFFFF;width:100%;height:34px;line-height:34px;
  text-align:center;font-family:'Segoe UI',Arial,sans-serif;font-size:8.5px;
  letter-spacing:1.3px;">{band}</div></div>"""

FOOTER = """<div style="-webkit-print-color-adjust:exact;print-color-adjust:exact;
 width:100%;padding:0 0.75in;font-family:'Segoe UI',Arial,sans-serif;font-size:8px;
 color:{label};">
 <div style="border-top:1px solid {border};padding-top:5px;">
  <span style="float:left;">{left}</span>
  <span style="float:right;">Page <span class="pageNumber"></span> of
   <span class="totalPages"></span></span>
 </div></div>"""

INK, LABEL, BORDER = "#242424", "#707070", "#E0E0E0"


def to_pdf(html_path, pdf_path, band="", footer_left=""):
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page()
        pg.goto(Path(html_path).resolve().as_uri(), wait_until="networkidle")
        # prefer_css_page_size lets a wide schedule take a landscape page via the
        # named @page rule in memo.css while the memo body stays portrait.
        # Margins come from CSS in that mode, so they are not passed here.
        pg.pdf(path=pdf_path, print_background=True, prefer_css_page_size=True,
               display_header_footer=True,
               header_template=HEADER.format(ink=INK, band=escape(band)),
               footer_template=FOOTER.format(left=escape(footer_left),
                                             label=LABEL, border=BORDER))
        b.close()


def main():
    ap = argparse.ArgumentParser(description="Render a memo spec to PDF.")
    ap.add_argument("spec")
    ap.add_argument("-o", "--out", default="memo.pdf")
    ap.add_argument("--html-out", default=None)
    ap.add_argument("--keep-html", action="store_true")
    ap.add_argument("--marks", action="store_true",
                    help="audit copy: superscript trace marks beside every bound figure")
    a = ap.parse_args()

    spec = json.load(open(a.spec))
    html, missing = render_html(spec, show_marks=True if a.marks else None)

    html_path = a.html_out or str(HERE / "_memo_render.html")
    Path(html_path).write_text(html, encoding="utf-8")

    meta = {"doc_class": "Internal memorandum",
            "confidentiality": "Confidential — internal distribution only"}
    meta.update(spec.get("meta", {}))
    to_pdf(html_path, a.out,
           band=f"{meta.get('doc_class', 'Memorandum')} — {meta.get('re', '')}".strip(" —"),
           footer_left=f"{meta.get('confidentiality', '')}"
                       f"{'  ·  ' + meta['ref'] if meta.get('ref') else ''}")

    if not (a.keep_html or a.html_out):
        os.remove(html_path)

    print(f"wrote {a.out}")
    if missing:
        print("! unresolved figure tokens: " + ", ".join(missing), file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
