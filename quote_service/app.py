import os
from flask import Flask, jsonify
from quote_service.quotes import get_random_quote


def create_app(instance_name=None):
    app = Flask(__name__)
    name = instance_name or os.environ.get("INSTANCE_NAME", "unknown")

    @app.route("/quote")
    def quote():
        q = get_random_quote()
        return jsonify({"quote": q["text"], "book": q["book"], "instance": name})

    @app.route("/health")
    def health():
        return jsonify({"status": "healthy"})

    return app


if __name__ == "__main__":
    port = int(os.environ.get("SERVICE_PORT", 5001))
    app = create_app()
    app.run(host="0.0.0.0", port=port)
