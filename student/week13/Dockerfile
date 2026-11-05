# Wanna San / 6631503097 - student-owned Week 13 defense.
# Build context: student/week13 only. Runtime: CPython 3.11 on Debian 12.
FROM python:3.11-slim@sha256:cdbd05fb6f457ca275ff51ce00d93d865ca0b6a25f5ffb08262d94f6835771e5 AS build
WORKDIR /build
COPY requirements.lock .
RUN python -m venv /venv \
    && /venv/bin/pip install --no-cache-dir --only-binary=:all: --require-hashes -r requirements.lock

FROM gcr.io/distroless/python3-debian12@sha256:2fdb05402a2cf21cf78fdb3ba4c5db167241e9e498140f5bf689d7efb773731f
WORKDIR /app
COPY --from=build /venv /venv
COPY --chown=65532:65532 app.py /app/app.py
ENV PYTHONPATH="/venv/lib/python3.11/site-packages" \
    PYTHONDONTWRITEBYTECODE="1"
USER 65532:65532
EXPOSE 5000
CMD ["app.py"]
