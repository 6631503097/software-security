# DRAFT-ONLY AI RESPONSE to prompt-final.txt; not deployed.
"""SECURE reference — Week 10 API Security. Fixes the flaws in vulnerable_api.py.

Mitigations:
  API1:2023 BOLA   -> per-object ownership check (caller may only read their own
                      orders, unless admin).
  API3:2023 Mass Assignment -> explicit allow-list of bindable fields; server sets
                      sensitive fields (id, balance, is_admin) itself.
  API4:2023 Unrestricted Resource Consumption -> simple per-IP rate limiter on /api/login.

Run:  flask --app solution_api run --port 5001   (or use docker-compose.yml)
"""
import time
from collections import defaultdict
from flask import Flask, jsonify, request
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

USERS = {
    1: {"id": 1, "username": "alice", "password": "alice123",
        "balance": 100, "is_admin": False},
    2: {"id": 2, "username": "bob", "password": "bob123",
        "balance": 50, "is_admin": False},
    3: {"id": 3, "username": "carol", "password": "carol123",
        "balance": 9999, "is_admin": True},
}
ORDERS = {
    1: [{"order_id": "A-1", "item": "Keyboard", "total": 30}],
    2: [{"order_id": "B-1", "item": "Mouse", "total": 15}],
    3: [{"order_id": "C-1", "item": "Server rack", "total": 5000}],
}
for _user in USERS.values():
    _user["password_hash"] = generate_password_hash(_user.pop("password"))
_next_id = 4

# Only these keys may come from the client body. Everything else is ignored.
ALLOWED_CREATE_FIELDS = {"username", "password"}


def current_user():
    try:
        return USERS.get(int(request.headers.get("X-User-Id", 0)))
    except (TypeError, ValueError):
        return None


# --- FIX API1: object-level authorization ------------------------------------
@app.get("/api/users/<int:uid>/orders")
def get_orders(uid):
    caller = current_user()
    if caller is None:
        return jsonify({"error": "authentication required"}), 401
    # The caller may only read their own orders unless they are an admin.
    if caller["id"] != uid and not caller["is_admin"]:
        return jsonify({"error": "forbidden"}), 403
    return jsonify(ORDERS.get(uid, []))


# --- FIX API3: allow-list binding --------------------------------------------
@app.post("/api/users")
def create_user():
    global _next_id
    body = request.get_json(silent=True)
    if not isinstance(body, dict):
        return jsonify({"error": "JSON object required"}), 400
    username, password = body.get("username"), body.get("password")
    if (not isinstance(username, str) or not isinstance(password, str)
            or not 1 <= len(username.strip()) <= 64
            or not 1 <= len(password) <= 128):
        return jsonify({"error": "invalid username or password"}), 400
    # Build explicitly; extra client properties never enter the stored record.
    user = {"id": _next_id, "username": username.strip(),
            "password_hash": generate_password_hash(password),
            "balance": 0, "is_admin": False}
    USERS[_next_id] = user
    _next_id += 1
    public = {key: user[key] for key in ("id", "username", "balance", "is_admin")}
    return jsonify(public), 201


# --- FIX API4: per-IP rate limiting ------------------------------------------
RATE_LIMIT = 5            # max attempts...
RATE_WINDOW = 60         # ...per this many seconds, per IP.
_attempts = defaultdict(list)


def rate_limited(ip):
    now = time.time()
    _attempts[ip] = [t for t in _attempts[ip] if now - t < RATE_WINDOW]
    if len(_attempts[ip]) >= RATE_LIMIT:
        return True
    _attempts[ip].append(now)
    return False


@app.post("/api/login")
def login():
    if rate_limited(request.remote_addr or "unknown"):
        return jsonify({"error": "too many requests"}), 429
    body = request.get_json(force=True) or {}
    for u in USERS.values():
        if u["username"] == body.get("username") and isinstance(body.get("password"), str) and check_password_hash(u["password_hash"], body["password"]):
            return jsonify({"ok": True, "user_id": u["id"], "is_admin": u["is_admin"]})
    return jsonify({"ok": False}), 401


@app.get("/")
def index():
    return "Week 10 SECURE API", 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
