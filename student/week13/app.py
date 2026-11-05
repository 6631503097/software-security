"""Sandbox/teaching only; for authorized lab use.

Week 13 — a minimal Flask app whose only purpose is to be containerized for the
Dockerfile-hardening exercise (Dockerfile.insecure vs Dockerfile.hardened, then
`trivy config` on the Dockerfiles and `trivy image` on the built images).
"""
from flask import Flask, jsonify

app = Flask(__name__)


@app.route("/")
def index():
    return jsonify(app="week13-demo", status="ok")


@app.route("/health")
def health():
    return jsonify(status="healthy")


if __name__ == "__main__":
    # 0.0.0.0 so the container is reachable via a published port.
    app.run(host="0.0.0.0", port=5000)
