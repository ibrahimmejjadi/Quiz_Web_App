import sqlite3
db_name = 'quiz.sqlite'
conn = None
cursor = None

def open():
    global conn, cursor
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

def close():
    cursor.close()
    conn.close()

def do(query):
    cursor.execute(query)
    conn.commit()

def clear_db():
    open()
    do('DROP TABLE IF EXISTS quiz_content')
    do('DROP TABLE IF EXISTS question')
    do('DROP TABLE IF EXISTS quiz')
    close()

def show(table):
    query = 'SELECT * FROM ' + table
    open()
    cursor.execute(query)
    print(cursor.fetchall())
    close()

def show_tables():
    show('question')
    show('quiz')
    show('quiz_content')

def create():
    open()
    do('''CREATE TABLE IF NOT EXISTS quiz (
        id INTEGER PRIMARY KEY, 
        name VARCHAR)''')
    do('''CREATE TABLE IF NOT EXISTS question (
        id INTEGER PRIMARY KEY, 
        question TEXT, answer TEXT, 
        wrong1 TEXT, wrong2 TEXT, wrong3 TEXT)''')
    do('''CREATE TABLE IF NOT EXISTS quiz_content (
        id INTEGER PRIMARY KEY,
        quiz_id INTEGER, 
        question_id INTEGER,
        FOREIGN KEY (quiz_id) REFERENCES quiz(id),
        FOREIGN KEY (question_id) REFERENCES question(id))''')
    close()

quizzes = [
    ("Python_intro",),
    ("Pseudo_code",),
    ("Logigramme_algo_symbols",),
    ("SQL_queries",),
    ("HTML_CSS_Basics",),
    ("FLASK_intro",)
]

questions = [
    # Python_intro
    ("What is the function to display text in Python?", "print()", "write()", "echo()", "display()"),
    ("Which of these is a pre-defined Python function?", "str()", "printf()", "length()", "create()"),
    ("How do you use a library in Python?", "import library_name", "Library_name(use).py", "Module.Library_name", "Python(usage.Library_name)"),
    # Pseudo_code
    ("The parts of pseudo-code by sequence are?", "Variables-Debut-Traitement-Fin", "Debut-Body-Fin", "Debut-Fin", "Variables-Body-Fin"),
    ("A for loop in pseudo-code is like?", "Pour i allant de 4 a 6...Fin Pour", "While True", "For i in range(0,4)", "Tant que(i<4)...Fin Tant que"),
    ("A pseudo-code can be written in?", "French, English, Arabic...", "Only French", "Only English", "Only Arabic"),
    # Logigramme_algo_symbols
    ("Which shape represents a decision in a flowchart?", "Diamond", "Rectangle", "Circle", "Arrow"),
    ("Which shape is used to START and END a flowchart?", "Oval/Ellipse", "Rectangle", "Diamond", "Triangle"),
    ("Which shape represents a process/action in a flowchart?", "Rectangle", "Diamond", "Oval", "Circle"),
    # SQL_queries
    ("Which SQL command retrieves data from a table?", "SELECT", "GET", "FETCH", "FIND"),
    ("Which SQL command adds a new row to a table?", "INSERT INTO", "ADD INTO", "PUSH INTO", "PUT INTO"),
    ("Which SQL keyword filters results?", "WHERE", "FILTER", "SEARCH", "CONDITION"),
    # HTML_CSS_Basics
    ("Which tag creates the largest heading in HTML?", "<h1>", "<h6>", "<head>", "<header>"),
    ("Which attribute adds an image source in HTML?", "src", "href", "link", "url"),
    ("Which tag creates an unordered list in HTML?", "<ul>", "<ol>", "<li>", "<list>"),
    # FLASK_intro
    ("What is Flask in Python?", "A web framework", "A database library", "A game engine", "A math library"),
    ("What function starts the Flask web server?", "app.run()", "app.start()", "app.launch()", "server.run()"),
    ("In Flask, what does the route define?", "The URL that triggers a function", "The database connection", "The HTML template", "The server port"),
]

def fill():
    open()
    cursor.executemany("INSERT INTO quiz (name) VALUES (?)", quizzes)
    cursor.executemany("INSERT INTO question (question, answer, wrong1, wrong2, wrong3) VALUES (?,?,?,?,?)", questions)
    conn.commit()
    close()

def fill_content():
    open()
    answer = input("Add a link? (y/n): ")
    while answer != "n":
        quiz_id = int(input("Quiz ID: "))
        question_id = int(input("Question ID: "))
        do(f"INSERT INTO quiz_content (quiz_id, question_id) VALUES ({quiz_id}, {question_id})")
        answer = input("Add a link? (y/n): ")
    close()

def main():
    clear_db()
    create()
    fill()
    fill_content()
    show_tables()

if __name__ == "__main__":
    main()