#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from flask import Flask, request, jsonify, send_from_directory
from infer import infer

app = Flask(__name__, static_folder="web", static_url_path="")

@app.get("/")
def index():
    return send_from_directory("web", "index.html")

@app.post("/api/chat")
def api_chat():
    data = request.get_json(force=True, silent=True) or {}
    message = (data.get("message") or "").strip()
    if not message:
        return jsonify({"ok": False, "error": "Empty message"}), 400

    try:
        answer = infer(message)
        return jsonify({"ok": True, "answer": answer})
    except Exception as e:
        # In production, you might want to hide internal errors.
        return jsonify({"ok": False, "error": str(e)}), 500


if __name__ == "__main__":
    host = os.environ.get("HOST", "0.0.0.0")
    port = int(os.environ.get("PORT", "8080"))
    app.run(host=host, port=port, debug=False)

