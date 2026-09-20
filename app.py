from flask import Flask, render_template, request, jsonify, session, redirect
import sqlite3
from datetime import datetime

app = Flask(__name__)

app.secret_key = "tiet_ai_chatbot_2026"

DATABASE = "college.db"


# =========================================================
# DATABASE CONNECTION
# =========================================================

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


# =========================================================
# COLLEGE INFORMATION
# =========================================================

college_info = {
    "college": "Tagore Institute of Engineering and Technology",

    "timing": "The college working hours are from 09:15 AM to 04:30 PM.",

    "department": "The Computer Science and Engineering (CSE) department is available.",

    "hod": "The CSE Head of the Department is Kokila Mam.",

    "faculty": (
        "CSE faculty members are Vishnupriya Mam, Priyadharshini Mam, "
        "Bakya Mam, Sathya Mam, Raja Sir, Aishwarya Mam, "
        "Harshini Mam and Malathi Mam."
    ),

    "library": "Library working hours are from 09:00 AM to 05:00 PM.",

    "hostel": (
        "Hostel facilities are available for students. "
        "Separate accommodation facilities are provided for boys and girls. "
        "For exact hostel fees and availability, please contact the college office."
    ),

    "placement": (
        "The placement cell provides aptitude training, soft-skill training, "
        "technical training and interview preparation. "
        "Students can participate in company recruitment drives."
    ),

    "admission": (
        "Admissions are available for eligible students. "
        "For course availability, eligibility and admission procedures, "
        "please contact the college admission office."
    ),

    "contact": (
        "Sample Contact: Tagore Institute of Engineering and Technology, "
        "College Office. Phone: 04182-XXXXXX. "
        "Email: info@tagoreengineering.example"
    )
}


# =========================================================
# DATABASE TABLES
# =========================================================

def create_tables():

    conn = get_db()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS chat_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER,
            question TEXT NOT NULL,
            answer TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS college_settings (
            id INTEGER PRIMARY KEY,
            timing TEXT,
            hod TEXT,
            library TEXT,
            placement TEXT,
            admission TEXT,
            contact TEXT
        )
    """)

    conn.commit()
    conn.close()


# Create database tables
create_tables()


# =========================================================
# LOAD COLLEGE INFORMATION
# =========================================================

def load_college_info():

    conn = get_db()

    row = conn.execute("""
        SELECT *
        FROM college_settings
        WHERE id = 1
    """).fetchone()

    if row:

        if row["timing"]:
            college_info["timing"] = row["timing"]

        if row["hod"]:
            college_info["hod"] = row["hod"]

        if row["library"]:
            college_info["library"] = row["library"]

        if row["placement"]:
            college_info["placement"] = row["placement"]

        if row["admission"]:
            college_info["admission"] = row["admission"]

        if row["contact"]:
            college_info["contact"] = row["contact"]

    else:

        conn.execute("""
            INSERT INTO college_settings
            (
                id,
                timing,
                hod,
                library,
                placement,
                admission,
                contact
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            1,
            college_info["timing"],
            college_info["hod"],
            college_info["library"],
            college_info["placement"],
            college_info["admission"],
            college_info["contact"]
        ))

        conn.commit()

    conn.close()


load_college_info()


# =========================================================
# CHATBOT RESPONSE
# =========================================================

def chatbot_response(message):

    message = message.lower().strip()

    if not message:
        return "Please enter a question."

    # Greeting
    if (
        "hello" in message
        or "hi" in message
        or "hey" in message
    ):
        return (
            "Hello! 👋 Welcome to Tagore Institute of Engineering "
            "and Technology AI College Chatbot. How can I help you?"
        )

    # College name
    elif (
        "college name" in message
        or "which college" in message
    ):
        return college_info["college"]

    # Timing
    elif (
        "timing" in message
        or "college time" in message
        or "working hours" in message
    ):
        return college_info["timing"]

    # Department
    elif (
        "department" in message
        or "departments" in message
    ):
        return college_info["department"]

    # HOD
    elif (
        "hod" in message
        or "head of the department" in message
    ):
        return college_info["hod"]

    # Faculty
    elif (
        "faculty" in message
        or "staff" in message
        or "teachers" in message
    ):
        return college_info["faculty"]

    # Library
    elif "library" in message:
        return college_info["library"]

    # Hostel
    elif "hostel" in message:
        return college_info["hostel"]

    # Placement
    elif (
        "placement" in message
        or "placements" in message
        or "job" in message
    ):
        return college_info["placement"]

    # Admission
    elif (
        "admission" in message
        or "admissions" in message
    ):
        return college_info["admission"]

    # Contact
    elif (
        "contact" in message
        or "phone" in message
        or "email" in message
    ):
        return college_info["contact"]

    # CSE
    elif (
        "cse" in message
        or "computer science" in message
    ):
        return (
            "CSE stands for Computer Science and Engineering. "
            "The CSE department focuses on programming, software "
            "development, databases, networking and computer technologies."
        )

    # Courses
    elif (
        "course" in message
        or "courses" in message
    ):
        return (
            "The college offers engineering courses. "
            "For the latest course list and admission details, "
            "please contact the admission office."
        )

    # Exam
    elif (
        "exam" in message
        or "examination" in message
    ):
        return (
            "Exam schedules and examination-related information "
            "are announced by the examination cell."
        )

    # Thank you
    elif "thank" in message:
        return "You're welcome! 😊 Have a great day!"

    # Unknown
    else:
        return (
            "Sorry 😔 I don't have information about that yet. "
            "You can ask me about college timing, CSE, HOD, faculty, "
            "library, hostel, placement, admission or contact details."
        )


# =========================================================
# HOME
# =========================================================

@app.route("/")
def home():

    return render_template("index.html")


# =========================================================
# CHAT
# =========================================================

@app.route("/chat", methods=["POST"])
def chat():

    data = request.get_json()

    if not data:
        return jsonify({
            "response": "Please enter a question."
        })

    message = data.get("message", "").strip()

    if not message:
        return jsonify({
            "response": "Please enter a question."
        })

    response = chatbot_response(message)

    student_id = session.get("student_id")

    # Save chat only for logged-in student
    if student_id:

        conn = get_db()

        conn.execute("""
            INSERT INTO chat_history
            (
                student_id,
                question,
                answer,
                created_at
            )
            VALUES (?, ?, ?, ?)
        """, (
            student_id,
            message,
            response,
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ))

        conn.commit()
        conn.close()

    return jsonify({
        "response": response
    })


# =========================================================
# STUDENT SIGNUP
# =========================================================

@app.route("/signup", methods=["GET", "POST"])
def signup():

    if request.method == "POST":

        name = request.form.get("name", "").strip()

        # Convert email to lowercase
        email = request.form.get(
            "email", ""
        ).strip().lower()

        password = request.form.get(
            "password", ""
        ).strip()

        if not name or not email or not password:

            return render_template(
                "signup.html",
                error="Please fill all fields."
            )

        conn = get_db()

        try:

            conn.execute("""
                INSERT INTO students
                (
                    name,
                    email,
                    password
                )
                VALUES (?, ?, ?)
            """, (
                name,
                email,
                password
            ))

            conn.commit()

        except sqlite3.IntegrityError:

            conn.close()

            return render_template(
                "signup.html",
                error="Email already registered."
            )

        conn.close()

        return redirect("/login")

    return render_template("signup.html")


# =========================================================
# STUDENT LOGIN
# =========================================================

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        # Convert email to lowercase
        email = request.form.get(
            "email", ""
        ).strip().lower()

        password = request.form.get(
            "password", ""
        ).strip()

        if not email or not password:

            return render_template(
                "login.html",
                error="Please enter email and password."
            )

        conn = get_db()

        student = conn.execute("""
            SELECT *
            FROM students
            WHERE LOWER(email) = ?
            AND password = ?
        """, (
            email,
            password
        )).fetchone()

        conn.close()

        if student:

            # Clear old sessions
            session.pop("admin", None)

            # Student session
            session["student_id"] = student["id"]
            session["student_name"] = student["name"]
            session["student_email"] = student["email"]

            return redirect("/")

        return render_template(
            "login.html",
            error="Wrong email or password."
        )

    return render_template("login.html")


# =========================================================
# STUDENT LOGOUT
# =========================================================

@app.route("/logout")
def logout():

    session.pop("student_id", None)
    session.pop("student_name", None)
    session.pop("student_email", None)

    return redirect("/login")


# =========================================================
# STUDENT CHAT HISTORY
# =========================================================

@app.route("/history")
def history():

    if not session.get("student_id"):
        return redirect("/login")

    conn = get_db()

    chats = conn.execute("""
        SELECT
            question,
            answer,
            created_at
        FROM chat_history
        WHERE student_id = ?
        ORDER BY id DESC
    """, (
        session["student_id"],
    )).fetchall()

    conn.close()

    return render_template(
        "history.html",
        chats=chats
    )


# =========================================================
# ADMIN LOGIN
# =========================================================

@app.route("/admin-login", methods=["GET", "POST"])
def admin_login():

    if request.method == "POST":

        username = request.form.get(
            "username", ""
        ).strip()

        password = request.form.get(
            "password", ""
        ).strip()

        if username == "admin" and password == "1234":

            # Clear student session
            session.pop("student_id", None)
            session.pop("student_name", None)
            session.pop("student_email", None)

            # Admin session
            session["admin"] = True

            return redirect("/dashboard")

        return render_template(
            "admin_login.html",
            error="Wrong admin username or password."
        )

    return render_template("admin_login.html")


# =========================================================
# ADMIN PANEL
# =========================================================

@app.route("/admin")
def admin():

    if not session.get("admin"):
        return redirect("/admin-login")

    return render_template("admin.html")


# =========================================================
# ADMIN LOGOUT
# =========================================================

@app.route("/admin-logout")
def admin_logout():

    session.pop("admin", None)

    return redirect("/admin-login")


# =========================================================
# ADMIN DASHBOARD
# =========================================================

@app.route("/dashboard")
def dashboard():

    if not session.get("admin"):
        return redirect("/admin-login")

    conn = get_db()

    # Total students
    total_students = conn.execute("""
        SELECT COUNT(*)
        FROM students
    """).fetchone()[0]

    # Total questions
    total_questions = conn.execute("""
        SELECT COUNT(*)
        FROM chat_history
    """).fetchone()[0]

    # Today's chats
    today_chats = conn.execute("""
        SELECT COUNT(*)
        FROM chat_history
        WHERE DATE(created_at) = DATE('now')
    """).fetchone()[0]

    # Students + chat count
    students = conn.execute("""
        SELECT
            students.id,
            students.name,
            students.email,
            COUNT(chat_history.id) AS chat_count
        FROM students
        LEFT JOIN chat_history
        ON students.id = chat_history.student_id
        GROUP BY students.id
        ORDER BY students.id DESC
    """).fetchall()

    # Recent chats
    recent_chats = conn.execute("""
        SELECT
            question,
            answer,
            created_at
        FROM chat_history
        ORDER BY id DESC
        LIMIT 10
    """).fetchall()

    conn.close()

    return render_template(
        "dashboard.html",
        total_students=total_students,
        total_questions=total_questions,
        today_chats=today_chats,
        students=students,
        recent_chats=recent_chats
    )


# =========================================================
# DELETE STUDENT
# =========================================================

@app.route(
    "/delete-student/<int:student_id>",
    methods=["POST"]
)
def delete_student(student_id):

    if not session.get("admin"):
        return redirect("/admin-login")

    conn = get_db()

    # Delete student's chats
    conn.execute("""
        DELETE FROM chat_history
        WHERE student_id = ?
    """, (
        student_id,
    ))

    # Delete student
    conn.execute("""
        DELETE FROM students
        WHERE id = ?
    """, (
        student_id,
    ))

    conn.commit()
    conn.close()

    return redirect("/dashboard")


# =========================================================
# ADMIN VIEW STUDENT CHATS
# =========================================================

@app.route("/student-chats/<int:student_id>")
def student_chats(student_id):

    if not session.get("admin"):
        return redirect("/admin-login")

    conn = get_db()

    student = conn.execute("""
        SELECT
            id,
            name,
            email
        FROM students
        WHERE id = ?
    """, (
        student_id,
    )).fetchone()

    chats = conn.execute("""
        SELECT
            question,
            answer,
            created_at
        FROM chat_history
        WHERE student_id = ?
        ORDER BY id DESC
    """, (
        student_id,
    )).fetchall()

    conn.close()

    if student is None:
        return "Student not found."

    return render_template(
        "student_chats.html",
        student=student,
        chats=chats
    )


# =========================================================
# UPDATE COLLEGE INFORMATION
# =========================================================

@app.route("/update-info", methods=["POST"])
def update_info():

    if not session.get("admin"):

        return jsonify({
            "message": "Unauthorized. Please login as admin."
        }), 401

    data = request.get_json()

    if not data:

        return jsonify({
            "message": "No information received."
        }), 400

    timing = data.get(
        "timing",
        college_info["timing"]
    )

    hod = data.get(
        "hod",
        college_info["hod"]
    )

    library = data.get(
        "library",
        college_info["library"]
    )

    placement = data.get(
        "placement",
        college_info["placement"]
    )

    admission = data.get(
        "admission",
        college_info["admission"]
    )

    contact = data.get(
        "contact",
        college_info["contact"]
    )

    # Update current chatbot information
    college_info["timing"] = timing
    college_info["hod"] = hod
    college_info["library"] = library
    college_info["placement"] = placement
    college_info["admission"] = admission
    college_info["contact"] = contact

    # Save permanently
    conn = get_db()

    conn.execute("""
        INSERT OR REPLACE INTO college_settings
        (
            id,
            timing,
            hod,
            library,
            placement,
            admission,
            contact
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        1,
        timing,
        hod,
        library,
        placement,
        admission,
        contact
    ))

    conn.commit()
    conn.close()

    return jsonify({
        "message": "Information saved permanently! ✅"
    })


# =========================================================
# RUN APPLICATION
# =========================================================

if __name__ == "__main__":

    app.run(debug=True)