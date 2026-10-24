# Week 12 — Tasks 0–2

Student: Wanna San | ID: 6631503097 | Group: The Imposters

AI disclosure: Codex created the isolated workspace, ran tools, extracted scanner results, and drafted this report. Review and explain these findings in your own words before submission. No final PDF, commit, push, PR, signing, or registry publication was performed.

## Workspace and environment

Branch `wk12` at upstream/main `eff680baf8d5f85e6cd736da776fb9d40e61c043`, fetched during this session. Worktree: `/private/tmp/software-security-wk12`. The original `wk06` checkout and its unrelated edits were preserved. Instructor sources were not edited.

Actual environment: macOS 27.0.1, ARM64; Docker Desktop 4.73.0 / Engine 29.4.3 (Linux ARM64), context desktop-linux; Git 2.54.0; Bash 3.2.57; host Python 3.13.2; Node v22.19.0. Actual containerized tool checks: Trivy 0.74.0, pip-audit 2.9.0, Python 3.9.25 (pip-audit version checked in a fresh container immediately after the scan). Scanner image digests are recorded in `evidence/environment/`. Identity command output is recorded there, but a text transcript does not satisfy the screenshot requirement.

## Task 0 — intentionally outdated packages

| Package | Pinned version | OWASP | CWE interpretation |
|---|---|---|---|
| Flask | 1.1.4 | A03:2025 | CWE-1104; CWE-1395 where confirmed vulnerable |
| Werkzeug | 1.0.1 | A03:2025 | CWE-1104; CWE-1395 where confirmed vulnerable |
| Jinja2 | 2.11.3 | A03:2025 | CWE-1104; CWE-1395 where confirmed vulnerable |
| MarkupSafe | 2.0.1 | A03:2025 | CWE-1104; CWE-1395 where confirmed vulnerable |
| itsdangerous | 1.1.0 | A03:2025 | CWE-1104; CWE-1395 where confirmed vulnerable |
| click | 7.1.2 | A03:2025 | CWE-1104; CWE-1395 where confirmed vulnerable |
| requests | 2.25.1 | A03:2025 | CWE-1104; CWE-1395 where confirmed vulnerable |
| urllib3 | 1.26.4 | A03:2025 | CWE-1104; CWE-1395 where confirmed vulnerable |
| PyYAML | 5.4.1 | A03:2025 | CWE-1104; CWE-1395 where confirmed vulnerable |

These are deliberate teaching pins, rather than production recommendations. A03 describes supply-chain exposure; CWE-1104 concerns unmaintained components and CWE-1395 concerns components with known vulnerabilities. Age alone does not prove a vulnerability or that each component is unmaintained; scanner-confirmed findings are listed separately below.

Remediation note: Treat the pins as a baseline for identifying affected components, then select mutually compatible patched releases and lock every resolved dependency with reviewed hashes. Upgrade and test in a separate defense artifact rather than silently replacing the instructor's intentionally vulnerable target.

Evidence: original manifest and package table in `evidence/task0/`; genuine identity-stamped screenshot: `evidence/screenshots/task0.png`.

## Task 1 — actual SCA results

Command: `cd labs/week12-supply-chain && bash sca_scan.sh`, with a PATH wrapper around Docker that preserves arguments and captures each subprocess's complete stdout/stderr and exit status. Wrapper source is in `support/docker`; no instructor code was changed. All Docker invocations had a 600-second timeout; none timed out.

- Trivy filesystem scan: **11 HIGH, 0 CRITICAL**, exit **0**. This command does not configure a nonzero vulnerability exit code.
- pip-audit: **33 known vulnerabilities in six packages**, exit **1** because vulnerabilities were found, not a tool crash. Includes the transitive package idna, absent from the nine direct pins.
- Optional image inspection: exit **1**, because `week12-supplychain:lab` does not exist. Image scan was skipped; no build was attempted for Tasks 0–2.
- Instructor script: exit **0** because scanner failures/statuses are masked by `|| true`.

### Three genuine findings

| Package | Installed version (manifest) | Advisory/CVE | Severity reported by Trivy | Fixed versions reported by Trivy |
|---|---|---|---|---|
| Flask | 1.1.4 | CVE-2023-30861 | HIGH | 2.3.2, 2.2.5 |
| Werkzeug | 1.0.1 | CVE-2023-25577 | HIGH | 2.2.3 |
| urllib3 | 1.26.4 | CVE-2021-33503 | HIGH | 1.26.5 |

Source: first Trivy stdout file referenced by `evidence/task1/process-status.jsonl`; the same output is included in `sca_scan.stdout.txt`. Versions above fix those individual advisories; they are NOT claims that these old releases resolve every present-day finding. Other findings in the full logs require later releases. pip-audit does not supply severity in this table, so no severity was invented for its advisory IDs.

Remediation note: Prioritize the HIGH findings and use the complete worklist when choosing compatible upgrades, since fixing one CVE can leave later advisories unresolved. Scan the resolved dependency tree again after the separately authorized defense change and test the app; map confirmed vulnerable components to A03/CWE-1395.

Trivy warned that no site-packages directory was available, so license detection was skipped. This was a manifest scan, not proof of a built image's full inventory. Preserve stderr as well as the findings table.

## Task 2 — provided dependency-confusion simulation

Only the instructor's `labs/live-quiz/static/sim/resolver-confusion.js` was executed, using a minimal DOM adapter in Node; no package installation, index query, payload or registry was used for this simulation. The adapter models radio-button exclusivity. The original engine check was subsequently supplemented with all three genuine Chrome screenshots below. The student selected the single-index and race presets manually; Codex arranged the windows, refreshed terminal identity, and captured the complete screen.

| Preset/mode | Private | Public | Actual simulation-engine verdict |
|---|---|---|---|
| the attack / merged | 1.4.0 | 99.0.0 | Public 99.0.0 selected — confused |
| single-index defense / single | 1.4.0 | 99.0.0 | Private 1.4.0 selected — public is not considered |
| win the race / merged | 2.0.0 | 1.9.0 | Private 2.0.0 selected — safe this time |

The attacker controls the public version number and can publish a higher version, defeating an internal-version-number race. This is a numeric teaching simulation, not a complete pip/PEP 440 resolver: an exact `==1.4.0` requirement would exclude 99.0.0, and real pip considers compatible candidates and configuration.

Remediation note: Use one curated trusted index and remove additional indexes from environment and configuration, so a public candidate cannot enter this simulated choice (A03/CWE-1357; untrusted inclusion CWE-829). Add a complete reviewed hash lockfile for integrity; one trusted source does not protect against compromise of that source itself.

Engine results and exact explanations: `evidence/task2/engine-results.json`; reproducible runner: `support/simulation-check.cjs`.

## Verified screenshot evidence — Task 2 complete

All images are original full-display macOS screencapture PNGs, visually verified with real Chrome and the exact identity command/output in an adjacent Terminal. No cropping, compositing, generated images, or invented verdicts were used. Capture times below are Asia/Bangkok on 24 October 2026.

| Mode/preset | Accepted original PNG | Capture time |
|---|---|---|
| Attack, merged, private 1.4.0/public 99.0.0 | `evidence/screenshots/task2-attack-merged-attempt3.png` | 14:07:13.275481 +07 (original PNG filesystem timestamp) |
| Single index, same versions | `evidence/screenshots/task2-single-index-confirmed.png` | 14:56:09.829440 +07 |
| Win the race, private 2.0.0/public 1.9.0 | `evidence/screenshots/task2-race-confirmed.png` | 14:59:27.318136 +07 |

Task 0 and Task 1 screenshots are also saved and visually verified: `task0.png`, `task1-trivy.png`, and `task1-pip-audit.png`. Task 1 screenshots accurately label the displayed output as preserved genuine scan logs.

Chrome blocked AppleScript JavaScript; native accessibility automation did not reliably change presets. The student manually selected the final two states, and Codex verified the actual visible outcomes. Rejected attempts are preserved and explicitly excluded in `evidence/task2/visual-review.json`. Capture timestamps and hashes are recorded in that file and `captures.jsonl`.

## Next step

Tasks 0–2 are complete. Task 3 is prepared only; see `task3-preparation.md`. No image build, SBOM generation, publication, signing, commit, push, or PR has been performed. Instructor files remain unchanged and the original wk06 working tree was not touched.


## Task 3 — local image build and SBOM complete; signing pending

Student: Wanna San | 6631503097 | The Imposters. Completed local portion on 24 October 2026. Earlier statements about Task 3 being preparation-only describe the prior session; this section records the newly authorized local execution.

### Exact commands and results

Build cwd: `/private/tmp/software-security-wk12/labs/week12-supply-chain`.

```bash
docker build --progress=plain -t week12-supplychain -t week12-supplychain:lab .
```

Build exit **0**. Local tags: `week12-supplychain:latest` (the requested unqualified name) and `week12-supplychain:lab` (worksheet compatibility). Platform: **linux/arm64**. Docker-reported image ID:

```text
sha256:f882526a88d1b808cbfc563a54f78db1650d10e6d025d7175b8cd0ed10e2e8a6
```

Build logs also distinguish the single-platform manifest and image configuration hashes from the exported manifest-list digest. No registry upload was performed; the build log's “naming to docker.io/library/…” lines are local tagging. Full stdout/stderr: `evidence/task3/build.stdout.txt`, `build.stderr.txt`; command, timing and status: `build-status.json`; immutable image details: `image-inspect.json`.

SBOM generation command:

```bash
docker run --rm -v /var/run/docker.sock:/var/run/docker.sock -v /private/tmp/software-security-wk12/submission/week12-6631503097/evidence/task3:/evidence aquasec/trivy:latest image --image-src docker --format cyclonedx --output /evidence/sbom.cdx.json sha256:f882526a88d1b808cbfc563a54f78db1650d10e6d025d7175b8cd0ed10e2e8a6
```

SBOM generation exit **0**. Artifact: **`evidence/task3/sbom.cdx.json`**, 229683 bytes. SHA-256: `d5df53e8007b432c18f12c5e200af978f422b438673f84199caeaad99451b9a7`. Full command/status and stdout/stderr are in `sbom-status.json`, `sbom.stdout.txt`, and `sbom.stderr.txt`.

### Format validation and component inventory

JSON parsing succeeded. **CycloneDX 1.7**, schema validation **PASS**, **0 errors**, using jsonschema 4.26.0 in a disposable Python environment. Versioned schemas were obtained from the official CycloneDX specification repository; source URLs and hashes, downloaded copies, validator source and logs are preserved. The first schema download from cyclonedx.org returned **HTTP 403 / exit 1**; this failure is retained in `validation-attempt1.stderr.txt`. Retrying the official GitHub schema source succeeded with **exit 0**, recorded in `validation-status.json`.

Inventory: **119 components** — **118 libraries and one operating system**, including **87 Debian packages and 31 Python packages**. Full rows: `component-inventory.tsv`; structured checks: `validation-summary.json`. The top-level container is separately recorded in metadata and is not included in that 119-component array count.

### Flask entry

- Name/version: **Flask 1.1.4**; type: `library`.
- PURL and bom-ref: `pkg:pypi/flask@1.1.4`.
- License metadata: `BSD-3-Clause`.
- Installed metadata path: `usr/local/lib/python3.9/site-packages/Flask-1.1.4.dist-info/METADATA`.
- Reported SHA-1: `caefbe085934d955994ee9bc9d8e4e86cb79c081`. This is tool-reported component metadata, not a signature or a reviewed pip artifact hash lockfile.
- Layer identifiers and complete component JSON: `flask-component.json`.

A separate `docker run --rm --network none --entrypoint python <image-id> ...` read importlib.metadata from the built image, confirming Flask 1.1.4 and its installed metadata path, and Debian 13 / full version 13.1. Exact command, output and exit **0** are in `installed-flask-status.json`, `installed-flask.stdout.txt`, and `installed-flask.stderr.txt`.

### Why this SBOM represents the image

Trivy ran `image --image-src docker` against the immutable Docker image ID, not `fs` against requirements.txt. No source-directory mount was supplied. The SBOM's `aquasecurity:trivy:ImageID` equals Docker inspect's ID, its top-level component is a container, and its components include installed Python METADATA paths, layer identifiers and Debian OS packages absent from requirements.txt. Any Docker-Hub-shaped repository string in metadata comes from local tags; it does not imply publication or remote scanning. This inventory is evidence of detected components in this built image, not a guarantee of exhaustive detection.

### Warnings and limitations

The build warned about pip running as root inside the image, and noted a newer pip release. Trivy reported that CycloneDX output disables vulnerability scanning unless explicitly requested, cautioned that license metadata may have additional terms, and advertised a newer Trivy release (0.76.1 versus the used 0.74.0). Consequently this SBOM is an inventory, not a new vulnerability assessment. No build or SBOM-generation failures occurred; the schema-host HTTP 403 was recovered as recorded above. Instructor sources and intentionally outdated pins were unchanged.

### Evidence screenshots

- `evidence/screenshots/task3-local-build.png` — 24 October 2026 **15:03:47.868887 +07**.
- `evidence/screenshots/task3-sbom-validation.png` — **15:04:35.739359 +07**.

Both are genuine, unmodified full-screen macOS captures showing the exact worksheet identity command and actual output alongside preserved real results. Capture timestamps/hashes: `evidence/task3/captures.jsonl`; visual review: `screenshot-review.json`.

### Incident response and remediation note

An image-linked SBOM lets responders search a newly announced affected package/version, identify impacted builds, and prioritize upgrades without reconstructing each dependency tree during an incident. Including OS and transitive dependencies exposes components that the nine direct requirements omit. For A03/A08, preserve this inventory with the exact image identity, remediate vulnerable components, and later verify an authorized signature before deployment; an SBOM alone neither proves trusted provenance nor blocks a malicious but signed upstream component.

### Remaining Task 3 work and approval boundary

The local image and SBOM portion is complete. Signature PASS, unsigned-image rejection, and deployment verification policy remain pending; no Cosign or OIDC command has run. To proceed later, separately approve (1) publication to `ghcr.io/6631503097/week12-supplychain:lab` with private package visibility verified, (2) registry authentication using privately supplied credentials with package write permission, and (3) keyless signing with the chosen OIDC identity and public transparency-log disclosure. OIDC login does not replace registry login. Public certificate/signing identity and digest-related metadata may be discoverable even for a private GHCR image. Obtain the actual registry digest after an approved push and verify against the expected certificate identity and issuer, not unrestricted regexes. No tokens were created or used, and no image/Git push, commit, PR, final PDF, publication or signing was performed.


## Task 3 — approved private GHCR publication completed

Student: Wanna San | 6631503097 | The Imposters. On 24 October 2026 the student explicitly approved image publication only. This section supersedes earlier preparation-only/publication-pending statements; signing remains pending.

Before pushing, Docker inspect's local image ID was checked against the previously built and SBOM-verified ID `sha256:f882526a88d1b808cbfc563a54f78db1650d10e6d025d7175b8cd0ed10e2e8a6`. It matched. Authentication identified account 6631503097; authenticated package listing and metadata checks confirmed the name was absent before first publication.

Executed commands:

```bash
docker tag sha256:f882526a88d1b808cbfc563a54f78db1650d10e6d025d7175b8cd0ed10e2e8a6 ghcr.io/6631503097/week12-supplychain:lab
docker push ghcr.io/6631503097/week12-supplychain:lab
```

Both commands exited **0**. Full unmodified stdout/stderr, exact commands and timestamps are in `evidence/task3-publication/`. Docker reported:

```text
lab: digest: sha256:f882526a88d1b808cbfc563a54f78db1650d10e6d025d7175b8cd0ed10e2e8a6 size: 856
```

Immediately after the successful push, the authenticated GitHub package API returned **HTTP 200**, name `week12-supplychain`, type `container`, visibility **`private`**, checked at `2026-10-24T09:07:23.537326+00:00` (16:07:23 +07). No visibility changes were made. The raw nonsecret check summary is `immediate-visibility.json`.

An independent authenticated registry GET of the `lab` manifest returned HTTP 200 and an OCI image index. Its `Docker-Content-Digest` header, SHA-256 computed from the exact returned bytes, push digest and verified local image ID all agree:

```text
ghcr.io/6631503097/week12-supplychain@sha256:f882526a88d1b808cbfc563a54f78db1650d10e6d025d7175b8cd0ed10e2e8a6
```

Registry verification: `registry-verification.json`; exact manifest bytes: `registry-manifest.json`. The index includes the ARM64 image manifest and the pre-existing BuildKit attestation manifest produced by the authorized local build. Publishing that existing index is not Cosign signing and did not involve Sigstore. The matching top-level digest preserves the association with the existing image SBOM; the original SBOM was not altered.

Genuine evidence screenshot: `evidence/screenshots/task3-private-ghcr-publication.png`, captured **24 October 2026 16:08:20.720510 +07**. The full display shows the exact worksheet identity command/output, preserved real push output, API private visibility and independently verified digest. Original PNG is unmodified; capture timestamps/hashes and visual review are in the publication evidence directory.

No failures occurred during the tag, push or visibility/digest checks. Credentials and bearer tokens stayed in memory and were not printed, saved in the repository or captured. Instructor file hashes remain unchanged; no original wk06 worktree files were written.

### Next requirements — signing is not authorized

Install/select an official pinned Cosign version, confirm the exact verified email used by the intended interactive GitHub signer, and establish exact identity/issuer verification policy (`https://github.com/login/oauth` for the planned interactive GitHub flow). Obtain separate explicit approval for signing this immutable reference, writing signature artifacts and public Sigstore certificate/transparency metadata. The student completes browser OIDC/2FA only after that approval. No Cosign, OIDC, Sigstore entry, Git commit/push, PR or final PDF occurred in this publication step.


## Task 3 — approved keyless signing and exact-policy verification completed

Student: Wanna San | 6631503097 | The Imposters. The student explicitly authorized signing, interactive GitHub OIDC, the exact email, private GHCR signature storage and public Sigstore transparency metadata. Earlier “signing pending” statements describe prior stages and are superseded by this result.

The request's abbreviated @sha256 reference was resolved to the full digest from the previously verified publication evidence. Signed reference:

```text
ghcr.io/6631503097/week12-supplychain@sha256:f882526a88d1b808cbfc563a54f78db1650d10e6d025d7175b8cd0ed10e2e8a6
```

Exact executed signing command:

```bash
/private/tmp/week12-tools/cosign/v3.1.4/cosign sign --yes --fulcio-auth-flow normal --oidc-disable-ambient-providers --bundle /private/tmp/software-security-wk12/submission/week12-6631503097/evidence/task3-signing/image.sigstore.json ghcr.io/6631503097/week12-supplychain@sha256:f882526a88d1b808cbfc563a54f78db1650d10e6d025d7175b8cd0ed10e2e8a6
```

Cosign v3.1.4 signing exited **0**, started `2026-10-24T09:24:19.093210+00:00`, finished `2026-10-24T09:25:10.820585+00:00` (24 October 2026, 16:25:10 +07). `--yes` applied the already explicit user consent, while `--fulcio-auth-flow normal` selected browser interaction and `--oidc-disable-ambient-providers` excluded unintended CI credentials. The student personally completed the browser GitHub authentication/2FA and confirmed login completion. Authentication URLs/codes/tokens and unrecognized progress lines were filtered before display or persistence; raw authentication output was not saved.

Actual retained signing output includes:

```text
Generating ephemeral keys...
Signing artifact...
Wrote bundle to file /private/tmp/software-security-wk12/submission/week12-6631503097/evidence/task3-signing/image.sigstore.json
Pushing signature to: ghcr.io/6631503097/week12-supplychain
```

Bundle: `evidence/task3-signing/image.sigstore.json`. Sanitized genuine combined stdout/stderr: `sign.sanitized-output.txt`; command/status/timestamps: `sign-command.json`, `sign-status.json`. This records a successful upload rather than merely local signing.

Exact executed verification command:

```bash
/private/tmp/week12-tools/cosign/v3.1.4/cosign verify --certificate-identity 6631503097@lamduan.mfu.ac.th --certificate-oidc-issuer https://github.com/login/oauth ghcr.io/6631503097/week12-supplychain@sha256:f882526a88d1b808cbfc563a54f78db1650d10e6d025d7175b8cd0ed10e2e8a6
```

Verification exited **0**. Cosign reported claims validated, transparency-log claims verified offline, and code-signing certificate verified with trusted CA certificates. No wildcard identity or issuer regex was used; the policy was not weakened. Actual certificate extraction from the bundle independently confirms:

- SAN email: **6631503097@lamduan.mfu.ac.th**.
- OIDC issuer extension: **https://github.com/login/oauth**.
- Both exactly match the expected policy.
- Certificate validity: 24 October 2026 09:25:00–09:35:00 UTC (16:25–16:35 +07); verification checked trusted signing/log evidence, not a long-lived signing key.
- Verified claim digest: **sha256:f882526a88d1b808cbfc563a54f78db1650d10e6d025d7175b8cd0ed10e2e8a6**.

Full verification stdout/stderr and status: `verify.stdout.json`, `verify.stderr.txt`, `verify-status.json`; public certificate details: `certificate-public.txt`; summary: `verified-result.json`.

The bundle contains **1 transparency-log entry**, log index **3438951395**, integrated time **1792833901** (Unix seconds), with inclusion proof. This is real public metadata generated under the student's explicit authorization, not a simulation. The bundle uses an in-toto statement with predicate type `https://sigstore.dev/cosign/sign/v1`; it signs the digest and is not automatically a SLSA build-provenance attestation. A signature proves the expected identity signed this artifact; it does not prove the old dependencies are safe.

### Private package and genuine screenshots

The post-sign GitHub API returned **HTTP 200**, package **week12-supplychain**, visibility **private**, at `2026-10-24T09:26:12.256138+00:00`. No visibility change was made.

- `evidence/screenshots/task3-cosign-signing.png` — **24 October 2026 16:26:48.458320 +07**.
- `evidence/screenshots/task3-cosign-verification.png` — **16:27:03.256375 +07**.

Both original full-screen PNGs were visually verified to show the exact worksheet identity command/output with the genuine sanitized signing and verification results. No screenshots were captured during authentication. Capture times/hashes: `evidence/task3-signing/captures.jsonl`; visual review: `screenshot-review.json`.

### Outcome and remaining scope

Signing and exact-policy verification succeeded with no mismatch or command failure. GHCR remains private. The approved public signing/transparency disclosure occurred. No authentication secret was intentionally printed, persisted or screenshotted. No instructor files or original wk06 files were modified; no Git commit, Git push or PR was created.

The worksheet's unsigned-image negative test is still pending and was not run in this signing-only step. Tasks 4, reflections and remaining submission work are outside this action. Stop after reporting these actual results.


## Task 3 — unsigned-image negative test completed

Student: Wanna San | 6631503097 | The Imposters. The instructor's worksheet Task 3 step 3 specifically requires `cosign verify --certificate-identity-regexp '.*' --certificate-oidc-issuer-regexp '.*' python:3.9-slim` to fail with **no signatures found**. Both identity flags are mandatory; a missing-argument/usage error would not satisfy this requirement.

### Confirmed target before verification

The suggested python:3.9-slim image was not assumed unsigned. A direct read of Docker Hub's image manifest succeeded (HTTP 200), and SHA-256 computed from its bytes matched the registry digest header:

```text
index.docker.io/library/python@sha256:2d97f6910b16bd338d3060f261f53f144965f755599aab1acda1e13cf1731b1b
```

Signature discovery for that exact index digest: OCI referrers endpoint **HTTP 200**, `manifests: []`; legacy Cosign signature-manifest location **HTTP 404** with manifest-unknown response, while the image manifest itself exists. Then `cosign tree` exited **0** and reported no supply-chain related artifacts. This confirms absence of discoverable registry Cosign signatures at this exact index digest at the recorded check time, not absence of all possible signing systems or signatures for every platform child. The initial local-cache lookup found no python:3.9-slim image; no pull was needed because this is read-only registry verification.

### Actual commands and outcomes

Worksheet command using installed Cosign v3.1.4:

```bash
/private/tmp/week12-tools/cosign/v3.1.4/cosign verify --certificate-identity-regexp '.*' --certificate-oidc-issuer-regexp '.*' python:3.9-slim
```

Actual exit: **10**. Stderr:

```text
Error: no signatures found
error during command execution: no signatures found
```

A second verification pinned the prechecked digest so that the result is attributable to an immutable image:

```bash
/private/tmp/week12-tools/cosign/v3.1.4/cosign verify --certificate-identity-regexp '.*' --certificate-oidc-issuer-regexp '.*' index.docker.io/library/python@sha256:2d97f6910b16bd338d3060f261f53f144965f755599aab1acda1e13cf1731b1b
```

Actual exit: **10**, with the same **no signatures found** rejection. Both stdout/stderr streams, exact commands/statuses and timings are preserved in `evidence/task3-negative/`. Discovery requests and response bodies are also preserved; registry authentication tokens stayed only in memory.

This is a missing-signature rejection, not an authentication, network, permissions or invalid-argument failure: registry manifest and referrers reads succeeded, `cosign tree` succeeded, both required CLI flags were supplied, and Cosign's actual error specifically names absent signatures. The permissive regexes follow the worksheet to isolate signature absence; they do not replace the existing positive test's strict email/issuer policy. No image was signed or published for the negative test and no prior signing was repeated.

### 3-sentence security explanation — A08 / CWE-829

Our positive verification succeeds because the approved image digest has a valid signature whose certificate matches `6631503097@lamduan.mfu.ac.th` and `https://github.com/login/oauth`, with trusted certificate and transparency evidence. The Python image fails because there is no discoverable Cosign signature to establish that integrity/authenticity evidence, even with the worksheet's permissive identity regexes. Making verification a required pre-deployment gate addresses **OWASP A08:2025 Software or Data Integrity Failures** and helps prevent **CWE-829 inclusion from an untrusted control sphere**, while neither a valid signature nor an SBOM alone establishes that dependencies are vulnerability-free.

### Evidence, privacy and Task 3 completion

Genuine full-screen screenshot: `evidence/screenshots/task3-unsigned-negative.png`, captured **24 October 2026 16:34:56.182638 +07**, visually verified to show the exact worksheet identity command/output in the same image as actual commands and rejection output. Original PNG unchanged; capture hashes/times and visual review are stored in `evidence/task3-negative/`.

The authenticated post-test GitHub API check returned **HTTP 200**, package visibility **private**; see `private-package-check.json`. Instructor file hashes remain unchanged, and no original wk06 files, commits, Git pushes or PRs were touched.

**Task 3 is now fully complete:** image-derived CycloneDX SBOM and Flask component evidence, exact-policy positive signature verification, and genuine unsigned-image negative verification with required screenshots and remediation/security explanations. Task 4 and remaining report/submission sections are separate work and were not performed in this step. Earlier negative-test-pending statements describe prior stages and are superseded here.


## Task 4 — technical defense exercises completed

Student: Wanna San | 6631503097 | The Imposters. The actual Task 4 worksheet and dependency-confusion guide were read before execution. They require a missing-hash refusal against the original requirements.txt, a single-index explanation tied to Task 2, namespace-scoping analysis, and a pre-deploy verification gate.

### Pin + hashes: actual enforcement refusal

A disposable venv at `/private/tmp/week12-task4-hash-20261024` used Python 3.13 / pip 25.0. The pip commands read the original manifest in `/private/tmp/software-security-wk12/labs/week12-supply-chain`; instructor files were not edited. Inherited PIP_* settings were excluded and `PIP_CONFIG_FILE=/dev/null` disabled external configuration. No packages were installed into the main environment.

```bash
/private/tmp/week12-task4-hash-20261024/bin/pip install --require-hashes -r requirements.txt
```

Exit **1**. Actual stderr included:

```text
ERROR: Hashes are required in --require-hashes mode, but they are missing from some requirements.
Flask==1.1.4 --hash=sha256:c34f04500f2cbbea882b1acb02002ad6fe6b7ffa64a6164577995657f50aed22
```

The abbreviated error above quotes its genuine first sentence; the complete refusal and stdout are saved in `evidence/task4/hash-refusal.stderr.txt` and `.stdout.txt`. pip downloaded the Flask wheel to compute its hash, then refused before installing it. `installed-after.stdout.txt` confirms the isolated venv contains **only pip 25.0**. The SHA-256 is the downloaded Flask wheel's actual hash; it is not a reviewed complete lockfile, and printing it does not establish that its source/artifact is trustworthy. Trusted hashes must cover all resolved dependencies and permitted artifacts; a single missing-hash refusal is not a successful installation or demonstrated malicious substitution.

### Single trusted index: actual command and configuration

```bash
/private/tmp/week12-task4-hash-20261024/bin/pip install --require-hashes --index-url https://pypi.org/simple -r requirements.txt
```

Exit **1**, again because the same manifest has no hashes. The explicit CLI index was `https://pypi.org/simple`, with no extra index, inherited index variables or pip config; `single-index-config.*` records the clean configuration and real exit **0**. This exercise uses PyPI as the one source for public lab dependencies, not as a private internal registry. The initial disposable-Docker-image availability checks found no usable cached lab/base image, so the isolated venv approach was used instead; this did not block the required pip demonstration.

For a real team, configure one trusted private/curated proxy index containing authorized internal packages and vetted public dependencies. `--extra-index-url` merges candidates from indexes without making the private source authoritative; pip can choose a higher compatible public version. `--index-url` only excludes alternatives when extra indexes/find-links/direct references in environment, configuration and manifests are also controlled. Exact pins constrain versions but do not by themselves authenticate artifact bytes or origin. Evidence from Task 2 is reused unchanged: `task2-attack-merged-attempt3.png` selects public 99.0.0, while `task2-single-index-confirmed.png` selects private 1.4.0 for the same version pair. No simulated internal package was installed and no private/public attack registries were queried.

### Namespace scoping — written defense draft

Use an organization-specific internal naming convention and restrict internal distribution to a trusted private registry with access control and a collision/allow-list policy. Where registry policy permits, reserving the corresponding public name reduces accidental collision risk, but Python package prefixes are not enforceable namespace ownership and a prefix alone does not force pip to a private source. Combine naming with a single curated source and reviewed artifact hashes; no public package was reserved or published for this lab.

### Pre-deploy signature verification gate — actual read-only run

Student-owned defense artifact: **`support/task4-verification-gate.sh`**. Exact executed command:

```bash
bash submission/week12-6631503097/support/task4-verification-gate.sh
```

Exit **0**. The gate hardcodes the approved immutable GHCR digest, exact identity `6631503097@lamduan.mfu.ac.th`, and issuer `https://github.com/login/oauth`. It prints ALLOW only after Cosign verifies; otherwise it preserves the failing exit code, prints DENY and stops. This turn exercised the genuine PASS branch and **simulated** deploy decision; no deployment was executed and the DENY branch was not separately exercised in this turn. Task 3's existing negative verification separately documents actual missing-signature rejection.

Actual stdout ends with:

```text
ALLOW: signature policy passed; simulated deploy would use ghcr.io/6631503097/week12-supplychain@sha256:f882526a88d1b808cbfc563a54f78db1650d10e6d025d7175b8cd0ed10e2e8a6
No deployment executed. Full build-provenance policy has not been established.
```

Gate command/status/timestamps and complete stdout/stderr are in `evidence/task4/gate-*` and `gate.*`. A real deployment pipeline must prevent bypass, verify and deploy the same digest, and treat all verification/auth/network failures as DENY. The current script deliberately performs no actual deploy.

### Signature versus SLSA provenance

Inspection of the existing verified signature bundle found predicate type **`https://sigstore.dev/cosign/sign/v1`**, with an empty predicate, not a verified SLSA build-provenance statement. The earlier image index contains a BuildKit attestation descriptor, but this exercise did not assess that attestation's contents, builder trust or compliance; a descriptor alone establishes no SLSA level. **No SLSA level is claimed.** A fuller provenance gate would require a trusted builder's authenticated attestation with subject digest matching this artifact, allowed source repository/revision, build type/parameters, and relevant resolved inputs; merely adding a signature or SBOM does not prove those properties. SLSA's current build provenance format uses `https://slsa.dev/provenance/v1`; no new attestation was generated, signed or published here.

Sources: https://pip.pypa.io/en/stable/cli/pip_install/ ; https://slsa.dev/spec/v1.2/build-provenance

### Concise mitigation mapping

| Control | What the evidence establishes | Mapping | Limit |
|---|---|---|---|
| Require hashes | pip refuses the unhashed manifest before installing lab dependencies | A03/A08; CWE-1357, CWE-829 | Does not create a trusted complete lockfile or patch CVEs |
| One trusted index | Actual explicit single-source command under clean pip settings, plus prior simulation before/after | A03; CWE-1357 | Registry compromise and uncontrolled alternate sources still matter |
| Internal naming/scoping | Written proposal only | A03; CWE-829 | A name prefix is not ownership or registry routing |
| Exact-identity digest gate | Valid existing signature permits simulated deploy decision | A08; CWE-829 | Does not assess full SLSA build provenance or prove dependency safety |

A03/A08 defenses should work together: source restrictions reduce substitution opportunities, reviewed hashes bind permitted bytes, and the signed-digest gate requires the authorized signer before deployment. Known vulnerable components still require remediation (CWE-1395); signature acceptance does not erase the SCA findings.

### Genuine screenshots and remaining written requirements

Accepted original full-screen identity-stamped captures:

- `evidence/screenshots/task4-hashes-single-index.png` — **24 October 2026 21:02:01.007074 +07**.
- `evidence/screenshots/task4-signature-gate-confirmed.png` — **21:03:06.256354 +07**.

Both were visually verified. The first gate capture showed another foreground application and is explicitly rejected in `evidence/task4/screenshot-review.json`; it is preserved without being submitted as evidence. Capture hashes/times and command statuses are preserved in `evidence/task4/`.

**Technical exercises are complete.** Remaining student-written work: review/adapt the namespace-scoping explanation for The Imposters, explain Task 2's before/after verdict in your own words, and choose the **one most effective defense and why** (the worksheet explicitly requires your judgment). The gate and signature/provenance limitations above are verified technical material for that explanation. Part 4's mapping table, XZ case analysis and evidence-based SLSA self-assessment remain separate reflection requirements; do not invent a level. This is not a completed full hashed-lockfile implementation, and none was required by the Task 4 refusal exercise.

No instructor or original wk06 files were changed. No additional signing, publication, Git commit/push, PR or final PDF occurred.
