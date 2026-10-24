**Task 4’s technical exercises are complete.**

- **Hash enforcement:** pip refused the original unhashed requirements with exit **1** and printed Flask’s actual SHA-256. The disposable environment contains only pip; no vulnerable dependencies were installed.
- **Single index:** demonstrated `--index-url https://pypi.org/simple` with inherited pip settings removed. The report links this to Task 2’s verified before/after evidence.
- **Verification gate:** the signed, digest-pinned image passed the exact email/issuer policy, exit **0**, allowing only a **simulated** deployment.
- **SLSA:** signature verification is distinguished from build-provenance verification. **No SLSA level is claimed.**

Saved:

- [Commands, outputs, exit codes and evidence](/private/tmp/software-security-wk12/submission/week12-6631503097/evidence/task4)
- [Hash/index screenshot](/private/tmp/software-security-wk12/submission/week12-6631503097/evidence/screenshots/task4-hashes-single-index.png)
- [Gate screenshot](/private/tmp/software-security-wk12/submission/week12-6631503097/evidence/screenshots/task4-signature-gate-confirmed.png)
- [Gate script](/private/tmp/software-security-wk12/submission/week12-6631503097/support/task4-verification-gate.sh)
- [Updated report](/private/tmp/software-security-wk12/submission/week12-6631503097/week12-tasks0-2.md)

Remaining written work: personalize the namespace-scoping explanation, explain the simulation’s before/after result, and choose the **most effective defense and why**. Reflection questions remain separate.

No instructor or `wk06` changes, additional publication/signing, Git commits/pushes, PR, or PDF generation occurred.
