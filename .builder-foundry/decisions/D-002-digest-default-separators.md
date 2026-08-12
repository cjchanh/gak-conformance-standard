# D-002 — Digest uses Python default JSON separators

- **Date:** 2026-08-12
- **Wave:** baseline
- **Status:** accepted
- **Author lane:** lead (session 1)

## Decision

`clauses_digest` is SHA-256 of UTF-8 `json.dumps(body, sort_keys=True)` with
**default** separators `', '` and `': '` (a space after each). This is spec
§5.3 verbatim.

## Measurement

From `v1/evidence/deponent-conformance-receipt.json`:

| Encoding | SHA-256 | Matches published `de6b7089…` |
|---|---|---|
| `json.dumps(obj, sort_keys=True)` | `de6b7089f894e009a6d1a1dba8c9b32b26e38daf803b07b83ec0958ff64c5406` | yes |
| `separators=(',', ':')` | `65f40400dbaa6145afacdf5cd1de979c83150be6cfbab8d038ec0dacb14b2733` | **no** |

Same algorithm also re-derives v1.1 Deponent `cf26befe…` and sworncode
`e65dd28b…`.

## Rejected

- RFC 8785 JCS (not what published receipts used).
- Compact separators (common "canonical JSON" advice; **breaks the standard**).

Evidence: `.builder-foundry/evidence/digest-separator-experiment.json`
