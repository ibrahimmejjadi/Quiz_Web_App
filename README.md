# Quiz Web App — Flask + SQLite

A role-based quiz web application built with Python and Flask.
Designed for classroom use: teachers manage students, students take quizzes.


## Features

- 3 role levels: Admin Full / Admin Mini / Student
- Students can take quizzes once (no retakes without admin reset)
- Answer choices are shuffled randomly each time
- Teachers (Admin Mini) view all student scores and pass/fail status
- Admin Full can create users, delete users, and reset scores
- 6 quizzes covering: Python, Pseudo-code, Flowcharts, SQL, HTML/CSS, Flask

## Tech Stack

- Python 3
- Flask (web framework + routing + sessions)
- SQLite (database)
- Jinja2 (HTML templating)
- CSS (custom dark theme)

## How to Run

1. Install Flask: pip install flask
2. Run the database setup: python Quiz_Create.py
3. Start the app: python app.py
4. Open your browser: http://localhost:5000

## Test Accounts

| Role       | Email                  | Password    |
|------------|------------------------|-------------|
| Admin Full | Ibrahim_quiz@admin     | admin123    |
| Admin Mini | teacher@quiz.com       | teacher123  |
| Student    | student@quiz.com       | student123  |

## Known Limitations

This is a school project. Known areas for improvement:
- Passwords are stored in plain text (should use hashing e.g. bcrypt)
- Some queries use f-strings instead of parameterized queries (SQL injection risk)
- No registration page (users created by admin only)