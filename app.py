from flask import Flask, request, redirect, session, render_template
from random import *  #we need it for choices of the quiz to not be displayed in an order correct_answer, wron1, wr2, wr3 is not a quiz then
import db

app = Flask(__name__)
app.secret_key = "quiz_secret_123"


# app.add_url_rule("/", "index", index)

@app.route("/")
def index():
  return redirect("/login")

@app.route("/login", methods = ["GET", "POST"])
def login():
  if request.method == "POST":
    email = request.form.get("email")
    password = request.form.get("password")
    user = db.get_user(email, password)
    if user:
      session["user_id"] = user[0]
      session["username"] = user[1]
      session["role"]= user [4]
      
      if session["role"] == "admin-full":
        return redirect("/admin/full")
      elif session["role"] == "admin-mini":
        return redirect("/admin/mini")
      else:
        return redirect("/home")
      
    else:
      return redirect("/login")
  else:
    return render_template("login.html")
  
@app.route("/home")
def home():
  if "user_id" not in session:
    return redirect("/login")
  quizzes = db.get_quizzes()
  return render_template("home.html", username = session["username"], role = session["role"], quizzes = quizzes)

@app.route("/logout")
def logout():
  session.clear()
  return redirect("/login")

@app.route("/quiz/<int:quiz_id>") #<int:quiz_id> means takes whatever number is in the URL and pass to function as quiz_id
def quiz(quiz_id):
  if "user_id" not in session:
    return redirect("/login")
  if db.already_taken(session["user_id"], quiz_id):
    return redirect("/home")
  question = db.get_first_question(quiz_id)
  choices = [question[2], question[3],question[4], question[5]]
  shuffle(choices) # shuffle to re-order the choices of the question
  return render_template("question.html", question=question, quiz_id=quiz_id, choices=choices )

@app.route("/answer", methods=["POST"])
def answer():
  quiz_id = int(request.form.get("quiz_id"))
  question_id = int(request.form.get("question_id"))
  correct_answer = request.form.get("correct_answer")
  user_answer = request.form.get("answer")

  if "score" not in session:
    session["score"] = 0
  if user_answer == correct_answer:
    session["score"] += 1
  
  next_question = db.get_next_question(quiz_id, question_id)
  if next_question:
    choices = [ next_question[2], next_question[3], next_question[4], next_question[5]]  
    shuffle(choices)  
    return render_template("question.html",question=next_question, quiz_id=quiz_id, choices=choices)
  else:
    return redirect("/result/" + str (quiz_id))
  
@app.route("/result/<int:quiz_id>")
def result(quiz_id):
  if "user_id" not in session:
    return redirect("/login")
  score = session.get("score", 0)
  db.save_score(session["user_id"], quiz_id, score)
  session["score"] = 0  #as reset for the next quiz
  return render_template("result.html", score= score, quiz_id =quiz_id)

@app.route("/admin/full", methods= ["GET", "POST"])
def admin_full():
  if "user_id" not in session:
    return redirect ("/login")
  if session["role"] != "admin-full":
    return redirect("/home")
  if request.method == "POST":
    username = request.form.get("username")
    email = request.form.get("email")
    password = request.form.get("password")
    role = request.form.get("role")
    db.create_user(username, email, password, role)
  users = db.get_all_users()

  return render_template("admin_full.html", username = session["username"], users =users)

@app.route("/admin/mini")
def admin_mini():
  if "user_id" not in session:
    return redirect("/login")
  if session["role"] not in ["admin-mini", "admin-full"]:
    return redirect("/home")
  scores = db.get_summary_score()
  return render_template("admin_mini.html", username = session["username"], scores=scores)

@app.route("/admin/student/<int:user_id>")
def student_detail(user_id):
  if "user_id" not in session:
    return redirect("/login")
  if session["role"] not in ["admin-mini", "admin-full"]:
    return redirect("/home")
  scores = db.get_student_scores(user_id)
  return render_template("student_detail_results.html", scores= scores, user_id=user_id, username=session["username"])

@app.route("/admin/delete/<int:user_id>")
def delete_confirm(user_id):
    if "user_id" not in session:
        return redirect("/login")
    if session["role"] != "admin-full":
        return redirect("/home")
    users = db.get_all_users()
    user = [u for u in users if u[0] == user_id][0]
    return render_template("delete_confirmation.html", user=user)

@app.route("/admin/delete/<int:user_id>/confirmation", methods=["POST"])
def delete_user(user_id):
    if "user_id" not in session:
        return redirect("/login")
    db.delete_user(user_id)
    return redirect("/admin/full")

@app.route("/admin/reset/<int:user_id>", methods=["POST"])
def reset_scores(user_id):
    if "user_id" not in session:
        return redirect("/login")
    db.reset_student_scores(user_id)
    return redirect("/admin/full")

# db.reset_scores()  # once per time

db.init_db()
if __name__ == "__main__":
  app.run(debug=True, host='0.0.0.0')   # debug it servers as go live in html 
  #host to link it with my laptop       # if you want to change something you don't have to stop and run the app again
                                        # the changes are being save automatically
                                        # NOTe!: if you wre interested to share publicly change True to False
                                        # because instead of a blank error page it can gives some deatils errors could be risk for security purposes
