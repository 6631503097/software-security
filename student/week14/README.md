# Week 14 defensive chatbot

Wanna San · 6631503097 · The Outsiders

A standalone student implementation for the local AI/LLM security exercise.
The instructor's teaching sources are unchanged. The chatbot uses a local
rule-based mock with no secrets, external model calls or tool access.

## Run locally

Use Python 3.12 or 3.13 in a virtual environment:

```sh
python -m pip install -r student/week14/requirements.txt
python student/week14/defensive_chatbot.py
```

Open `http://127.0.0.1:8084/`. This is a local development server.

## Verify

```sh
python -m unittest discover -s student/week14 -v
```

The seven test methods cover ordinary behavior, Unicode and HTML encoding,
message/query limits, duplicate/unknown parameters, control characters, response
headers and the model-output contract. Output must be an exact plain string of
at most 2,000 characters; other output returns HTTP 502 with a fixed message.

Jinja escaping applies at the HTML text sink. Limits and type checks are not a
complete prompt-injection defense for a real LLM. A production integration also
needs authorization, model timeouts, rate limits, safe tool interfaces and
context-specific output handling. GET messages remain visible in URLs.

AI assistance: Codex implemented and tested this student-owned defense under the
student's direction. The student selected and reviewed the output-handling
solution. Private worksheet evidence and personalized challenge data are excluded.
