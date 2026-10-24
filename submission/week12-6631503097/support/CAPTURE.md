# Genuine evidence capture — Wanna San, 6631503097, The Imposters

Never composite a terminal stamp onto a screenshot. A browser-only screenshot or text log is insufficient.

## Task 0
Open a real Terminal window and run:

```bash
bash /private/tmp/software-security-wk12/submission/week12-6631503097/support/task0-display.sh
```

The script prints and executes the exact worksheet identity command, displays the real branch and manifest. Make the whole manifest and identity readable, then capture the whole screen to `evidence/screenshots/task0.png` with macOS Shift-Command-3 (move the resulting original image there).

## Task 1
In a real Terminal run:

```bash
cd /private/tmp/software-security-wk12
printf '%s | %s | ' "$(whoami)" '6631503097'; date '+%F %T %Z'
head -40 submission/week12-6631503097/evidence/task1/sca_scan.stdout.txt
```

Keep the command itself and its identity output visible. Label this accurately as a replay of preserved scan output. Capture the first findings, then use another pane for pip-audit stdout and `process-status.jsonl`; refresh the identity command for each image. Full untruncated originals are preserved in the text evidence even if a screenshot shows only a readable excerpt.

## Task 2
In one Terminal run the local-only server:

```bash
python3 /private/tmp/software-security-wk12/submission/week12-6631503097/support/serve-simulation.py
```

Open `http://127.0.0.1:8765/sim/resolver-confusion` in your real browser. It serves the instructor's existing template/JS/CSS; only the normal title/cache-version template values are filled in memory. No registry is contacted.

Put a second Terminal beside the browser and execute exactly:

```bash
printf '%s | %s | ' "$(whoami)" '6631503097'; date '+%F %T %Z'
```

Capture the whole screen, including browser controls, versions, verdict, and terminal command/output:

1. Click **the attack** (1.4.0 private / 99.0.0 public, merged); save `task2-merged.png`.
2. Keep those versions and select single trusted index; save `task2-single.png`.
3. Click **win the race** (2.0.0 / 1.9.0, merged); save `task2-race.png`.

Refresh the exact identity command before each image. Stop the server with Ctrl-C when finished. Do not install acme-internal-utils or publish any package.
