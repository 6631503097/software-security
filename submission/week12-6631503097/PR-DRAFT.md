# Proposed PR title

Week 12: supply-chain security report, SBOM and verified defense gate

# Proposed PR description

Adds Wanna San’s Week 12 submission (6631503097, The Imposters), with an image-derived CycloneDX SBOM, dependency-confusion simulation evidence, and a digest-pinned signature gate that permits only simulated deployment after the exact email/issuer policy passes. Instructor lab sources remain unchanged.

Includes saved SCA findings and advisory-specific remediation, all 15 original identity-stamped screenshots, signing/verification transcripts, unsigned-image rejection, hash-enforcement refusal, and the verified wrong-signer rejection. The student reviewed and approved the reflection, EiPE, strongest-defense rationale and Audit the AI critique; AI assistance and the full actual prompt/response remain disclosed.

Validation: recorded tool exit statuses and screenshot integrity audited; CycloneDX schema passed; exact signer/issuer verification passed; unsigned and wrong-signer checks rejected. The PDF is generated with a binary-safe process and validated with independent readers and rendered-page inspection. No SLSA level, full hash lockfile, package-upgrade remediation or production deployment is claimed. GHCR image visibility was verified private in the preserved evidence. Quiz and course-portal submission are student actions.

Defense code commit: 336aaf8f9457d0a573c1649ff83e4cb0c2c99d2b.

# Prepared publication target

Repository: nutthakorn7/software-security
Base: main
Head: 6631503097:wk12
Approval: explicit user approval required before the first push. No force push; do not merge.

After PR creation, record its actual URL in support/finalization.json, regenerate and validate the PDF, and push only the authorized follow-up report commit to the same branch.
