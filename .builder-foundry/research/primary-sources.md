# GAK v0 — Primary sources (mechanical scorer + deterministic receipt)

**Lane:** research (read-only)
**Scope:** vendor-neutral mechanical conformance scorer + deterministic JSON receipt
**Window:** sources current as of 2025–2026
**Frozen target:** `gak-conformance/v1` in `v1/spec.md` (13 clauses; digest `de6b7089…`)

**Bottom line:** copy *named clause IDs, binary PASS/FAIL/NA, versioned harness string, re-runnable digest, fail-closed exit 0 only when the mark is earned*. Do **not** copy Scorecard 0–10 aggregates, SLSA/in-toto envelopes (timestamps + signatures), SBOM schemas, Common Criteria labs/EALs, or CISA-style self-attestation forms.

Each finding: source, date/version, claim class, confidence, GAK v0 implication, what **not** to copy.

Claim classes: `official_fact` (the spec/docs say this) · `third_party_report` · `inference`.

---

## 1. Comparable products / patterns

### F-01 SLSA provenance is a *build* attestation, not a behavior score

- **Source:** [SLSA Build Provenance v1.2](https://slsa.dev/spec/v1.2/build-provenance); current spec series is v1.2 ([slsa.dev/spec/v1.2/provenance](https://slsa.dev/spec/v1.2/provenance))
- **Version/date:** SLSA v1.2; predicateType `https://slsa.dev/provenance/v1` (URI always resolves to latest *minor*)
- **Claim class:** official_fact · **Confidence:** high
- **Claim:** Provenance is an in-toto predicate: `buildDefinition` + `runDetails`. `runDetails.metadata` carries `invocationId`, `startedOn`, `finishedOn` (ISO-8601 Z). Parsing rules: consumers MUST ignore unrecognized fields; unset/null/empty are equivalent; major version is in the type URI.
- **Implication:** GAK certification already has the useful bits: typed `schema_version` / `harness_version`, ignore-unknown future fields, re-derive-and-compare. Keep **no timestamp** in receipt or digest (spec §5.1 / §5.3). A later optional *envelope* MAY attach SLSA/in-toto around a frozen receipt without changing §5.3 bytes.
- **Do not copy:** build-platform `builder.id` trust model; L1–L3 tracks; `startedOn`/`finishedOn` inside the identity of the result; “consumers ignore missing fields” as a way to treat missing clause results as PASS (that is fail-open).

### F-02 in-toto Statement + monotonic policy

- **Source:** [in-toto Attestation Framework spec v1](https://github.com/in-toto/attestation/blob/main/spec/v1/README.md) (Version: v1.2); [Statement layer](https://github.com/in-toto/attestation/blob/main/spec/v1/statement.md). Release v1.2.0 dated 2026-03-18.
- **Claim class:** official_fact · **Confidence:** high
- **Claim:** Layers are Envelope (auth/serialization) → Statement (`_type`, `subject`+digest, `predicateType`, `predicate`) → Predicate. **Monotonic principle:** ignoring an attestation or field MUST never turn DENY into ALLOW. Example given: deny *unless* a “no vulnerabilities” attestation exists — not “deny if a has-vulnerabilities attestation exists.”
- **Implication:** GAK §3.4 already matches: all-NA is a refusal; a missing/erroring check is FAIL (§3.3). Implement the scorer as “deny unless evidence of PASS”; never treat omitted clause rows as PASS. Version the harness string the way in-toto versions TypeURIs (`gak-conformance/v1` vs `/v1.1`).
- **Do not copy:** DSSE/sigstore Envelope as a v0 requirement; `subject` artifact-digest binding (GAK scores a *running kernel*, not a blob); protobuf as the interchange format.

### F-03 SPDX 3.0.1 is an inventory + declared-profile claim

- **Source:** [SPDX Specification 3.0.1](https://spdx.github.io/spdx-spec/v3.0.1/) (Linux Foundation, © 2010–2024); [ProfileIdentifierType](https://spdx.github.io/spdx-spec/v3.0.1/model/Core/Vocabularies/ProfileIdentifierType/)
- **Claim class:** official_fact · **Confidence:** high
- **Claim:** SPDX 3 organizes fields into profiles (`core`, `software`, `security`, `build`, `lite`, …). Listing a profile in `profileConformance` **claims** that contained elements meet that profile’s restrictions. SPDX 2.3 is ISO/IEC 5962:2021; 3.0.1 is the current 3.x text.
- **Implication:** Copy the *idea* of a declared profile (`action-gate` | `commit-gate`) plus a machine-check that the declaration matches the clause set. Use SPDX **license expressions** in `pyproject.toml` (see F-16). GAK receipt is not an SBOM.
- **Do not copy:** SPDX JSON-LD / RDF document shape; component graphs; treating `profileConformance` as self-attested without a mechanical run.

### F-04 CycloneDX 1.7 has Declarations (“compliance-as-code”) — too heavy for v0

- **Source:** [CycloneDX specification overview](https://cyclonedx.org/specification/overview/) — Current Version **1.7**, release **2025-10-21**, ECMA-424 2nd Ed. published **2025-12-10**. in-toto predicate type `https://cyclonedx.org/bom`.
- **Claim class:** official_fact · **Confidence:** high
- **Claim:** Object model includes Components, Dependencies, Formulation, **Definitions** (standards/requirements/levels; ASVS ships as CDX), and **Declarations** (attestations, claims, counter-claims, evidence, conformance, confidence, signatories). Media types are IANA-registered (`application/vnd.cyclonedx+json`).
- **Implication:** GAK’s receipt is the lightweight cousin of a Declaration: named standard + per-requirement status + digest. Stay on the small schema in spec §5.1/§5.2. A future export *to* CycloneDX Declarations is optional interop, not v0.
- **Do not copy:** full BOM/CBOM/ML-BOM; confidence scores; counter-claim graphs; requiring IANA media types; formulation/workflow blocks.

### F-05 OpenSSF Scorecard: named checks yes; 0–10 aggregate no

- **Source:** [ossf/scorecard README](https://github.com/ossf/scorecard); [docs/checks.md](https://github.com/ossf/scorecard/blob/main/docs/checks.md); [scorecard.dev](https://scorecard.dev/)
- **Version/date:** live main, 2025–2026. Project non-goals are first-party.
- **Claim class:** official_fact · **Confidence:** high
- **Claim:** Each check scores 0–10. Aggregate is a **risk-weighted average** (Critical 10, High 7.5, Medium 5, Low 2.5). Maintainers state non-goals: not a definitive report; checks are **heuristics** with false positives/negatives; **aggregate scores hide which behaviors occurred**; many ways to arrive at the same number. CII/OpenSSF Best Practices badge check is largely **self-claimed**. Structured Results / probes exist because a single score is not policy-grade. CI-Tests docs admit detection gaps → low score ≠ definitive risk.
- **Implication:** GAK already chose the better model: 13 named IDs, ternary PASS/FAIL/NA, `conformant` = (no FAIL ∧ ≥1 PASS). Emit **structured per-clause results**, not a 0–10. CLI/docs must say the mark is the clause set, not a health score.
- **Do not copy:** weighted aggregate; “score out of 10”; GitHub-heuristic checks; network/API scanning; treating a high aggregate as conformance.

### F-06 CIS Benchmarks / CIS-CAT: per-rule pass/fail; Manual ≠ scored

- **Source:** [CIS-CAT Pro Assessor](https://www.cisecurity.org/cybersecurity-tools/cis-cat-pro); [CIS scoring-status blog](https://www.cisecurity.org/insights/blog/changes-to-cis-benchmark-assessment-recommendation-scoring); XCCDF language: [NIST SCAP/XCCDF](https://csrc.nist.gov/projects/security-content-automation-protocol/specifications/xccdf) / NISTIR 7275 Rev. 4 (XCCDF 1.2, 2011/2012)
- **Claim class:** official_fact · **Confidence:** high
- **Claim:** CIS renamed Scored/Not Scored → **Automated/Manual**. Manual recommendations **cannot** produce automated pass/fail and are **excluded from the overall numeric score**. CIS-CAT still prints a compliance **percentage** over automated rules. Older XCCDF default scoring is weighted-sibling, not boolean conformance. CIS-CAT is Java + member-gated XML — not a stdlib CLI.
- **Implication:** Map Automated → scored clauses, Manual/out-of-profile/unclaimed capability → **NA**. NA must not inflate a pass rate. GAK has **no** percentage: one FAIL fails the mark (§3.4, §7.3 “no partial credit”).
- **Do not copy:** % compliant; weighted XCCDF scores; “Manual omitted from the headline number”; member-only content; remote SSH/WinRM assessor architecture.

### F-07 NIST SSDF + CISA Secure Software Attestation Form = author self-claim

- **Source:** [NIST SP 800-218 SSDF v1.1](https://csrc.nist.gov/pubs/sp/800/218/final) (final **2022-02-03**, DOI 10.6028/NIST.SP.800-218); [CISA Secure Software Development Attestation Form](https://www.cisa.gov/resources-tools/resources/secure-software-development-attestation-form) (revision **2024-05-14**). OMB M-26-05 (cited on the CISA page) makes the government-wide form optional.
- **Claim class:** official_fact · **Confidence:** high
- **Claim:** SSDF is a *practice framework* (vocabulary for producers/purchasers), not a mechanical harness. The CISA form is a **self-attestation** over a **subset** of SSDF 1.1. There is no third-party re-run that recomputes a digest of observed behavior.
- **Implication:** GAK v0 exists to *escape* this failure mode. Author-signed prose is not a receipt. `v1/evidence/deponent-*.json` is **author-run evidence**, not a third-party verdict (mission PS-05). The product is `python3 -m gak_conformance score --adapter …`.
- **Do not copy:** PDF/form attestation; “we follow SSDF” as a mark; subset-of-practices checkboxes; producer-signed letters in place of a harness run.

### F-08 OWASP ASVS 5.0.0 — versioned requirement IDs; levels ≠ GAK profiles

- **Source:** [OWASP ASVS project](https://owasp.org/www-project-application-security-verification-standard/) (stable **5.0.0**, announced **2025-05-30**); [github.com/OWASP/ASVS v5.0.0](https://github.com/OWASP/ASVS/tree/v5.0.0); [0x03-What-is-the-ASVS.md](https://github.com/OWASP/ASVS/blob/master/5.0/en/0x03-What-is-the-ASVS.md)
- **Claim class:** official_fact · **Confidence:** high
- **Claim:** Requirements use `<chapter>.<section>.<requirement>`. External refs SHOULD be `v<version>-<id>` (e.g. `v5.0.0-1.2.5`) because IDs move across versions. Three **verification levels** (L1/L2/L3) increase depth; L2 is the intended default for most apps. ASVS is a *catalog to verify against*, not a single boolean mark. v5 states black-box-only is insufficient.
- **Implication:** Copy **version-pinned IDs** (`GAK-DENY-DEFAULT` under harness `gak-conformance/v1`). Profiles (`action-gate`/`commit-gate`) are *shape*, not assurance depth — do not rename them L1/L2/L3. Keep “conformance is the clause set under this harness version” (spec §8).
- **Do not copy:** ~350 web/API requirements; L1/L2/L3 as a marketing ladder; treating GAK as an application pentest standard.

### F-09 Common Criteria CC:2022 vs lightweight clause receipts

- **Source:** [commoncriteriaportal.org Publications](https://www.commoncriteriaportal.org/cc/index.cfm) — CC:2022 Release 1 (Parts 1–5 + CEM:2022); Exact Conformance addendum CCDB-013; transition: CC 3.1 starts no later than 2024-06-30; ST-on-3.1-PP accepted through 2027-12-31.
- **Claim class:** official_fact · **Confidence:** high
- **Claim:** CC is lab-evaluated conformance to a Protection Profile / Security Target, with SARs/SFRs and (historically) EALs. CC:2022 instantiates **Exact Conformance** (no cafeteria SFRs). Cycle time is months–years and requires a licensed lab. That is a different product than a 13-clause mechanical receipt.
- **Implication:** Copy **Exact Conformance** (every applicable clause; no waivers — spec §7.3) and **bounded claim language** (spec §8: not “secure/evaluated”). Face the leave-behind as *research prototype, not a security-evaluated product* (mission). Independent *re-run* is GAK’s stand-in for a lab.
- **Do not copy:** EAL numbers; Protection Profiles; evaluator labs; CEM activity catalogs; “certified product” wording.

### F-10 What to copy vs not (synthesis)

| Pattern | Copy | Do not copy |
|---|---|---|
| SLSA / in-toto | Typed version URI; monotonic deny-unless-evidence; ignore-*unknown* fields | Timestamps in identity; DSSE; build L1–L3; subject-blob binding |
| SPDX / CycloneDX | SPDX license string; declared profile; optional future export | SBOM/BOM as the receipt; CDXA confidence/signatories |
| Scorecard | Named checks; structured per-check results | 0–10 weights; aggregate; GitHub heuristics |
| CIS / XCCDF | Per-rule pass/fail; Manual → NA | Percentage score; weighted default model |
| SSDF / CISA form | Named practice IDs as vocabulary only | Self-attestation form as the product |
| ASVS | Version-pinned requirement IDs | L1–L3 ladder; web-app catalog |
| Common Criteria | Exact conformance; bounded mark | Labs, EALs, “evaluated product” |

---

## 2. Python packaging — stdlib-only CLI

### F-11 PEP 517 `module:object` is the adapter string

- **Source:** [PEP 517](https://peps.python.org/pep-0517/) (Final, 2015–2017)
- **Claim class:** official_fact · **Confidence:** high
- **Claim:** `build-backend` uses setuptools entry-point grammar:

  ```
  identifier = (letter | '_') (letter | '_' | digit)*
  module_path = identifier ('.' identifier)*
  object_path = identifier ('.' identifier)*
  entry_point = module_path (':' object_path)?
  ```

  Lookup is `import module_path` then attribute walk. Backend import MUST NOT implicitly search the source tree unless it is already on `sys.path`.
- **Implication:** `--adapter <module:Class>` MUST use this grammar (reject `/`, `..`, empty, extra colons). Load with `importlib.import_module` + `getattr` — not `eval`, not `pickle`, not `spec_from_file_location` unless a separate, loudly-documented `--adapter-file` is added later. Putting the project root on `sys.path` is the caller’s job (`python3 -m` from a checkout already does this).
- **Do not copy:** PEP 517 `backend-path` in-tree backend search as a silent default for untrusted adapters.

### F-12 PEP 621 / current `pyproject.toml` spec

- **Source:** [PEP 621](https://peps.python.org/pep-0621/) (Final, 2020; historical); canonical [pyproject.toml specification](https://packaging.python.org/en/latest/specifications/pyproject-toml/) (PyPA, live 2026)
- **Claim class:** official_fact · **Confidence:** high
- **Claim:** `[build-system]` declares `requires` + `build-backend`. Missing table defaults to setuptools. `[project]` requires static `name`; `version` static or `dynamic`. `license` is now an SPDX expression string (PEP 639); table form is legacy. `dependencies` may be empty. `scripts` / `entry-points` are optional. Tools MUST error on invalid metadata.
- **Implication:** Ship a minimal `pyproject.toml`:

  ```toml
  [build-system]
  requires = ["setuptools>=68"]
  build-backend = "setuptools.build_meta"

  [project]
  name = "gak-conformance"
  version = "0.1.0"
  description = "Vendor-neutral GAK mechanical conformance scorer"
  readme = "README.md"
  requires-python = ">=3.10"
  license = "Apache-2.0"
  dependencies = []
  ```

  Runtime stays **stdlib-only** (`json`, `hashlib`, `argparse`, `importlib`, `sys`). Build backend is install-time only. Do **not** put Deponent in `dependencies`.
- **Do not copy:** Poetry `[tool.poetry]` as the metadata source; runtime deps for HTTP, pydantic, click, or DSSE; dynamic version from git (hurts offline reproducibility).

### F-13 `python3 -m package` is the documented entry (PEP 338 / runpy)

- **Source:** [PEP 338](https://peps.python.org/pep-0338/) (Final, Python 2.5+); [runpy](https://docs.python.org/3/library/runpy.html) (CPython 3.14.7 docs, updated 2026-08-11)
- **Claim class:** official_fact · **Confidence:** high
- **Claim:** `-m` locates a module via import and executes its code (`pkg/__main__.py` for a package). `runpy` is **not a sandbox**; side effects persist. Relative imports in `__main__` are historically sharp; use absolute imports.
- **Implication:** Primary UX is `python3 -m gak_conformance …` with `gak_conformance/__main__.py`. Works from a clone without installing console scripts. `project.scripts` MAY be added later as an alias, never as the only path.
- **Do not copy:** `setup.py` console-only entry with no `__main__`; relying on `pip install` before `--help` works.

### F-14 Offline `--help` / import-time network

- **Source:** mission (`MISSION_FOUNDRY_GAK_V0.md`); GNU Coding Standards §4.8 (F-28); inference from PEP 338 + argparse
- **Claim class:** inference · **Confidence:** high
- **Claim:** Any import of Deponent, HTTP version checks, or adapter load inside `argparse` construction will break “clone → `--help`” and the fixture selfcheck.
- **Implication:** `__main__.py` must parse argv and print help **before** `importlib.import_module(adapter)`. `selfcheck` uses an in-repo fixture adapter. No telemetry. No DNS.
- **Do not copy:** Scorecard’s GitHub-token CLI; pip’s network index probe on invocation.

---

## 3. Deterministic JSON + SHA-256

### F-15 CPython `json.dumps` defaults match spec §5.3 — RFC 8785 does **not**

- **Source:** [json — Python 3.14.7](https://docs.python.org/3/library/json.html); spec `v1/spec.md` §5.3; [RFC 8785 JCS](https://www.rfc-editor.org/rfc/rfc8785.html) (Informational, June 2020)
- **Claim class:** official_fact · **Confidence:** high
- **Claim:** CPython `json.dumps(obj, sort_keys=True)` with `indent=None` uses:
  - `separators = (', ', ': ')` — **space after `,` and after `:`**
  - `ensure_ascii=True` — non-ASCII escaped as `\uXXXX`
  - `allow_nan=True` — would emit `NaN`/`Infinity` (illegal JSON) if floats appear
  - `sort_keys=True` sorts **every** dict, recursively
  Compact form `separators=(',', ':')` is a different byte string. RFC 8785 **forbids whitespace between tokens** and serializes numbers via ECMAScript (rounding). JCS ≠ §5.3.
- **Implication:** Implement digest **exactly** as the spec snippet, but pin kwargs so a future “cleanup” cannot drift:

  ```python
  json.dumps(body, sort_keys=True, separators=(", ", ": "),
             ensure_ascii=True, allow_nan=False)
  ```

  Hash `hashlib.sha256(text.encode("utf-8")).hexdigest()` — lowercase hex ([hashlib](https://docs.python.org/3/library/hashlib.html); `sha256` is in `algorithms_guaranteed`). Digest object contains only strings + arrays of strings → no float/NaN path. **Do not switch to JCS** — that is a v2 event and would invalidate `de6b7089f894e009a6d1a1dba8c9b32b26e38daf803b07b83ec0958ff64c5406`.
- **Do not copy:** RFC 8785 / `rfc8785.py`; `separators=(',', ':')`; `ensure_ascii=False`; `indent=2` inside the digest body; including `detail`, timestamps, or `conformant` in the hashed object.

### F-16 Receipt pretty-print ≠ digest bytes

- **Source:** spec §5.1 vs §5.3; existing [`v1/evidence/deponent-conformance-receipt.json`](../../v1/evidence/deponent-conformance-receipt.json) (indent-2, clause order = Appendix A, not lexicographic)
- **Claim class:** official_fact · **Confidence:** high
- **Claim:** The receipt is a different document from the digest body. Digest sorts `(id, status)` pairs; receipt in evidence is *not* sorted by `id`. Spec requires “equivalent receipts” across runs, not pretty-print identity of the human receipt.
- **Implication:** Pin **two** serializers: (1) digest = §5.3 one-line spaced JSON; (2) `--out` receipt = stable indent-2, **fixed clause order** (spec §4 / Appendix A order), no timestamp. Re-derivation compares **digest**, not `diff` of pretty JSON. Still make two runs of an unchanged fixture byte-identical on the digest *and* on the receipt if the serializer is pinned.
- **Do not copy:** hashing the pretty receipt; leaving clause order to `dict` iteration; adding `generated_at`.

### F-17 Unicode, clocks, and “equivalent”

- **Source:** spec §5.3 (ASCII kernel names); RFC 8785 §3.1 (no Unicode normalization); Python `json` `ensure_ascii` docs
- **Claim class:** official_fact + inference · **Confidence:** high
- **Claim:** Kernel `name` MUST be ASCII `[A-Za-z0-9._-]` recommended. JCS explicitly does **not** apply Unicode normalization — “as is.” Wall clocks in SLSA `startedOn` would make two honest runs diverge.
- **Implication:** Reject non-ASCII `adapter.name` at score time (fail-closed, exit ≠ 0). `detail` MAY contain Unicode (not in digest). Never call `datetime.now()` / `time.time()` on the receipt or digest path.
- **Do not copy:** NFC/NFKC normalization of names; ISO timestamps “for audit”; locale-dependent separators.

---

## 4. Fail-closed CLI exit codes

### F-18 POSIX / sysexits / pytest / existing GAK appendix

- **Sources:**
  - [OpenBSD sysexits(3)](https://man.openbsd.org/sysexits) — 2017 text: codes 64–78; page now says **“Do not use them”** (non-portable). `EX_OK=0`, `EX_USAGE=64`, `EX_DATAERR=65`, `EX_SOFTWARE=70`, `EX_TEMPFAIL=75`, `EX_CONFIG=78`
  - [pytest exit codes](https://docs.pytest.org/en/stable/reference/exit-codes.html): **0** all passed · **1** tests ran, some failed · **2** interrupted · **3** internal error · **4** usage · **5** no tests collected
  - spec Appendix A: Deponent `verify` exits **0** mark earned · **1** non-conformant · **2** unknown kernel
  - argparse (F-27): usage errors → `SystemExit(2)`
- **Claim class:** official_fact · **Confidence:** high
- **Claim:** Every serious harness treats **0 as “the desired outcome happened.”** pytest’s 0 is *all tests passed*, not “the process ran.” Using 0 for “scored but failed” would fail-open every CI `&&`.
- **Implication:** Document a **small custom table** (do not claim sysexits portability):

  | Code | Meaning |
  |---|---|
  | **0** | scored **and** conformant (§3.4) |
  | **1** | scored, **not** conformant (any FAIL, or all-NA) |
  | **2** | cannot score — usage / missing `--adapter` / bad grammar / unknown command (argparse default) |
  | **3** | adapter import/construct failed (trusted-code load error) |
  | **4** | harness internal error (should be unreachable) |

  `selfcheck` / `--help` / `--version` exit 0. Never exit 0 for a FAIL receipt. Do not reuse Foundry’s **75** (dual-start) inside this CLI.
- **Do not copy:** “0 = ran successfully”; silent mapping of all errors to 1; advertising sysexits.h as POSIX; Scorecard-style 0–10 as process status.

---

## 5. Plugin / adapter loading safety

### F-19 `importlib.import_module` executes module-level code

- **Source:** [importlib](https://docs.python.org/3/library/importlib.html) (CPython 3.14.7); [runpy](https://docs.python.org/3/library/runpy.html) (“this is *not* a sandbox”); PEP 517 lookup (F-11)
- **Claim class:** official_fact · **Confidence:** high
- **Claim:** `import_module(name)` is the supported programmatic import. Import runs the module body in-process (same as `pytest` collecting a plugin, or `build-backend`). `getattr(module, "Class")` does not execute the class body beyond normal class creation; **instantiation** (`Cls()`) runs `__init__`.
- **Implication:** `--adapter` is a **trusted-code load**, not a data format. Document that residual risk honestly in `--help` and README. Mitigations that actually help: (1) PEP 517 identifier grammar only; (2) no `eval`/`exec`/`pickle`; (3) no filesystem path by default; (4) instantiate only after `getattr`; (5) require `name`/`profile`/`supports` before any clause dispatch; (6) a raise during a clause is FAIL (§6.3), a raise during import is exit 3.
- **Do not copy:** claiming the loader is a sandbox; loading via `runpy.run_path` (mutates `sys.path`); `importlib.util.spec_from_file_location` on user paths as the default.

### F-20 pickle / eval are RCE

- **Source:** [pickle](https://docs.python.org/3/library/pickle.html) — warning: “The pickle module **is not secure**. … malicious pickle data which will **execute arbitrary code during unpickling**.” JSON “does not in itself create an arbitrary code execution vulnerability.”
- **Claim class:** official_fact · **Confidence:** high
- **Implication:** Adapter identity is a string `module:Class`. Receipts and certifications are JSON only. No `.pkl` adapter cache. No `eval(args.adapter)`.
- **Do not copy:** pickle for “fast adapter snapshots”; `yaml.load` (unsafe); `marshal`.

### F-21 Path traversal and unexpected execution (residual risk)

- **Source:** inference from import system + PEP 517 “do not look in the source tree unless on `sys.path`”
- **Claim class:** inference · **Confidence:** high
- **Claim:** Strings like `--adapter ../../evil:X`, `--adapter /tmp/x:Y`, `--adapter evil;os.system`: the grammar reject is the control. If a future `--adapter-file PATH.py` is added, that path **is** code execution — same as `python3 PATH.py`. Relative imports inside a user adapter can import sibling attacker modules if cwd is on `sys.path` (it is, under `-m`).
- **Implication:** Validate with the PEP 517 regex; reject more than one `:`; reject any `/`, `\`, or `..`. Document: *loading an adapter runs that code with the scorer’s privileges.* Do not pretend path validation removes ACE.
- **Do not copy:** “safe plugin host” marketing; restricting imports via partial sandboxing that fails open.

---

## 6. Accessibility / first-run (CLI, not a web UI)

### F-22 GNU CLI + argparse are the first-run surface

- **Source:** [GNU Coding Standards §4.8](https://www.gnu.org/prep/standards/html_node/Command_002dLine-Interfaces.html); [argparse](https://docs.python.org/3/library/argparse.html) (CPython 3.14.7)
- **Claim class:** official_fact · **Confidence:** high
- **Claim:** GNU: support `--help` and `--version`; long options; output files via `-o`/`--output` rather than a positional. argparse auto-generates help; `epilog` is the place for a copy-paste example; `RawDescriptionHelpFormatter` preserves that example. Python 3.14 defaults `color=True` on `ArgumentParser`.
- **Implication:** First-run for a **third-party kernel author**:

  ```
  python3 -m gak_conformance --help
  python3 -m gak_conformance selfcheck
  python3 -m gak_conformance score --adapter gak_conformance.fixtures:FixtureAdapter --out receipt.json
  ```

  Help text states: profiles, adapter contract pointer (`v1/spec.md` §6), residual import risk, exit codes, “GAK-conformant means the 13 clauses, not a security evaluation.” Receipt JSON on **stdout** (or `--out`); diagnostics on **stderr**. No TTY, no pager, no color-only PASS/FAIL (PASS/FAIL/NA as text). Respect `NO_COLOR`; consider `color=False` so 3.14 does not paint help.
- **Do not copy:** web dashboard; Scorecard badges as the intro; requiring a GitHub token; color-only status; `--help` that imports Deponent.

### F-23 Dyslexia / reading-load (operator-facing CLI copy)

- **Source:** campaign operator-cognition rules (always-on); GNU “users should be able to expect `--verbose`”
- **Claim class:** inference · **Confidence:** high
- **Implication:** `--help` is short lines, one example to copy, no wall of theory. Subcommands named after verbs: `score`, `selfcheck`, `digest` (re-hash a receipt). Failures print the **clause id** first, then one-line detail.
- **Do not copy:** multi-page man-style dump as the only help; emoji-only marks.

---

## 7. Known failure modes of self-score programs

### F-24 Author-only evidence

- **Source:** CISA SSDF form (F-07); OpenSSF Best Practices badge (Scorecard CII-Best-Practices check, F-05); spec §8 (unverified public claim = assertion); mission PS-05 “Third-party scores: 0”
- **Claim class:** official_fact · **Confidence:** high
- **Claim:** Self-attestation and author-run evidence systematically over-report. Scorecard’s own docs contrast automatic detection vs human-claimed badges.
- **Implication:** Ship a stranger-runnable scorer. Treat `v1/evidence/deponent-*` as **informative, author-produced**. A live Deponent score in this campaign is still first-party unless someone else re-runs. README must say how a stranger scores *their* kernel without us.
- **Do not copy:** “certified by the authors” as the mark; directory listings without a re-runnable receipt.

### F-25 Simulated adapters (void mark)

- **Source:** spec §6.3 / §8: adapter MUST drive the **real** kernel; fabricated outcomes → mark void
- **Claim class:** official_fact · **Confidence:** high
- **Implication:** The in-repo **fixture** adapter is for offline `--help`/selfcheck and digest golden tests. It MUST NOT be a “return PASS for everything” shim used to mint a Deponent (or hedge) mark. Label fixture receipts `kernel: fixture` (or similar) so they cannot be confused with a product kernel. No hidden special-case `if name == "deponent": return canned_receipt`.
- **Do not copy:** record/replay adapters as conformance evidence; hardcoded Appendix A JSON as the score result.

### F-26 Clause special-casing (test-anchor gaming)

- **Source:** spec §4 intro: anchors are **minimum probes, not the obligation**; special-casing literal inputs while allowing equivalent violations is non-conformant. Scorecard non-goals: heuristics, false pos/neg. CIS: automatable check ≠ the whole recommendation.
- **Claim class:** official_fact · **Confidence:** high
- **Implication:** Scorer calls adapter methods with the spec’s literal anchors (so third parties can re-run). README/spec already warn that passing the literal while failing the normative sentence is cheating. v0 MAY add **one extra probe per ALLOW/BLOCK clause** (different but equivalent input) as a harness hardening — that is a product choice, not a spec change, if it still implements the stated anchors. Do not encode Deponent-only path strings.
- **Do not copy:** vendor-specific oracles; Scorecard-style “we guessed your CI name.”

### F-27 Optimistic NA / all-NA / deny-everything

- **Source:** spec §3.2–§3.4
- **Claim class:** official_fact · **Confidence:** high
- **Claim:** Unclaimed capability → NA; claimed-but-broken → FAIL. All-NA is not conformant. Deny-everything fails GAK-ALLOW-INBOUNDS / GAK-COMMIT-ALLOW-CLEAN.
- **Implication:** Implement §3.4 in one function used by both CLI exit and `conformant` field. Test: empty-profile adapter → exit 1; brick adapter → exit 1; honest fixture with ≥1 PASS and 0 FAIL → exit 0.
- **Do not copy:** CIS-style “Manual excluded from score so the number looks better.”

---

## Cross-cutting constraints already in-repo

- Scorer lives **in this repo**; `from deponent.conformance import run_conformance` is a defect (`scripts/check_consistency.py` today).
- v0 ships frozen **v1** 13 clauses, not v1.1’s optional 14th.
- Face: research prototype; mark language spec §8.

---

## Backlog implications

Research must change the empty feature/hypothesis ledgers. Suggested IDs (writer lane to open; this lane does not edit ledgers):

### Features to add

| ID | Item | Why (finding) |
|---|---|---|
| **FEAT-001** | stdlib-only `gak_conformance` package + `pyproject.toml` (PEP 517/621, `dependencies = []`, SPDX `license = "Apache-2.0"`) | F-12 |
| **FEAT-002** | `gak_conformance/__main__.py` so `python3 -m gak_conformance` works without install | F-13 |
| **FEAT-003** | `score --adapter module:Class [--out receipt.json]` | mission, F-11, F-22 |
| **FEAT-004** | Offline `--help` / `--version` (no adapter, no network, no Deponent import) | F-14, F-22 |
| **FEAT-005** | `selfcheck` subcommand using in-repo fixture adapter | F-14, F-25 |
| **FEAT-006** | Receipt emit per spec §5.1 (no timestamp; 13 clauses; `id/profile/status/detail`) | F-16 |
| **FEAT-007** | Digest helper: `json.dumps(..., sort_keys=True, separators=(", ", ": "), ensure_ascii=True, allow_nan=False)` + SHA-256 hex | F-15 |
| **FEAT-008** | Optional `certify` / `--certification` emit of `gak-certification/v1` (§5.2) | F-01, spec §5.2 |
| **FEAT-009** | Exit-code table: 0 conformant, 1 not conformant, 2 usage, 3 adapter load, 4 internal | F-18 |
| **FEAT-010** | Adapter loader: PEP 517 grammar, `import_module`+`getattr`, reject path-like strings | F-11, F-19–F-21 |
| **FEAT-011** | `--help` residual-risk sentence: adapter import is trusted-code execution | F-19, F-21 |
| **FEAT-012** | stdout = receipt JSON; stderr = human verdict; `--out` for file (GNU `-o`) | F-22 |
| **FEAT-013** | Stable receipt clause order = spec §4 / Appendix A (independent of digest sort) | F-16 |
| **FEAT-014** | Two-run determinism test on fixture (same digest, no clock) | F-17 |
| **FEAT-015** | Reject non-ASCII `adapter.name` (digest scope) | F-17 |
| **FEAT-016** | `conformant` computed only in §3.4 helper (no FAIL ∧ ≥1 PASS) | F-27 |
| **FEAT-017** | Kernel-author first-run block in README + argparse `epilog` (copy-paste three commands) | F-22, F-23 |
| **FEAT-018** | Bounded mark line on every receipt/CLI: “passes gak-conformance/v1, not a security evaluation” | F-08, F-09, spec §8 |
| **FEAT-019** | Deponent scored **via** a §6 adapter in *this* repo; harness must not import `deponent.conformance` | F-24, mission |
| **FEAT-020** | Fixture kernel name distinct from `deponent`; fixture never used as product evidence | F-25 |
| **FEAT-021** | `digest` subcommand: re-hash a receipt file and compare | F-01, spec §5.4 |
| **FEAT-022** | NO_COLOR / non-color status words (argparse 3.14 `color`) | F-22 |
| **FEAT-023** | Golden test: fixture or canned pairs reproduce `de6b7089…` **only** when inputs match Appendix A | F-15 |
| **FEAT-024** | Documented “void if simulated” in README (spec §6.3) | F-25 |
| **FEAT-025** | Extra-probe tests (non-literal equivalent ALLOW/BLOCK) behind the same clause IDs — optional hardening | F-26 |

### Hypotheses to add

| ID | Hypothesis | Falsify by |
|---|---|---|
| **HYP-001** | Third-party implementers will compact JSON or apply RFC 8785 and miss `de6b7089…` | Cross-language digest fixture; pin separators in spec comments + code |
| **HYP-002** | `--adapter` will be treated as a data plugin; someone will add pickle/`eval`/file-path load | Code search gate: no `pickle`, `eval`, `exec` in loader |
| **HYP-003** | Author Deponent receipts will be mistaken for a third-party verdict | README + receipt `kernel` + campaign language |
| **HYP-004** | A pass-all fixture will be used to mint real marks | Fixture name + selfcheck not emitting `GAK-conformant` for `deponent` |
| **HYP-005** | Kernels will special-case literal anchors (`crypto/vault.py`, `rm -rf /`) | Extra-probe tests (FEAT-025); spec §4 already normative |
| **HYP-006** | Adding ISO timestamps “for audit” will break two-run equality | Determinism test fails if any clock field appears |
| **HYP-007** | CI users will expect exit 0 on “harness ran” even when `conformant: false` | Document + test: FAIL receipt → exit 1 |
| **HYP-008** | `console_scripts` without `__main__` will make `python3 -m` fail | FEAT-002 test |
| **HYP-009** | Import-time Deponent/network will break offline `--help` | Test `python3 -m gak_conformance --help` with `deponent` absent |
| **HYP-010** | A 0–10 or % score will be requested and will hide a single FAIL | Refuse aggregate; keep boolean mark |
| **HYP-011** | Wrapping receipts in in-toto/SLSA will pull `startedOn` into the hashed bytes | Envelope, if any, is outside §5.3 |
| **HYP-012** | All-NA adapter will be reported conformant if §3.4 is not centralized | Unit test empty supports + wrong profile |
| **HYP-013** | `ensure_ascii=False` or `indent=2` in digest path will ship by accident | Golden digest test |
| **HYP-014** | Path-like `--adapter ./foo.py:Bar` will be “helpfully” accepted and become ACE-by-file | Grammar reject test |
| **HYP-015** | Color-only PASS/FAIL will fail non-color / screen-reader use | FEAT-022 |

### Explicitly out of v0 backlog (do not open)

- SLSA provenance documents / DSSE signing
- SPDX/CycloneDX document emit (except SPDX license string in pyproject)
- OpenSSF Scorecard port or GitHub API checks
- CIS-CAT / XCCDF XML
- CISA SSDF form mapping
- Common Criteria PP/ST
- ASVS L1–L2–L3
- v1.1 `GAK-AUDIT-CONTENT-BLIND` as required
- PyPI publish (halt-list)
