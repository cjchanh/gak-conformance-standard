# Primary-source research — conformance receipts and packaging

Source: grok-fleet `grok_research` task `grk_8b1c4f6c2ff845ccb974b29c43f94628` on 2026-08-12.
Claim class: mixed `official_fact` (cited specs) + `inference` (design implications).

## Copy

- **CIS-style / Scorecard / ASVS**: named clauses, mechanical pass/fail/NA, profile selection, fail-closed aggregate.
- **SLSA / in-toto**: bind a claim to a content digest. Do not require build-platform provenance or signing for v0.
- **PEP 621**: `pyproject.toml` `[project]` metadata; `python3 -m gak_conformance` must work from a clone without a network install.
- **Fail-closed CLI**: exit 0 only when conformant; nonzero otherwise.

## Do not copy

- SPDX / CycloneDX as the *receipt* schema (inventory ≠ clause verdict).
- Required Sigstore / DSSE / cosign.
- Live GitHub Scorecard or CIS-CAT commercial scanner.
- CISA SSDF legal self-attestation form as a mechanical PASS.
- Fuzzy 0–10 composite as the gate.
- Compact JSON (`separators=(',', ':')`) as the digest bytes — **measured later: that breaks `de6b7089…`**.

## Direct backlog changes

- FEAT-0009 / FEAT-0032: freeze v1 13 clauses; reject Deponent extras as GAK clauses.
- FEAT-0005 / HYP-0010: digest = `json.dumps(..., sort_keys=True)` default separators.
- FEAT-0021 / FEAT-0038: `--adapter module:Class` is import-time code exec; document residual risk; no pickle.
- FEAT-0029: stdlib-only, Apache-2.0, no paid APIs.

## Sources (official)

| Source | Date / version | URL |
|---|---|---|
| SLSA spec v1.0 | 2023-04-19 | https://slsa.dev/spec/v1.0/ |
| in-toto attestation | v1.x | https://github.com/in-toto/attestation |
| SPDX 3.0.1 | 2024 | https://spdx.github.io/spdx-spec/v3.0.1/ |
| CycloneDX 1.7 / ECMA-424 | 2025-10-21 | https://cyclonedx.org/specification/overview/ |
| OpenSSF Scorecard checks | current | https://github.com/ossf/scorecard/blob/main/docs/checks.md |
| NIST SP 800-218 SSDF v1.1 | 2022-02 | https://csrc.nist.gov/pubs/sp/800/218/final |
| CISA Secure Software Attestation Form | 2024-03 | https://www.cisa.gov/secure-software-attestation-form |
| OWASP ASVS 5.0.0 | 2025-05 | https://owasp.org/www-project-application-security-verification-standard/ |
| PEP 621 | 2020-11 (Final) | https://peps.python.org/pep-0621/ |
| Python json module | current | https://docs.python.org/3/library/json.html |
