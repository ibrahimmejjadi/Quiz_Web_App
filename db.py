import sqlite3

db_name = "quiz.sqlite"
conn = None
cursor= None

def open():
    global conn, cursor
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

def close():
    cursor.close()
    conn.close()

def do(querry):
    cursor.execute(querry)
    conn.commit()

def create_tables():
    open()
    do('''CREATE TABLE IF NOT EXISTS users (
       id INTEGER PRIMARY KEY,
       username TEXT,
       email TEXT UNIQUE,
       password TEXT,
       role TEXT)''')
    do('''CREATE TABLE IF NOT EXISTS scores (
       id INTEGER PRIMARY KEY,
       user_id INTEGER ,
       quiz_id INTEGER,
       score INTEGER,
       is_pass INTEGER,
       date TEXT,
       FOREIGN KEY (user_id) REFERENCES users(id),
       FOREIGN KEY (quiz_id) REFERENCES quiz(id))''')
    close()

def create_admin_full():
    open()
    do("INSERT OR IGNORE INTO users (username, email, password, role) VALUES ('Ibrahim', 'Ibrahim_quiz@admin', 'admin123', 'admin-full' )")
    do("INSERT OR IGNORE INTO users (username, email, password, role) VALUES ('Teacher', 'teacher@quiz.com', 'teacher123', 'admin-mini')")
    do("INSERT OR IGNORE INTO users (username, email, password, role) VALUES ('Student', 'student@quiz.com', 'student123', 'user')")
    close()

def init_db():
    create_tables()
    create_admin_full()

def get_user(email, password):
    open()
    cursor.execute("SELECT * FROM users WHERE email= ? AND password =?", (email, password))
    user = cursor.fetchone()
    close()
    return user

def reset_scores():
    open()
    do("DELETE FROM scores")
    close()

def get_quizzes():
    open()
    cursor.execute("SELECT * FROM quiz")
    quizzes = cursor.fetchall()
    close()
    return quizzes

def already_taken(user_id, quiz_id):
    open()
    cursor.execute("SELECT * FROM scores WHERE user_id = ? AND quiz_id = ?", (user_id, quiz_id))
    result = cursor.fetchone()
    close()
    return result is not None

def get_first_question(quiz_id):
    open()
    cursor.execute("""SELECT question.* FROM question, quiz_content
                   WHERE quiz_content.quiz_id = ?
                   AND quiz_content.question_id = question.id
                   ORDER BY quiz_content.id
                   LIMIT 1""", (quiz_id,)) #is a tuple with one value without the comma Python think it's just parentheses, not a tuple this is why we added one
    question = cursor.fetchone()
    close()
    return question

def get_next_question(quiz_id, question_id):
    open()
    cursor.execute("""SELECT question.* FROM question, quiz_content
                   WHERE quiz_content.quiz_id = ?
                   AND quiz_content.question_id = question.id
                   AND quiz_content.question_id > ?
                   ORDER BY quiz_content.id
                   LIMIT 1""", (quiz_id, question_id))
    question= cursor.fetchone()
    close()
    return question
    
def save_score(user_id, quiz_id, score):
    open()
    is_pass = 1 if score >=2 else 0
    do(f"INSERT INTO scores (user_id, quiz_id, score, is_pass, date) VALUES ({user_id}, {quiz_id}, {score}, {is_pass}, date('now'))")  #date('now') --> sqlite automatically inserts today's date
    close()

def get_all_scores():
    open()
    cursor.execute("""SELECT users.username, quiz.name, scores.score, scores.is_pass, scores.date
                   FROM scores, users, quiz
                   Where scores.user_id = users.id
                   AND scores.quiz_id = quiz.id""")
    data = cursor.fetchall()
    close()
    return data

def get_summary_score():
    open()
    cursor.execute("""SELECT users.username, users.id,
                   SUM(scores.score),
                   COUNT (scores.id)
                   FROM scores, users
                   WHERE scores.user_id = users.id
                   GROUP BY users.id""")
    data = cursor.fetchall()
    close()
    return data

def get_student_scores(user_id):
    open()
    cursor.execute("""SELECT quiz.name, scores.score, scores.is_pass, scores. date
                   FROM scores, quiz
                   WHERE scores.quiz_id = quiz.id
                   AND scores.user_id = ?""", (user_id,))
    data = cursor.fetchall()
    close()
    return data

def get_all_users():
    open()
    cursor.execute("SELECT id, username, email, role FROM users")
    data = cursor.fetchall()
    close()
    return data 

def reset_student_scores(user_id):
    open()
    do(f"DELETE FROM scores WHERE user_id = {user_id}")
    close()

def create_user(username, email, password, role):
    open()
    do(f"INSERT OR IGNORE INTO users (username, email, password, role) VALUES ('{username}', '{email}', '{password}', '{role}')")
    close()

def delete_user(user_id):
    open()
    do(f"DELETE FROM users WHERE id = {user_id}")
    do(f"DELETE FROM scores WHERE user_id = {user_id}")
    close()



