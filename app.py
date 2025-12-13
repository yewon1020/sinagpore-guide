import requests
import requests
import os

from flask import Flask, render_template, jsonify,request

app = Flask(__name__)

VOTES = {
    "marina_bay_sands": 0,
    "gardens_by_the_bay": 0,
    "merlion_park": 0
}

GUESTBOOK = []

@app.route("/vote", methods=["POST"])
def vote_post():
    data = request.get_json()
    choice = data.get("choice")
    if choice not in VOTES:
        return jsonify({"ok": False, "error": "invalid choice"}), 400
    VOTES[choice] += 1
    return jsonify({"ok": True})

@app.route("/guestbook", methods=["POST"])
def add_guestbook():
    data = request.get_json()
    name = data.get("name", "Anonymous")
    message = data.get("message", "")
    if not message.strip:
        return jsonify({"ok": False, "error": "Empty message"}), 400

    entry = {"name" : name, "message" : message}
    GUESTBOOK.append(entry)
    return jsonify({"ok" : True, "entries" : GUESTBOOK})

@app.route("/guestbook/list")
def guestbook_list() :
    return jsonify({"entries" : GUESTBOOK})

@app.route("/map")
def map_page() :
    return render_template("map_sg.html")

@app.route("/results")
def results():
    total = sum(VOTES.values())
    return jsonify({"votes": VOTES, "total": total})

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/vote")
def vote():
    return render_template("vote.html")

@app.route("/guestbook")
def guestbook():
    return render_template("guestbook.html")

if __name__ == '__main__':
# debug=True 모드는 개발 중에만 사용해야 합니다.
    port = int(os.environ.get("PORT", 5002))  #Render가 주는 PORT 사용
    app.run(host="0.0.0.0", debug=False, port=port)