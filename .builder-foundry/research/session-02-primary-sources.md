# GAK v0 — Session 2 primary-source research (synthesis)

**Lane:** research (then consumed by implementation in the same session)
**Window:** official sources retrieved 2026-08-12
**Frozen target:** `gak-conformance/v1` (13 clauses; digest `de6b7089…`)
**This wave changes:** verify command, optional Deponent adapter isolation, leave-behind/release zip, loader grammar, exception-path redaction.

Session 1 locked receipt/clause/packaging doctrine. Session 2 answers the four remaining product questions with primary sources. Claim classes: `official_fact` · `measured` · `inference`.

---

## Bottom line (what changed)

| Decision | Why | What we will not do |
|---|---|---|
| Ship `verify --adapter --cert` | Spec §5.4 MUST; `digest --receipt` does not re-run the kernel. SLSA/in-toto: identity is digest; published PASS is not ALLOW. | Treat `score`+`digest` as §5.4. Require Cosign. |
| Lazy optional Deponent adapter via `importlib.import_module("deponent…")` | CPython: `find_spec` probes; `import_module` loads. Never put deponent in `[project].dependencies`. | Wrap `deponent.conformance`. Top-level `import deponent`. Named extra as the only path. Subprocess “sandbox.” |
| Product-tree + zip leave-behind scan; extra zip excludes | Apache §4d: ship LICENSE + NOTICE. Kit zipper omits `.builder-foundry` but **includes** `MISSION_FOUNDRY_GAK_V0.md` and `.agents/.claude/.grok`. | Full REUSE 3.3 on every file. Ignore entire `.builder-foundry/` (campaign state must stay). |
| Keep CLI exits **0 / 1 / 2** | Doctrine (higher layer) + shipped argparse. Research 0/1/2/3/4 is optional. | Advertise sysexits 64–78 or pytest 3/4/5 as portable. |
| Reject `..` and non-identifier adapter tokens | PyPA entry-points: `module:object` with identifier segments. | Claim the loader is a sandbox. |
| Redact host paths in clause `detail` | Spec §6.3 requires type + message. CWE-209 / OWASP: raw paths leak. | Drop the message entirely. Hash the pretty receipt. |

---

## F-28 Optional probe is `find_spec`; load is `import_module`; neither is a sandbox

- **Source:** [importlib](https://docs.python.org/3/library/importlib.html) (CPython 3.14.7 docs, retrieved 2026-08-12); [importlib.util.find_spec](https://docs.python.org/3/library/importlib.html#importlib.util.find_spec); [The import system](https://docs.python.org/3/reference/import.html)
- **Claim class:** official_fact · **Confidence:** high
- **Claim:** Programmatic import SHOULD use `importlib.import_module`. `find_spec(name)` is the documented way to ask whether a module can be imported. For a dotted name the **parent package is imported**. Module body runs when the loader executes, not at “first call.” [runpy](https://docs.python.org/3/library/runpy.html): “this is *not* a sandbox.”
- **Implication:** `gak_conformance.adapters.deponent` MUST NOT `import deponent` at module scope. Probe `find_spec("deponent")` (top-level name). Load `deponent.adapters.deponent` only inside `DeponentKernelAdapter.__init__` via **string** `import_module`. Missing Deponent → `ImportError` → CLI exit 2. Do not add `deponent` to `[project].dependencies`. An extra named `deponent` is install convenience only and **looks vendor-owned**; v0 ships **no extra**.
- **Do not copy:** claiming find_spec isolates untrusted code; `runpy.run_path`; putting the kernel in core deps.

**Measured here:** `importlib.util.find_spec("deponent")` is `None` in campaign Python (2026-08-12).

## F-29 PEP 621 extras vs vendor-neutral core

- **Source:** [PEP 621](https://peps.python.org/pep-0621/) (Final, 2020); [pyproject.toml spec](https://packaging.python.org/en/latest/specifications/pyproject-toml/)
- **Claim class:** official_fact · **Confidence:** high
- **Claim:** `[project.dependencies]` are required. `[project.optional-dependencies]` are extras (`pip install pkg[extra]`). Extras do not make a kernel own the standard.
- **Implication:** Keep `dependencies = []`. No `deponent` extra in v0 (optics + architecture §13). Runtime detect + documented skip.
- **Do not copy:** `deponent` as a required install; `pytest.importorskip` as a production CLI gate ([pytest.importorskip](https://docs.pytest.org/en/stable/reference/reference.html#pytest.importorskip) is a **test skip**).

## F-30 Standards do not let the reference tool own the standard

- **Source:** [SPDX tools](https://spdx.dev/use/spdx-tools/) (no endorsement of listed tools); [CIS Benchmarks](https://www.cisecurity.org/cis-benchmarks/) vs [CIS-CAT](https://www.cisecurity.org/cybersecurity-tools/cis-cat-pro); [OpenSSF Scorecard non-goals](https://github.com/ossf/scorecard)
- **Claim class:** official_fact · **Confidence:** high
- **Claim:** The spec and the assessment tool are different objects. Scorecard’s own README: not definitive; heuristics; aggregate hides behavior.
- **Implication:** In-repo `clauses.py` remains the clause table. Optional adapter **drives** Deponent’s public §6 class (`deponent.adapters.deponent.DeponentAdapter` per ARCHITECTURE.md). Never import `deponent.conformance` or `deponent.badge`. Score only frozen 13 v1 IDs.
- **Do not copy:** wrapping the vendor self-score suite (16 live Deponent IDs).

## F-31 §5.4 verify is a live re-score, not a file hash

- **Source:** spec `v1/spec.md` §5.4; [SLSA verifying artifacts v1.2](https://slsa.dev/spec/v1.2/verifying-artifacts); [SLSA provenance v1.2](https://slsa.dev/spec/v1.2/build-provenance) (ignore/delete extension MUST NOT turn DENY into ALLOW); [Sigstore threat model](https://docs.sigstore.dev/about/threat-model/) (a signature does not prove the artifact is good); [pytest exit codes](https://docs.pytest.org/en/stable/reference/exit-codes.html) (0 = success)
- **Claim class:** official_fact + inference · **Confidence:** high
- **Claim:** §5.4: obtain kernel+adapter → run harness → §3.4 → re-derive digest → compare published `clauses_digest`. Fail-closed if the re-run is not conformant, **whatever a previously published receipt says**. `digest --receipt` only hashes a file.
- **Implication:** Add `verify --adapter module:Class --cert FILE`. Exit **0** only if live score is conformant **and** digests match. Exit **1** if scored-not-conformant **or** digest mismatch (including a *now-conformant* kernel against a stale cert). Exit **2** if adapter/cert cannot be loaded. No signatures in v0.
- **Do not copy:** Cosign as a v0 requirement; treating a published PASS as sufficient ALLOW; hashing wall-clock fields.

## F-32 Entry-point object reference grammar

- **Source:** [Entry points specification](https://packaging.python.org/en/latest/specifications/entry-points/) (PyPA; retrieved 2026-08-12). Object reference is `importable.module` or `importable.module:object.attr`. Each part delimited by dots/colon is a **valid Python identifier**. Lookup: `import_module` then `getattr` walk.
- **Claim class:** official_fact · **Confidence:** high
- **Implication:** `--adapter` is this grammar with **exactly one colon** and a single class name (v0 does not walk `Class.factory`). Reject `..`, `/`, `\`, empty parts, extra colons, non-identifier segments.
- **Do not copy:** `eval`, `pickle`, `spec_from_file_location` as the default.

## F-33 CWE-209 vs spec §6.3

- **Source:** spec §6.3 (record exception **type and message**); [CWE-209](https://cwe.mitre.org/data/definitions/209.html); [OWASP Improper Error Handling](https://owasp.org/www-community/Improper_Error_Handling)
- **Claim class:** official_fact · **Confidence:** high
- **Claim:** Full path/traceback in a public receipt is sensitive-information leakage. Spec still requires a recorded exception.
- **Implication:** Keep `{type}: {message}` but redact `/Users/<name>`, `/home/<name>`, `X:\Users\<name>` to `<path>` in `detail`. Digest is unchanged (detail is not hashed).
- **Do not copy:** dropping the message; shipping raw `traceback.format_exception` on stdout JSON.

## F-34 Apache §4d + PEP 639 + REUSE 3.3

- **Source:** [Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0) (Jan 2004) §4(a)–(d); [PEP 639](https://peps.python.org/pep-0639/) (Final); [Setuptools license migration](https://setuptools.pypa.io/en/latest/userguide/license_migration.html) (v77+ SPDX string); [REUSE Spec 3.3](https://reuse.software/spec-3.3/) (2024-11-14); [git-archive export-ignore](https://git-scm.com/docs/git-archive)
- **Claim class:** official_fact · **Confidence:** high
- **Claim:** Redistribution MUST include the License and retain notices. If a NOTICE exists, derivatives must carry its attributions; NOTICE does **not** modify the License. PEP 639: `license = "Apache-2.0"` + `license-files`. REUSE wants every covered file annotated — **not required** by Apache-2.0. `export-ignore` keeps campaign dirs out of `git archive`.
- **Implication:** Keep LICENSE + NOTICE in the zip. Prefer PEP 639 in pyproject (setuptools 81 is installed here). Do **not** block v0 on `reuse lint`. Add `.gitattributes` export-ignore for campaign/kit/agent dirs. Extra zipper excludes: `MISSION_FOUNDRY_GAK_V0.md`, `AGENTS.builder-foundry.md`, `.agents/*`, `.claude/*`, `.grok/*`.
- **Do not copy:** claiming NOTICE changes the license; shipping mission/campaign host paths; requiring SPDX headers on every file this wave.

## F-35 JSON Schema Draft 2020-12 as a document, not a runtime engine

- **Source:** [JSON Schema Draft 2020-12](https://json-schema.org/draft/2020-12) (published 2022-06-16)
- **Claim class:** official_fact · **Confidence:** high
- **Implication:** Ship `v1/receipt.schema.json` for interop. Do **not** add a `jsonschema` dependency. The harness remains stdlib-only.

## F-36 Agent-gate category is still empty (third-party scores stay 0)

- **Sources (official, retrieved 2026-08-12):**
  - [OpenAI function calling](https://developers.openai.com/api/docs/guides/function-calling)
  - [Anthropic tool use](https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview)
  - [NVIDIA NeMo Guardrails](https://docs.nvidia.com/nemo-guardrails/index.html)
  - [Guardrails AI docs](https://guardrailsai.com/guardrails/docs)
  - [Lakera / Check Point AI Guardrails](https://docs.lakera.ai/docs/defenses)
  - [Semantic Kernel Filters](https://learn.microsoft.com/en-us/semantic-kernel/concepts/enterprise-readiness/filters) (updated 2026-05-01)
  - [OWASP Top 10 for Agentic Applications 2026](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/) (2025-12-09)
  - [OpenSSF Scorecard non-goals](https://github.com/ossf/scorecard)
- **Claim class:** official_fact (each product’s self-description) + inference (category emptiness)
- **Copy:** host-side execution; intercept-before-execute; named deny. **Do not copy:** cloud policy API as oracle; 0–10 scores; prompt-injection theater as the mark; “LLM said no” as PASS; Top-10 checklist cosplay.
- **Implication:** README mark language stays *research prototype / clause-bounded*. “Third-party verdicts: zero” remains honest. No official vendor-neutral mechanical suite for action-gates was found.

---

## Conflicts preserved (not silently reconciled)

1. **Doctrine Sequence C `verify` vs Architecture CLI (no verify) vs shipped `score`/`digest`/`selfcheck`.** Spec §5.4 is the higher layer → **ship verify**.
2. **Research F-18 exit 0/1/2/3/4 vs doctrine 0/1/2 vs shipped 2=usage+load.** Doctrine wins → **keep 0/1/2**; narrow `except` so harness bugs are not “load failed.”
3. **`test_import_boundary.py` AST-forbids any `import deponent` under `gak_conformance/`.** Do not weaken the test. Use string `import_module`.
4. **Doctrine Sequence A token `gak_conformance.fixtures:FixtureActionAdapter` vs shipped `…action_gate:PassingActionAdapter`.** Amend doctrine to the shipped token (one public name).
5. **PEP 639 string license vs current `license = { file = "LICENSE" }`.** Setuptools 81 is present → migrate.
6. **Session-1 leave-behind scan is stale** (claimed no scorer, checker imports Deponent). Re-scan product + zip.

---

## Backlog deltas this wave (writer implements)

| ID | Item | Finding |
|---|---|---|
| FEAT-0026 | Optional `DeponentKernelAdapter` (lazy; exit 2 if absent; 13 v1 clauses if present) | F-28–F-30 |
| FEAT-0039 | `verify --adapter --cert` | F-31 |
| FEAT-0040 | `list-clauses` + `--help` names score/selfcheck/verify/list-clauses | doctrine + Appendix B |
| FEAT-0041 | README: v1 face first; Sequence B one-liner; exit 0/1/2; Sequence D in-repo adapter | F-36, doctrine |
| FEAT-0042 | `audit_is_content_blind` documented as v1.1-only on the Protocol | spec §6 vs amendment |
| FEAT-0043 | Loader rejects `..` and non-identifiers | F-32 |
| FEAT-0007 / 0027 / 0028 | Product+zip leave-behind; create_release smoke with PYTHONPATH=. | F-34 |
| FEAT-0044 | Host-path redaction in FAIL `detail` | F-33 |

## Out of v0 (reconfirmed)

- Cosign / DSSE / SLSA envelope
- REUSE lint as a gate
- jsonschema runtime
- Extra-probe / non-literal anchors (would change the scorer; honesty remains §6.3/§8)
- Subprocess plugin sandbox
- Deponent extra / PyPI publish
- Claiming an official agent-gate category exists

## Fleet task IDs (independent research)

| Task | Topic |
|---|---|
| `grk_e9a640b6aede4cb5adb73ff47c3db256` | Optional adapter / find_spec / extras |
| `grk_2dcba48125fc473aa66b6ed7d8f73998` | Release zip / Apache / PEP 639 / REUSE |
| `grk_bc780722ed914d2e862ccf11f3b47c53` | Verify / SLSA / CWE-209 / entry points |
| `grk_580c9a8bec5b44acb265bf2f9f56d0c5` | Agent-gate comparables |
