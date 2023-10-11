from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

comments = {
    "1": {"post_id": "1", "user_id": "1", "comment": "Great post!"},
    "2": {"post_id": "1", "user_id": "2", "comment": "Interesting..."},
    "3": {"post_id": "2", "user_id": "1", "comment": "I like this one better."},
}


@app.route("/comment/<id>", methods=["GET"])
def get_comment(id):
    comment_info = comments.get(id, {})
    if comment_info:
        response = requests.get(f'http://localhost:5000/user/{comment_info["user_id"]}')
        if response.status_code == 200:
            comment_info["user"] = response.json()
    if comment_info:
        response = requests.get(f'http://localhost:5001/post/{comment_info["post_id"]}')
        if response.status_code == 200:
            comment_info["post"] = response.json()
    return jsonify(comment_info)


@app.route("/comment", methods=["POST"])
def create_comment():
    new_comment = request.get_json()
    id = str(len(comments) + 1)
    new_comment["id"] = id
    comments[id] = new_comment
    return jsonify(new_comment), 201


@app.route("/comment/<id>", methods=["PUT"])
def update_comment(id):
    comment_info = comments.get(id, {})
    if not comment_info:
        return jsonify({"error": "Comment not found"}), 404

    updated_comment = request.get_json()
    comments[id].update(updated_comment)
    return jsonify(comments[id])


@app.route("/comment/<id>", methods=["DELETE"])
def delete_comment(id):
    comment_info = comments.get(id, {})
    if not comment_info:
        return jsonify({"error": "Comment not found"}), 404

    del comments[id]
    return jsonify({"result": "Comment deleted"})


if __name__ == "__main__":
    app.run(port=5002)
