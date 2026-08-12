# Leave-behind scan — GAK v0

**Date:** 2026-08-12T18:35:00Z  
**Scope:** this repo only. Sibling Deponent peeked **names-only** (no private file copy).  
**Mode:** read-only. No fixes applied.

**Verdict:** no forbidden private-surface files in the product tree. Two S2 leave-behind defects: Deponent used as the live harness, and `.gitignore` does not keep campaign host-paths off `git add`.

---

## Forbidden-surface matrix

Mission forbids these in the public leave-behind. Checked by filename + content grep over the repo (including untracked campaign dirs).

| Forbidden | In GAK product tree | In untracked campaign / mission text | Notes |
|---|---|---|---|
| `deponent/attest.py` | **absent** | named only as a *forbid* in `MISSION_FOUNDRY_GAK_V0.md` | Sibling private tree **has** this name. GAK does not copy it. |
| `00Agent` | **absent** | same forbid-list only | Not a file or import here. |
| `cds-compliance` | **absent** | same forbid-list only | Not a file or import here. |
| CMMC-RMF coverage maps | **absent** | same forbid-list only | No control-ID tables, no coverage CSVs. |
| ATO-in-a-Box | **absent** | same forbid-list only | String not in spec/README/evidence. |
| per-control maps | **absent** | same forbid-list only | — |
| secrets / tokens / keys | **absent** | none | No `AKIA*`, `ghp_`, `sk-`, `xai-`, `BEGIN * PRIVATE KEY`. No `.env`. |
| `/Users/cj` personal paths | **absent from tracked product files** | **present in `.builder-foundry/`** | See S2 gitignore. |

Capability word `attest` in spec/README/receipts is the **public** GAK-ATTEST-HONEST clause, not the private sibling module.

`v1/spec.md` § v1.1 mentions NIST AU-family, GDPR Art. 5(1)(c), and classified-spillage as *motivation* for content-blind audit. That is not a CMMC/RMF per-control map.

---

## Tracked product tree (HEAD `e55b068`)

Inferred from working tree minus baseline porcelain `??` list.

| Path | Leave-behind role |
|---|---|
| `v1/spec.md` | normative standard |
| `v1/evidence/*` (12 files) | scored-kernel evidence |
| `README.md` | public face |
| `scripts/check_consistency.py` | only executable |
| `LICENSE`, `NOTICE`, `.gitignore` | legal + ignore |

Untracked (must not ship): `.builder-foundry/`, `.builder-foundry-kit/`, `.agents/`, `.claude/`, `.grok/`, `AGENTS.builder-foundry.md`, `MISSION_FOUNDRY_GAK_V0.md`.

Remote: `https://github.com/cjchanh/gak-conformance-standard.git` — no embedded credential.

---

## Secrets and personal paths

- **Tracked files:** no `/Users/`, no `$HOME` expansion, no env dumps, no tokens.
- **README public links:** `github.com/cjchanh/deponent`, `github.com/cjchanh/sworn` — public identity, not a host path.
- **Mission (untracked):** `~/Workspace/active/gak-conformance-standard` — tilde path; process coupling if committed.
- **Campaign (untracked):** `.builder-foundry/baseline.json`, `locks/marathon.pid`, `logs/grok-inspect.txt`, `logs/session-01.jsonl` contain `/Users/cj/Workspace/...`, `/Users/cj/.claude/`, `/Users/cj/.grok/`.
- `.gitignore` excludes only `__pycache__/`, `*.pyc`, `.DS_Store`. Campaign dirs are **not** ignored.

---

## Claim language vs spec §8

**§8 bound:** mark means *passes the harness under the declared profile*. Does **not** mean secure, audited, adversarially robust, or endorsed. Public claims MUST publish certification JSON. Simulated adapters void the mark.

**README “The claim, bounded”:** restates not secure / not audited / not endorsed; points at §8. Honest on third-party verdicts: **zero**. Does **not** stretch adoption.

**Gap:** mission face *“research prototype, not a security-evaluated product”* is **not** on the README. §8 covers the mark; the product-face sentence is missing.

**Spec §7.1 / Appendix A** still document Deponent as the runnable harness (`from deponent.conformance import run_conformance`, `python3 -m deponent.badge verify`). That is vendor-owned execution, not a mark stretch — but it fights the vendor-neutral leave-behind.

---

## Adapter loading / code-exec

- **No in-repo adapter loader.** No `importlib`, `eval`, `exec`, `pickle`, `subprocess` in this repo.
- Planned mission entrypoint `python3 -m gak_conformance score --adapter <module:Class>` is **not implemented**.
- When implemented, `module:Class` is trusted-code import (arbitrary code exec of the named module). Must not `eval` source, must not unpickle adapters, must document that the adapter module runs on the host.
- Spec §6.3: a raising check records **exception type and message** in `detail` — host-path leak if the kernel raises `FileNotFoundError` etc.

---

## Receipt host-data

Checked: `v1/evidence/deponent-*.json`, `sworn-*.json`.

| Field | Present | Host leak? |
|---|---|---|
| `kernel`, `profile`, `conformant`, `counts`, `clauses` | yes | no |
| `schema_version`, `harness_version`, `mark`, `clauses_digest` (certs) | yes | no |
| timestamp | **no** (matches §5.1) | — |
| absolute paths | **no** | — |
| env / hostname / username | **no** | — |
| `detail` | clause statement or NA reason | generic; no host strings |

`determinism-proof.txt` names sibling repo SHA `e7e8fe6` and branch `feat/rename-deponent` — internal crumb, not a secret.

---

## `scripts/check_consistency.py` import surface

**Direct:**

- stdlib: `json`, `re`, `sys`, `pathlib`
- `deponent.badge` → `HARNESS_VERSION`, `certify`
- `deponent.conformance` → `CLAUSES`
- `import sworn` — presence probe only

**Not imported:** `deponent.attest` (private sibling name).

**Transitive (names-only, sibling public modules):** `from deponent.badge` loads package `__init__` → `cell`, `claims`, `gate`, `jail`, `ledger`, `profiles`, `receipts`. `conformance` loads `adapters.contract`, `adapters.deponent`. `cell` uses `claims.attest` (public claims helper), not `deponent.attest`.

**Runtime:** `certify("deponent")` (twice) executes the live sibling kernel. Fail-closed `ImportError` → exit 3. This script **is** the harness, not an adapter-boundary client.

---

## Findings by severity

### S2 — close before public leave-behind / any `git add -A`

1. **Vendor harness coupling.** `scripts/check_consistency.py` imports `deponent.badge` / `deponent.conformance`. README + spec §7.1 / App A tell third parties to run Deponent modules. No in-repo scorer. Violates mission “adapter boundary only” and “score without importing Deponent internals.”
2. **`.gitignore` does not exclude campaign state.** `.builder-foundry/` already holds `/Users/cj` and operator-home paths. Origin is a public GitHub repo. Accidental add is a personal-path leak.

### S3 — hygiene

3. README missing *research prototype, not a security-evaluated product*.
4. Spec §6.3 exception-message-in-`detail` is a future host-path leak in any new harness.
5. Future `--adapter module:Class` is code-exec of operator-supplied Python; document and do not eval/pickle.
6. `determinism-proof.txt` internal branch name `feat/rename-deponent`.
7. Untracked `MISSION_FOUNDRY_GAK_V0.md` names private-surface forbid-list and `~/Workspace/active/...` — do not add to the public tree.

### INFO — clean

- No secrets in tracked files.
- No `/Users/cj` in tracked product files.
- No copy of `attest.py`, `00Agent`, `cds-compliance`, CMMC-RMF maps, ATO-in-a-Box, per-control maps.
- Current receipts have no timestamps, paths, or env.
- Checker does not import `deponent.attest`.

---

## Release-forbidden material

Do **not** include in a public tag, zip, or push:

- `.builder-foundry/`, `.builder-foundry-kit/`
- `MISSION_FOUNDRY_GAK_V0.md`, `AGENTS.builder-foundry.md`
- `.agents/`, `.claude/`, `.grok/`
- anything matching the forbid-list above
- any file with `/Users/` or operator-home paths

Kit zipper (`safe_release_zip.py`) already excludes `.builder-foundry` / `.builder-foundry-kit`. **Git does not.** Relying on the zipper alone is not enough if the git tree is the leave-behind.

---

## Not done (this lane)

No code changes. Gates not weakened. Harness not rewritten.
