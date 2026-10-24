> Status update: the newly authorized local build and SBOM are now complete; see the Task 3 section in `week12-tasks0-2.md`. Registry publication and signing remain unperformed. The preparation notes below record the earlier plan.

# Task 3 preparation — Wanna San, 6631503097, The Imposters

Prepared 24 October 2026 after Task 2's three browser screenshots were verified. No build, SBOM generation, registry login, publication or signing was performed.

## Actual readiness checks

- Docker Desktop 4.73.0 / Engine 29.4.3 responds. The desktop-linux builder is running BuildKit v0.29.0 and advertises linux/arm64 and linux/amd64 support.
- `python:3.9-slim` and `aquasec/trivy:latest` are cached. `week12-supplychain:lab` is not built. Build success remains untested; dependency downloads need network access, and old pins/tooling may encounter compatibility failures.
- The instructor Dockerfile uses python:3.9-slim and installs the original requirements.txt. app.py, requirements.txt and Dockerfile exist and are unchanged. No running service or port publication is needed.
- Host volume reports approximately 17 GiB available (91% used). Docker system df reports 10.28 GB of images and 7.209 GB build cache; these figures are usage, not free space inside the VM. No cleanup was performed.
- Installed Trivy container help confirms `--format cyclonedx`, `--image-src docker`, and `--input` for a saved image archive. This help invocation did not scan anything.
- Docker credential-store configuration was inspected without reading secrets: see `evidence/task3-preflight/registry-auth-summary.json`. Login validity, namespace ownership and package push permissions remain unverified.

All commands, stdout, stderr and statuses are in `evidence/task3-preflight/`.

## Local build and SBOM plan — commands NOT executed

From `/private/tmp/software-security-wk12/labs/week12-supply-chain`:

```bash
docker build -t week12-supplychain:lab .
```

Then generate the worksheet's CycloneDX inventory with the existing Trivy image, using the Docker daemon as its image source and writing the artifact into the submission evidence folder:

```bash
docker run --rm \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -v /private/tmp/software-security-wk12/submission/week12-6631503097/evidence:/evidence \
  aquasec/trivy:latest image --image-src docker \
  --format cyclonedx --output /evidence/sbom.cdx.json week12-supplychain:lab
```

Alternative: `docker save` the built image into an evidence tar archive, then run the same Trivy container with `image --input /evidence/image.tar --format cyclonedx ...`. This avoids mounting the Docker socket but uses extra disk space. Both inventory methods are local and need no GHCR publication. Inspect Flask's component and preserve tool/image versions, full logs, statuses and identity screenshots.

## Proposed private GHCR destination

`ghcr.io/6631503097/week12-supplychain:lab`

The name is proposed, not created or checked remotely. For a new GHCR package the documented default visibility is private. Confirm the name is unused or an existing package is private before publication; do not assume a tag makes a public package private. Repository permissions and package visibility are separate settings.

For local publishing/signature upload, authenticate as 6631503097 with a short-lived classic PAT scoped to `write:packages` (which includes package read/upload capabilities), with package write access. Do not request `delete:packages` or broad repository access for this lab. If applicable, authorize SSO. Use Docker's host credential helper and `docker login ghcr.io -u 6631503097 --password-stdin` with a token supplied privately; never paste credentials into chat, reports, screenshots or shell history. A GitHub web/CLI login does not by itself establish Docker registry authentication. A containerized Cosign also needs an explicit working registry-credential/helper strategy; a Docker socket mount does not supply that.

For a future Actions workflow, use repository-scoped GITHUB_TOKEN with `packages: write`, and `id-token: write` for keyless OIDC, rather than storing a PAT where avoidable. That workflow is outside the current task.

Source: https://docs.github.com/en/packages/working-with-a-github-packages-registry/working-with-the-container-registry

## Signing/OIDC and public logging — later approval required

Registry authentication authorizes image/signature storage; browser OIDC authentication establishes the signing identity. They are separate. The student completes browser login/2FA. Keyless Sigstore uses a short-lived Fulcio certificate and public Rekor transparency records. Signing identity/certificate and verification metadata, including digest-related information, can become publicly discoverable even if the GHCR image is private. Private GHCR visibility does not make Sigstore's public log private or make logged metadata deletable.

Choose the expected certificate identity and issuer before signing; verify the exact registry digest with that policy rather than `.*` wildcards. OIDC, image publication and public signing/transparency disclosure require explicit authorization. No such action is authorized by this preparation step.

Sources: https://docs.sigstore.dev/cosign/signing/overview/ ; https://blog.sigstore.dev/privacy-in-sigstore-57cac15af0d0/

## Exact next action

Authorize the local Docker build and CycloneDX SBOM generation only. These can complete Task 3's inventory portion without GHCR credentials or publication. Separately confirm the proposed private GHCR destination and authorize publication/signing only when ready for the verification-PASS portion. Do not run sign.sh blindly against the local-only image.
