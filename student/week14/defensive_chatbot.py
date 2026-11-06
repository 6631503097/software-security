"""Student defensive implementation; local mock only, no secrets or tools."""
import unicodedata

from flask import Flask, render_template_string, request

app = Flask(__name__)
MAX_MESSAGE_CHARS = 1000
MAX_QUERY_BYTES = 8192
MAX_REPLY_CHARS = 2000
SYSTEM_PROMPT = "You are HelpBot. Answer general questions only."
PAGE = """<!doctype html>
<html lang="en"><meta charset="utf-8"><title>HelpBot</title>
<h2>HelpBot</h2>
<form method="get">
<label for="msg">Message</label>
<input id="msg" name="msg" maxlength="1000" size="60">
<button>Send</button></form>
<div>{{ reply }}</div></html>"""


def mock_llm(system: str, user: str) -> str:
    """Return untrusted text; the handler validates it before HTML rendering."""
    if "hello" in user.casefold() or "hi" in user.casefold():
        return "Hello! I'm HelpBot. How can I help you today?"
    return f"You said: {user}"


@app.after_request
def security_headers(response):
    response.headers["Content-Security-Policy"] = (
        "default-src 'none'; base-uri 'none'; form-action 'self'; frame-ancestors 'none'"
    )
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["Cache-Control"] = "no-store"
    return response


@app.get("/")
def chat():
    # Check transport size before parsing, and length before trimming.
    if len(request.query_string) > MAX_QUERY_BYTES:
        return render_template_string(PAGE, reply="Request is too large."), 413
    values = request.args.getlist("msg")
    if set(request.args) - {"msg"} or len(values) > 1:
        return render_template_string(PAGE, reply="Use a single message parameter."), 400
    msg = values[0] if values else ""
    if len(msg) > MAX_MESSAGE_CHARS:
        return render_template_string(PAGE, reply="Message is too long."), 400
    if any(unicodedata.category(char) in {"Cc", "Cs"} for char in msg):
        return render_template_string(PAGE, reply="Message contains unsupported characters."), 400
    msg = msg.strip()
    reply = mock_llm(SYSTEM_PROMPT, msg) if msg else "Ask me something!"
    # Reject trusted-markup subclasses as well as non-text or excessive output.
    if type(reply) is not str or len(reply) > MAX_REPLY_CHARS:
        return render_template_string(PAGE, reply="Unable to display this response."), 502
    # Jinja autoescaping applies to both user text and model output.
    return render_template_string(PAGE, reply=reply)


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8084, debug=False)
