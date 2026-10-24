# GHCR authentication and Cosign plan — Wanna San / 6631503097

Preparation only, 24 October 2026. Existing evidence and instructor sources were not modified. No image publication, registry login, OIDC authentication, signature or transparency entry was performed.

## Actual read-only checks

- Docker uses the Desktop credential helper. No ghcr.io credential was returned by that helper, and no matching Docker auth entry exists. No credential/token/error body was printed or written to disk by these checks.
- Existing GitHub CLI session authenticated successfully as `6631503097` (personal account). Its token scopes are `gist, read:org, repo`, without package scopes.
- GET target package metadata returned HTTP 404; listing the authenticated account's container packages returned HTTP 403. Because package access is absent, 404 does not establish that the target is unused or private. Creation/push permission is NOT verified.
- The existing credential could not read verified email metadata. Exact signing email is unknown. Do not substitute the GitHub username or a guessed noreply address.
- Neither a native Cosign binary nor the instructor's Cosign container is available locally. Choose/install an official version and record its version before later signing. Native Cosign is preferable here because it can use Docker Desktop's host credential helper; merely mounting ~/.docker/config.json into a Linux container would not supply the macOS credential-helper executable or Keychain access.

## Authentication — student action needed

1. Sign in to GitHub as 6631503097, complete any password/passkey/2FA/re-authentication, and create a short-lived PAT **classic** for GHCR. Minimum publishing permission: `write:packages` (package read capability is included). Confirm the resulting scopes; remove automatically selected broad `repo` scope where it is unnecessary. No `delete:packages` is required. This is not a fine-grained PAT workflow. If SSO applies, authorize the token for it.
2. Use a private host Terminal, with shell tracing disabled. Never paste the token into chat, a source file, a command argument, or a screenshot. The following prompts without echo and passes it only through stdin to Docker; Docker Desktop stores login credentials in its configured helper, outside the repository:

```bash
python3 - <<'PY'
import getpass, subprocess
secret = getpass.getpass('GHCR classic PAT (hidden): ')
try:
    result = subprocess.run(
        ['docker', 'login', 'ghcr.io', '-u', '6631503097', '--password-stdin'],
        input=secret + '\n', text=True,
    )
finally:
    secret = None
raise SystemExit(result.returncode)
PY
```

This command is provided for the student; it has NOT run. Login is authentication, not permission to publish. Do not use a registry token as an OIDC token.
3. Recheck account identity, credential validity, granted package scopes, and the target package's visibility with read-only API/registry calls. If a package-scoped API credential is needed, use it from the host credential helper in memory, never log token bodies or put it in the repository. Do not overwrite the existing GitHub CLI session just to add package access. Check for pagination if listing packages.
4. Confirm the verified GitHub email you intend to make public through Sigstore. It is not necessary to expand the existing GitHub CLI token just to tell the verifier this email; inspect GitHub Settings → Emails yourself and confirm it.

## Private visibility gate — required BEFORE any push

Target: `ghcr.io/6631503097/week12-supplychain:lab`.

GitHub documents first publication of a new GHCR package as private by default; there is no separate empty-package creation step in the documented Docker push workflow. For an existing package, check actual private visibility and write access first. Repository visibility alone is not evidence of package visibility. If the package is already public, do not push this image to it: stop and resolve visibility or choose a confirmed unused new name. Do not rely on changing visibility after a public push, because it cannot undo exposure. With valid package scopes, establish either that the name is new (successful authenticated listing/metadata checks) or that it is an existing private package the user can write. If ambiguity remains, stop.

For a confirmed new name, after explicit publication approval, first push uses GitHub's documented private default; immediately verify API `visibility=private`. Abort further actions if that cannot be confirmed. Account ownership and scopes establish prerequisites, but a successful push cannot be proven without the later authorized write operation.

## Digest-pinned publication/signing workflow — NOT executed

Gate A: separate explicit approval for private image publication, once identity/scopes/privacy checks pass.

```bash
LOCAL_ID=sha256:f882526a88d1b808cbfc563a54f78db1650d10e6d025d7175b8cd0ed10e2e8a6
IMAGE=ghcr.io/6631503097/week12-supplychain
docker image inspect "$LOCAL_ID"  # recheck the recorded local artifact
docker tag "$LOCAL_ID" "$IMAGE:lab"
docker push "$IMAGE:lab"         # STOP: publication approval required
```

Record the actual registry digest returned by the approved push and independently retrieve the registry manifest's digest. Confirm package visibility before proceeding. Do not guess it from the local tag or substitute a single-platform config digest; registry media-type/index handling can matter. Bind the pushed reference to the locally built artifact, record the comparison, and stop on an unexplained mismatch. Reuse the verified SBOM only after that association is established.

```bash
IMAGE=ghcr.io/6631503097/week12-supplychain
DIGEST='sha256:<actual-verified-registry-digest>'
REF="$IMAGE@$DIGEST"
SIGNER_EMAIL='<confirmed-verified-GitHub-email>'
ISSUER=https://github.com/login/oauth
```

Gate B: separate explicit approval for keyless signing, including the exact email and public logging consequences. Install/pin an official native Cosign release, record `cosign version`, and confirm it can read the host registry credential helper. Then run in an interactive host Terminal:

```bash
cosign sign --bundle image.sigstore.json "$REF"  # STOP: signing/logging approval required
# Student selects GitHub and completes login/2FA/consent.
cosign verify --certificate-identity "$SIGNER_EMAIL" \
  --certificate-oidc-issuer "$ISSUER" "$REF"
```

The standard interactive GitHub verification policy uses certificate issuer `https://github.com/login/oauth` and the exact email supplied by the GitHub connector. The login broker endpoint `https://oauth2.sigstore.dev/auth` is not interchangeable with that certificate verification issuer. Confirm the actual certificate SAN/issuer and reject unexpected values; do not relax to `.*` or dynamically trust whatever identity signed. An actual GitHub Actions workflow would use a different issuer (`https://token.actions.githubusercontent.com`) and workflow-URI identity, and is not this local interactive workflow.

The planned verify checks the exact image digest, expected identity and issuer, trusted Sigstore chain and transparency proof. Preserve certificate/bundle and sanitized result output after authentication, never bearer tokens, passwords or login codes. A later negative signature test must distinguish a real signature rejection from an auth/network/usage failure.

## Public metadata and human-only steps

Public-good Sigstore keyless signing can disclose the signer email (even one hidden on GitHub), certificate issuer and validity information, public key/certificate, signature, timing/log inclusion data, and artifact/payload digest-related information. Signed container payloads may identify the image repository reference and digest. Private GHCR access does not make the public certificate/transparency records private or removable. The image layers and full SBOM are not automatically uploaded to Rekor just because the image is signed; do not attach sensitive annotations/attestations without reviewing their disclosure. `--upload=false` only changes registry signature upload and must not be treated as a no-public-log mode.

The student completes GitHub token creation, any reauthentication/2FA, Docker login hidden prompt, confirmation of the verified email, and later browser OIDC login/2FA/consent. The current preparation does not approve image publication or signing. Get explicit approval at each gate.

## Sources

- https://docs.github.com/en/packages/working-with-a-github-packages-registry/working-with-the-container-registry
- https://docs.sigstore.dev/quickstart/verification-cheat-sheet/
- https://docs.sigstore.dev/certificate_authority/oidc-in-fulcio/
- https://docs.sigstore.dev/cosign/signing/signing_with_containers/
- https://blog.sigstore.dev/privacy-in-sigstore-57cac15af0d0/
