from flask import Flask, jsonify

app = Flask(__name__)


@app.route("/user/<id>")
def user(id):
    users = {
        "1": {"name": "Alice", "email": "alice@example.com"},
        "2": {"name": "Bob", "email": "bob@example.com"},
    }
    user_info = users.get(id, {})
    return jsonify(user_info)


if __name__ == "__main__":
    app.run(port=5000)
