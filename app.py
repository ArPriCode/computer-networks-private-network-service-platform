from flask import Flask, jsonify

app = Flask(__name__)


@app.route("/", methods=["GET"])
def home():
    response = jsonify({
        "backend": "A",
        "status": "running"
    })
    response.headers["X-Backend"] = "A"
    response.headers["Cache-Control"] = "max-age=60"
    return response


@app.route("/api/status", methods=["GET"])
def status():
    response = jsonify({
        "backend": "A",
        "status": "ok"
    })
    response.headers["X-Backend"] = "A"
    response.headers["Cache-Control"] = "max-age=60"
    return response


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3001)
