# Official Cosign prepared — Wanna San / 6631503097

Mac architecture checked: arm64. Official Sigstore release v3.1.4, published 20 October 2026; asset cosign-darwin-arm64. Prepared at:

`/private/tmp/week12-tools/cosign/v3.1.4/cosign`

This explicit path works without changing PATH, system directories, instructor sources or the original wk06 worktree. The /private/tmp tool location is temporary and should be rechecked before later use.

## Verification completed

SHA-256: `9f9b8cd557cf2e5b3df3373a00baa005a86b02391e3e06dd0ce37b3a1533d3a4`.

Matched the official release checksum manifest and GitHub release-asset API digest before execution. Checksums and signature bundle assets also matched API digests. `version` reports v3.1.4, darwin/arm64, commit 0e48502cf5ef34e2e60bbd3617aa19945712f705. Version and sign/verify/verify-blob help commands all exited 0.

The official binary's existing signature bundle was additionally verified (exit 0, “Verified OK”) against documented release identity `keyless@projectsigstore.iam.gserviceaccount.com`, issuer `https://accounts.google.com`. This is the upstream release signer, NOT the student's intended signing identity. Verification reads existing public proofs and creates no signature, OIDC session or transparency-log entry. Bootstrap trust was the official HTTPS release source plus its published checksums; an independent artifact-key/TUF bootstrap was not performed, so self-verification is supplementary evidence rather than an independent bootstrap trust anchor.

Logs, public release metadata, checksum records, signature verification command/results and GHCR private recheck: `evidence/cosign-install/`. Binary/checksum/bundle downloads remain outside Git at /private/tmp/week12-tools/cosign/v3.1.4/.

## Exact artifact

`ghcr.io/6631503097/week12-supplychain@sha256:f882526a88d1b808cbfc563a54f78db1650d10e6d025d7175b8cd0ed10e2e8a6`

The abbreviated reference in the request was resolved using verified publication evidence, not guessed. GHCR was rechecked and still returns visibility=private.

## Commands prepared — NOT executed

The following signing command is digest-pinned. `--oidc-disable-ambient-providers` ensures it does not accidentally consume an ambient CI identity. In the interactive browser flow choose GitHub. The installed version's `--oidc-provider` flag does NOT offer a generic interactive `github` provider, so no unsupported `--oidc-provider github` flag is used. No `--yes` is included; signing/transparency consent remains visible.

```bash
COSIGN=/private/tmp/week12-tools/cosign/v3.1.4/cosign
REF='ghcr.io/6631503097/week12-supplychain@sha256:f882526a88d1b808cbfc563a54f78db1650d10e6d025d7175b8cd0ed10e2e8a6'
"$COSIGN" sign --oidc-disable-ambient-providers \
  --bundle /private/tmp/software-security-wk12/submission/week12-6631503097/evidence/task3-signing/image.sigstore.json \
  "$REF"
```

Create the task3-signing evidence directory only when signing is authorized. This command will authenticate, obtain a Fulcio certificate, sign the digest, upload signature material to the private registry and create public signing/transparency metadata. It must not run merely as a login or dry run.

Exact-policy verification command (NOT executed; expected identity confirmed by student):

```bash
COSIGN=/private/tmp/week12-tools/cosign/v3.1.4/cosign
REF='ghcr.io/6631503097/week12-supplychain@sha256:f882526a88d1b808cbfc563a54f78db1650d10e6d025d7175b8cd0ed10e2e8a6'
SIGNER_EMAIL='6631503097@lamduan.mfu.ac.th'
"$COSIGN" verify \
  --certificate-identity "$SIGNER_EMAIL" \
  --certificate-oidc-issuer 'https://github.com/login/oauth' \
  "$REF"
```

The student confirmed `6631503097@lamduan.mfu.ac.th` as their verified GitHub email and authorized its use as the expected identity for preparation only. This is student confirmation, not an observed issued certificate. Do not use username 6631503097 or guess a noreply email. Check the issued certificate matches the preselected expected email/issuer; stop on mismatch rather than widening the policy. The expected interactive GitHub certificate issuer follows Sigstore's verification guidance; it is distinct from the broker URL oauth2.sigstore.dev/auth and the GitHub Actions issuer.

## Browser flow and public disclosure

After explicit approval, Cosign uses an ephemeral key and opens a browser or provides an authentication link. The student selects GitHub, verifies the browser is on the expected authentication site, signs in as 6631503097, and completes any password/passkey, 2FA and authorization consent. Cosign obtains an identity token and requests a short-lived Fulcio certificate, then signs and submits transparency metadata. Do not screenshot authentication links with sensitive parameters, authorization codes, tokens or secrets; capture sanitized completion/results instead.

The email can become publicly visible even if hidden in the GitHub profile. Certificate/public key, issuer, validity information, signature, timing/inclusion metadata and digest-related data may be publicly discoverable in certificate/transparency records. Signed container payloads can include the repository reference. Private GHCR visibility does not make those public records private or removable. Image layers and the entire SBOM are not automatically published in the public log by this signing command.

## Remaining gates

1. Expected email confirmed for preparation: `6631503097@lamduan.mfu.ac.th`. Explicit approval for signing and public disclosure remains required.
2. Student explicitly approves signing the exact digest, signature storage and public Sigstore metadata.
3. Student personally completes browser OIDC/2FA when signing is subsequently started.

No signing or OIDC login has been run. No new Sigstore entry, Git commit/push or PR was created. Instructor files and original wk06 worktree were not modified.

Official sources:
- https://github.com/sigstore/cosign/releases/tag/v3.1.4
- https://docs.sigstore.dev/cosign/system_config/installation/
- https://docs.sigstore.dev/quickstart/verification-cheat-sheet/
- https://docs.sigstore.dev/certificate_authority/oidc-in-fulcio/
- https://blog.sigstore.dev/privacy-in-sigstore-57cac15af0d0/
