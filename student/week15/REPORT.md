# Week 15 — DevSecOps: Putting It Together

## Student information

| Name | Student ID | Date | Group |
|---|---|---|---|
| Wanna San | 6631503097 | 7 November 2026 | The Outsiders |

AI-use disclosure: I used Codex to help inspect the course files, automate authorized local and GitHub tests in my repository, capture identity-stamped evidence, and draft this report. I reviewed the results and explanations. Codex performed the technical automation described below; I do not present that automation as work I ran manually. My hosted “Break the Build” CTF result was completed and accepted separately, and its private flag is not included here.

## Lecture questions

1. A single scan step that exits as soon as it finds a problem can stop the job before its report is uploaded. The supplied design first produces SARIF, uploads it with `if: always()`, and then runs a separate gate. This keeps the findings available for investigation while still making the build red.

2. Fail-closed means an error denies access; fail-open means an error grants access. In `sample-service.py`, lines 96–103 catch an unexpected exception, log its type, and return 403. The commented line 110 would instead return the secret, so an error would become an authorization bypass (OWASP A10 / CWE-636).

3. The workflow only needs `contents: read` to check out and scan the repository and `security-events: write` to upload SARIF. A broad `write-all` token would unnecessarily let compromised workflow code alter repository content or other resources, increasing the effect of a supply-chain or script compromise.

4. A token is authentication data. Writing its value to logs creates another disclosure path and is CWE-532. The application should log the event type, allow/deny outcome, non-sensitive subject where known, source address, and a general reason so a SIEM can alert without receiving credentials.

5. Semgrep performs SAST for insecure code patterns and maps broadly to OWASP Top 10 rules. Trivy checks vulnerable dependencies and IaC/Dockerfile/secret issues, mapping to A03 and A02 in the course table. Gitleaks finds hard-coded secrets in files and Git history and maps to CWE-798.

## Task 0 — onboarding and structured logs

I used Codex to run the Flask sample service and make the three required benign requests. An invalid login returned 401 and logged `event=authn_failure outcome=deny reason=bad_token`; `bob-token` returned 403 and logged `event=authz_failure outcome=deny subject=bob reason=not_admin`; `alice-token` returned 200 and logged `event=authz_success outcome=allow subject=alice`. Evidence E1 shows all three structured events with my identity and timestamp.

## Task 1 — logging and fail-closed behavior

The authorization lookup is inside a `try` block. Normal missing and unauthorized identities are denied explicitly, while lines 96–103 also deny any unexpected exception with HTTP 403. Only `type(exc).__name__` is logged, which supports diagnosis without exposing an exception message that might contain sensitive details (CWE-209). The insecure commented alternative at lines 109–110 returns the secret from the exception handler and therefore fails open (A10/CWE-636).

I also verified the unexpected-error path with `student/week15/test_fail_closed.py`. A synthetic token store raised `RuntimeError`; the test observed HTTP 403, the fixed `{"error":"forbidden"}` body, an `authz_error/outcome=deny/error=RuntimeError` log entry, and no exception detail in the response or log. Result: 1 test passed.

### Task 1b — live insecure/secure comparison

The Docker services used the local synthetic value `LOCAL_WEEK15_DEMO_ONLY`, not a personalized flag. With no Authorization header, port 8090 returned 200 with `panel=UNLOCKED` and that synthetic value. Port 8091 returned 403 `forbidden`, while the legitimate `alice-token` request returned 200 and unlocked the panel. Evidence E2–E4 records these results.

The exact insecure path is `insecure_service.py` lines 41–49: `USERS[token]` raises `KeyError` for an empty token, and the broad `except Exception` returns the panel and secret. The secure service uses `USERS.get`, denies `None`, logs the event, and its exception handler also returns 403 (lines 45–76).

## Task 2 — stand up the security gate

I used the course design in a dedicated Week 15 workflow with least-privilege permissions and separate report, SARIF-upload, and gate steps. The three jobs were Semgrep, Trivy, and Gitleaks. An initial configuration problem was corrected: Trivy was pinned to a real immutable action revision, and Gitleaks was scoped to the Week 15 student-owned paths so unrelated historical course material did not create false failures. No blanket ignore was added.

The passing run is https://github.com/6631503097/software-security/actions/runs/42360522733. All three jobs passed and their SARIF upload steps completed. Evidence E5 shows the successful run. The fresh automation browser was not authenticated for the repository Security page, so I did not fabricate a Code Scanning page screenshot; the Actions run and authenticated GitHub API results provide the verified pipeline evidence.

## Task 3 — blue team passing gate

The secure student Dockerfile creates fixed UID 10001 and ends with `USER appuser`. The image built successfully, Docker inspection reported `Config.User=appuser`, and local Trivy configuration scanning at HIGH/CRITICAL returned exit 0. The dedicated GitHub workflow passed in all three jobs (E5).

## Task 4 — red team: Break the Build

On temporary branch `wk15-red-root`, I used Codex to change only the last Dockerfile user from `appuser` to `root`. Pull request https://github.com/6631503097/software-security/pull/4 triggered the gate. Trivy reported `AVD-DS-0002` / HIGH at Dockerfile line 9 and the step `Gate — fail on HIGH/CRITICAL (IaC)` exited 1: https://github.com/6631503097/software-security/actions/runs/42360740737/job/128368395877 (E6).

The secure `USER appuser` line was restored before the PR was closed without merge. The restored run passed all three jobs: https://github.com/6631503097/software-security/actions/runs/42360906089 (E7). No vulnerable change entered the protected branch.

## Task 5 — Red versus Blue scoreboard

| Planted finding | Gate result | Score |
|---|---|---|
| Dockerfile runs as root, DS-0002 HIGH | Caught by Trivy config gate; build failed | Blue +1 |

Final score: Blue 1, Red 0. One improvement would be to gate Trivy configuration findings at MEDIUM as well as HIGH/CRITICAL. This would catch `DS-0001` (`latest` tag), which the present threshold permits; the change should be paired with documented, narrow exceptions to control noise.

## Security analysis and mappings

| Control | Mapping | CWE | Rationale |
|---|---|---|---|
| Structured authentication/authorization events without token values | OWASP A09 | CWE-778 and CWE-532 | Events are observable without copying secrets into logs. |
| Deny on every unexpected authorization error | OWASP A10 | CWE-636 | An exception cannot turn into permission. |
| Non-root container plus Trivy IaC gate | OWASP A02/A03 scanner coverage | CWE-250 | The runtime avoids unnecessary privilege and CI rejects regression. |

## Reflection

1. The three mappings above connect the exercised controls to the course categories. The important point is that a scanner finding is useful only when the gate enforces it, while a log is useful only when it is collected and monitored.

2. The 2013 Target breach is a relevant example because security alerts were generated but were not acted on effectively, allowing the intrusion to continue. A09-oriented monitoring, ownership, and escalation of the structured events would not guarantee prevention, but it could shorten detection and response time.

3. For a small team, fail-closed code matters most at runtime because it protects the endpoint even if CI is unavailable or bypassed. The CI gate still matters because it stops known insecure patterns before deployment. Together they provide prevention at two different points: development and execution.

## Audit the AI

Original AI answer:

> Wrap the `/admin` body in `try/except` and return 403 on every exception:  
> `except Exception:`  
> `    return jsonify(error="forbidden"), 403`

The risky omission is the exact return-only exception block: it fails closed but silently hides unexpected authorization errors. That weakens A09 observability and makes attacks or defects harder to investigate. The corrected course implementation logs `event=authz_error outcome=deny`, source IP, and only `type(exc).__name__`, then returns the same fixed 403 response. My benign regression test forced a `RuntimeError` and verified denial, the structured log, and absence of the detailed exception message.

## Explain in Plain English

The insecure endpoint looks up an empty authorization token in a dictionary, which causes an error. Its error handler mistakenly treats that error as permission and returns the admin data. The secure version treats missing credentials and all errors as denial, records a safe event, and still allows the valid administrator token.

## Prompt Problem

Final prompt:

> Review the Week 15 student Dockerfile. Preserve Flask functionality. Ensure the final runtime user is a named non-root user created with a fixed UID after package installation; keep `USER appuser` as the last USER. Do not modify instructor teaching files or add scanner ignores. Verify the secure Dockerfile with a Docker build, inspection of `Config.User`, and a Trivy config HIGH/CRITICAL scan that exits 0. Then, only on a temporary branch, change it to `USER root`, verify that Trivy reports DS-0002 HIGH and exits 1, restore `appuser`, and rerun the passing gate.

Verified result: the secure image built with `Config.User=appuser`, local Trivy passed, the temporary root change produced DS-0002 HIGH and a failing GitHub gate, and restoration produced a passing three-job workflow. This verifies both the requested correction and the regression detector.

## Evidence and integrity

| ID | File | Verified observation |
|---|---|---|
| E1 | `task0-structured-security-logs-identity-approved.png` | Three required structured events; identity/time visible |
| E2 | `task1b-insecure-8090-identity.png` | Unauthenticated insecure service exposes only the local synthetic value |
| E3 | `task1b-secure-8091-deny-identity.png` | Unauthenticated secure service returns forbidden |
| E4 | `task1b-three-curl-results-identity.png` | 8090=200, 8091 unauthenticated=403, 8091 admin=200 |
| E5 | `task3-passing-security-run-identity.png` | Semgrep, Trivy, Gitleaks all pass |
| E6 | `task4-red-trivy-ds0002-failure-identity-final.png` | DS-0002 HIGH and enforcing exit 1 |
| E7 | `task4-restored-passing-run-identity.png` | Restored workflow passes all jobs |

Every listed image is a genuine whole-screen capture with a real terminal stamp. Originals and SHA-256 values are kept in the private evidence folder and are not committed. The personalized CTF flag and private CTF evidence are also excluded from GitHub.

## Completion status

Tasks 0–5 have verified local or GitHub results. The hosted CTF is student-confirmed as accepted but is not repeated here. Before final submission, I must personally review the drafted explanations, add the genuine hosted-CTF screenshot when supplied, and confirm whether the instructor requires a Security-tab screenshot in addition to the successful SARIF-upload steps. No PDF has been generated at this stage.

## References

- OWASP Foundation, *OWASP Top 10:2025 A09 Security Logging and Alerting Failures* and *A10 Mishandling of Exceptional Conditions*.
- MITRE, CWE-209, CWE-250, CWE-532, CWE-636, CWE-778, and CWE-798.
- U.S. Senate Committee on Commerce, Science, and Transportation, *A “Kill Chain” Analysis of the 2013 Target Data Breach* (2014).
- Course files: `worksheet.md`, `README-pipeline.md`, `security-ci.yml`, and the three Flask teaching services.
