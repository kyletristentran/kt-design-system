# Attestation

The closing blocks: a signature-ruled "Prepared and reviewed" attestation and the appendix trace index that maps every figure to its source cell.

## Consumer provides
- `.kt-attest` with a `.kt-attest__grid` of signers, each a `.kt-attest__sig` line, `.kt-attest__nm` and `.kt-attest__cap` (role and date).
- `table.kt-trace` rows of mark, figure label, `Sheet!Cell` and value.

## Rules
- The trace index starts on its own page and lists every bound figure; the memo pipeline generates it and `verify_memo.py` checks each value against the workbook.
- Trace keys use `accent-deep` mono; values right-align in mono.
