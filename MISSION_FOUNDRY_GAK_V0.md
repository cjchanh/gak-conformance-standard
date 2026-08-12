# Mission — GAK v0 (standard)

## Objective
Ship **GAK v0** as a *runnable* conformance product in this repo: a **vendor-neutral mechanical scorer**, a **JSON conformance receipt**, **one kernel scored** (Deponent first, as a scored kernel — not the owner), and a **public-safe leave-behind**.

This is the first *product* marathon after Foundry 1.1.0 + session-testify. It is **not** a rename. It is **not** a Deponent PyPI / visibility flip (that campaign is an alternate; do not launch it).

PS-05 (North Star): GAK is named; `v1/spec.md` already drafts the 13 clauses + receipt/adapter contract. **Third-party scores: 0.** Close the gap from “spec + self-score evidence” to “a stranger can run a score command and get a receipt.”

## Stack role
- **Layer:** Category standard + harness (executable mark, not a kernel)
- **In-repo (normative, already drafted):** `v1/spec.md` (`gak-conformance/v1`, 13 clauses); v1.1 amendment is optional/capability-gated — **v0 ships the frozen v1 clause set**
- **First kernel (read-only sibling):** Deponent — score via the §6 adapter; do not own, rewrite, or publish it
- **Not:** session-testify, Foundry kit, Assurance UI, Deponent public flip, attest/compliance coupling

Writable root = `~/Workspace/active/gak-conformance-standard` only.

## Product
A third party must be able to score a kernel **without importing Deponent internals**.

1. **Mechanical scorer** lives in *this* repo (not `from deponent.conformance import …` as the harness). Today `scripts/check_consistency.py` imports `deponent.badge` / `deponent.conformance` — that coupling is a defect to close.
2. **Third-party-runnable score command** (name is an implementation detail; one documented entrypoint), e.g.:
   ```text
   python3 -m gak_conformance score --adapter <module:Class> [--out receipt.json]
   ```
   Offline `--help` / selfcheck with a fixture adapter (no Deponent required).
3. **JSON receipt** per spec §5.1 (`gak-conformance/v1`): `kernel`, `profile`, `conformant`, `counts`, all 13 `clauses` with `id` / `profile` / `status` / `detail`. No timestamp. Digest per §5.3. Fail-closed exits (0 = conformant; nonzero otherwise).
4. **Deponent scored** against the **v1** 13 clauses via a real adapter (not a simulation). Refresh or replace `v1/evidence/` only if a live run justifies it. Do not treat author self-scores as a third-party verdict.
5. **Public-safe leave-behind:** spec + harness + adapter contract + receipt schema + one scored-kernel evidence pack + README that says how a stranger scores *their* kernel. Face: *research prototype, not a security-evaluated product.* Bounded mark language (spec §8).

## Acceptance
- Third party: clone this repo → documented score command → JSON receipt (no Deponent install required for the fixture / their adapter)
- Deponent (when present locally) scored against **v1 clauses**; receipt `conformant` matches §3.4 (no FAIL; ≥1 PASS)
- Receipt is re-derivable (two runs, same digest) when the kernel is unchanged
- **No `attest.py` / private coupling leak** in the leave-behind: no `deponent/attest.py`, `00Agent`, `cds-compliance`, CMMC-RMF coverage maps, ATO-in-a-Box, per-control maps
- No import of Deponent private modules as the harness; adapter boundary only
- `foundry_guard` green; local commits only; **no push / publish / PyPI / GitHub visibility change**
- STRUCTURAL guard quotas ≠ semantic quality narration

## Exclusions
- Do **not** invoke `foundry-campaign` or `run_grok_marathon.sh` from inside this mission authoring / a nested session (operator launches once)
- Do **not** start a second marathon if one is live — **dual-start refuse = exit 75** (inspect `foundry-campaign status --repo …`; never auto-rm a live/unknown pidfile)
- No Deponent visibility flip, rename, or PyPI publish
- No `OPERATOR COMMIT` send / publish / push / deploy / license
- No MoLA start/stop
- No network paid APIs, credentials, PR, or weakening Foundry guard quotas
- Do not rewrite Deponent unless a **contract bug** in the public adapter surface is proven (prefer adapter note)
- Do not claim third-party adoption; do not stretch the mark beyond the clause set

## Profile
`standard`

**Why (least-wrong):** GAK v0 is a vendor-neutral **standard + harness + leave-behind**, not a Python library/CLI identity. `library-cli` would lock the campaign to packaging/API/compatibility waves. `marathon` / `extreme` / `web-product` / `game` demand visual or product-shape evidence this category does not have. `standard` is the end-to-end product + independent-audit profile without a CLI or visual quota.

## Why this campaign (operator intent)
Foundry 1.1.0 and session-testify already closed. Next product brick: **make the category testable by someone who is not us.** Spec exists; 0 third-party scores. Ship the scorer they would run.

## Completion criterion
Only `foundry_guard.py --repo . --run-commands --write-report` exit 0 after profile minimum sessions — not a plan, scaffold, or self-score dump.

## Launch (operator only — DO NOT RUN from this file)

```bash
# foundry-campaign --repo ~/Workspace/active/gak-conformance-standard --mission /tmp/mission-gak-v0.md --profile standard
```

If a marathon is already live on this repo: **refuse (exit 75)**. Wait or `foundry-campaign status --repo ~/Workspace/active/gak-conformance-standard`.
