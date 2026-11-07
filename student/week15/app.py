"""Small CI scan target for the Week 15 DevSecOps exercise."""

from flask import Flask, jsonify

app = Flask(__name__)


@app.get("/health")
def health():
    """Return a non-sensitive health response."""
    return jsonify(status="ok")


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5002, debug=False)
