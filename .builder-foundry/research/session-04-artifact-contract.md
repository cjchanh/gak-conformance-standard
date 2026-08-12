# GAK v0 — Session 4 primary-source research (artifact types)

**Lane:** architecture / research
**Window:** official sources retrieved 2026-08-12
**This wave changes:** inbound receipt vs certification contract; verify inherits `harness_version`.

## Bottom line

| Decision | Why | What we will not do |
|---|---|---|
| Type-check inbound JSON on `digest` / `verify` | SLSA v1.2 verifying-artifacts step 3: verify `predicateType` is the expected URI before treating the object as provenance. A receipt is not a certification. | Auto-detect; hash either object |
| Inherit claimed harness from the certification | SLSA: compare provenance fields to expectations; `buildType` tells the verifier how to interpret parameters. The cert's `harness_version` is the claimed predicate. A CLI default must not silently override it. | Require the operator to restate v1.1 |
| Type error is exit 2 | "Could not score/hash." Kernel drift remains exit 1 (D-004). | Collapse type errors into mismatch |
| No signatures / DSSE / TSA | Mission: offline SHA-256 content digest. Copy the *type check*, not the envelope. | Cosign, Rekor, timestamp authorities |

## F-40 Verifiers check predicate type before trusting the object

- **Source:** [SLSA v1.2 Verifying artifacts](https://slsa.dev/spec/v1.2/verifying-artifacts) (retrieved 2026-08-12)
- **Claim class:** official_fact · **Confidence:** high
- **Claim:** After signature and subject checks, the verifier "Verify that the predicateType is `https://slsa.dev/provenance/v1`." Unrecognized `externalParameters` SHOULD cause verification to fail.
- **Implication:** `verify --cert` must refuse a §5.1 receipt. `digest --receipt` must refuse a §5.2 certification. Do not hash a typed-wrong object and exit 0.
- **Do not copy:** signature roots of trust, Sigstore, builder identity maps. GAK v0 has no signatures.

## F-41 in-toto validation model is fail-closed on type

- **Source:** SLSA v1.2 links the envelope check to [in-toto attestation validation model](https://github.com/in-toto/attestation/blob/main/docs/validation.md#validation-model) (retrieved via SLSA page 2026-08-12)
- **Claim class:** official_fact · **Confidence:** high
- **Claim:** Validation distinguishes envelope, statement, and predicate. A type mismatch is not "subject drifted."
- **Implication:** Exit 2 for wrong artifact kind; exit 1 only after a well-typed certification is compared to a live re-score.
- **Do not copy:** DSSE payloadType, PAE encoding, X.509.

## F-42 Expectations come from the claim object, not a hidden CLI default

- **Source:** SLSA v1.2 Verifying artifacts, "Check expectations" / "Forming expectations" (retrieved 2026-08-12)
- **Claim class:** inference from official_fact · **Confidence:** high
- **Claim:** Verifiers compare provenance to expected `buildType` and parameters. A default that disagrees with the object's declared type produces a false failure or a false pass.
- **Implication:** `verify` inherits `harness_version`. An explicit `--harness` that disagrees is a usage error (exit 2), not kernel drift (exit 1).
- **Do not copy:** trust-on-first-use policy stores, producer-defined remote expectation APIs.

## F-43 What not to copy from the supply-chain stack

- **Sources:** SLSA v1.2 verifying-artifacts (signatures, roots of trust); mission / A-007 / D-004 / CUT-04
- **Claim class:** inference · **Confidence:** high
- **Do not copy:** Cosign/DSSE envelopes, Rekor, TSA timestamps (receipts have no timestamp), network monitors, VSAs as a substitute for re-running the kernel, a new `explain` command.

## F-44 Cosign CVE-2026-39395 — type mismatch said Verified OK

- **Source:** [GHSA-w6c6-c85g-mmv6](https://github.com/sigstore/cosign/security/advisories/GHSA-w6c6-c85g-mmv6) (published 2026-04-06)
- **Claim class:** official_fact · **Confidence:** high
- **Claim:** `verify-blob-attestation` reported Verified OK for malformed payloads or mismatched predicate types. `--type` could be bypassed. Workaround `--check-claims=true` was opt-in.
- **Implication:** Type check is mandatory, not a flag. Digest/verify must never print a hash or VERIFIED for the wrong object kind.
- **Do not copy:** optional claim checks; succeed-if-field-looks-like-hex.

## Measured here (this campaign)

See `.builder-foundry/evidence/artifact-type-confusion.json`. Silent wrong identity: v1.1 receipt/cert digested under default v1 → `d35b3247…` exit 0 vs published `cf26befe…`.
