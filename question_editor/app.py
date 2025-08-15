from flask import Flask, render_template, request, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(BASE_DIR, "questions.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

class Question(db.Model):
    __tablename__ = "questions"

    id = db.Column(db.Integer, primary_key=True)
    profession = db.Column(db.String(64), nullable=False)
    question = db.Column(db.Text, nullable=False)
    answer_text = db.Column(db.Text, nullable=True)
    answer_html = db.Column(db.Text, nullable=True)

    def to_api_dict(self):
        answer = self.answer_text if (self.answer_text and self.answer_text.strip()) else (self.answer_html or "")
        return {
            "id": self.id,
            "profession": self.profession,
            "question": self.question,
            "answer": answer,
            "answer_html": self.answer_html or "",
        }

@app.route("/")
def index():
    return render_template("index.html")

# Прямой переход на вопрос /q/123
@app.route("/q/<int:q_id>")
def index_q(q_id):
    return render_template("index.html")

# Список вопросов
@app.route("/api/questions", methods=["GET"])
def get_questions():
    items = Question.query.order_by(Question.id.asc()).all()
    return jsonify([q.to_api_dict() for q in items])

# Один вопрос по id (опционально, если хочешь подгружать по одному)
@app.route("/api/question/<int:q_id>", methods=["GET"])
def get_question(q_id):
    q = Question.query.get(q_id)
    if not q:
        abort(404)
    return jsonify(q.to_api_dict())

@app.route("/api/update", methods=["POST"])
def update_question():
    q_id = int(request.form["id"])
    question = request.form["question"].strip()
    answer = request.form["answer"].strip()

    q = Question.query.get(q_id)
    if q:
        q.question = question
        q.answer_text = answer
        db.session.commit()
    return "OK"

@app.route("/api/delete", methods=["POST"])
def delete_question():
    q_id = int(request.form["id"])  # <-- было "index", исправили на "id"
    q = Question.query.get(q_id)
    if q:
        db.session.delete(q)
        db.session.commit()
    return "OK"

if __name__ == "__main__":
    app.run(debug=True)
