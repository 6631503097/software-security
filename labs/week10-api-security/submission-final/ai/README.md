# Week 10 - API security correction

Wanna San | Student ID 6631503097 | Group: The Imposters

This is the separate AI-assisted correction used for the Week 10 Audit-the-AI and Prompt Problem exercises. It does not modify the supplied vulnerable_api.py or solution_api.py. The PDF and screenshot evidence are submitted separately.

## Changes

- Validate account creation JSON and username/password strings.
- Bind intended fields explicitly; generate IDs and force balance=0 and is_admin=False.
- Hash stored passwords and return only public account fields.
- Update copied seeded accounts and login consistently for hash verification.

## Files

- corrected_api.py: separate corrected copy, not a replacement Docker target.
- verify_correction.py: 16 in-process request checks and assertions.
- source-hashes.json: expected hashes of original supplied API sources.
- prompt-final.txt: exact prompt used for the AI-generated correction.

## Verification

Requires Python 3 with Flask and Werkzeug. From labs/week10-api-security in a suitable Python environment:

```bash
python3 submission-final/ai/verify_correction.py
```

The verifier uses Flask test_client without a live server or Docker requests. It checks the original mallory payload, attempted ID/hash injection, malformed/non-object/invalid account input, safe response fields, hash storage and valid/invalid login. Source-hash checks pin the original lab baseline.

## Limitations and attribution

The correction and verifier were generated with ChatGPT/Codex assistance. Authentication still uses the lab's client-controlled X-User-Id header. Users, ID generation and rate counters are in memory and not distributed or concurrency-safe. Production password policy, uniqueness, arbitrary malformed-login handling and deployment hardening remain outside this selected correction. The worksheet's password x is retained for lab compatibility. These checks are not a production-security claim or a Docker deployment test.
