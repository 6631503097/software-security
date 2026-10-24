#!/usr/bin/env bash
# Week 12 student defense artifact. Read-only verification; deployment is simulated.
set -euo pipefail
COSIGN=/private/tmp/week12-tools/cosign/v3.1.4/cosign
REF='ghcr.io/6631503097/week12-supplychain@sha256:f882526a88d1b808cbfc563a54f78db1650d10e6d025d7175b8cd0ed10e2e8a6'
IDENTITY='6631503097@lamduan.mfu.ac.th'
ISSUER='https://github.com/login/oauth'
if "$COSIGN" verify --certificate-identity "$IDENTITY" --certificate-oidc-issuer "$ISSUER" "$REF"; then
  printf '\nALLOW: signature policy passed; simulated deploy would use %s\n' "$REF"
  printf 'No deployment executed. Full build-provenance policy has not been established.\n'
else
  verify_status=$?
  printf '\nDENY: signature verification failed (exit %s); no simulated deploy allowed.\n' "$verify_status" >&2
  exit "$verify_status"
fi
