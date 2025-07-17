from flask import Flask, render_template, request, redirect, url_for, jsonify
import json

app = Flask(__name__)
QUESTIONS_FILE = "questions.json"

def load_questions():
    with open(QUESTIONS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_questions(data):
    with open(QUESTIONS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/questions", methods=["GET"])
def get_questions():
    return jsonify(load_questions())

@app.route("/api/update", methods=["POST"])
def update_question():
    index = int(request.form["index"])
    question = request.form["question"].strip()
    answer = request.form["answer"].strip()

    data = load_questions()
    if 0 <= index < len(data):
        data[index]["question"] = question
        data[index]["answer"] = answer
        save_questions(data)
    return "OK"

@app.route("/api/delete", methods=["POST"])
def delete_question():
    index = int(request.form["index"])
    data = load_questions()
    if 0 <= index < len(data):
        del data[index]
        save_questions(data)
    return "OK"

if __name__ == "__main__":
    app.run(debug=True)
