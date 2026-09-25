from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)

# Secret key for Flask sessions
app.secret_key = "capacity-connect-demo-key"


# =========================================================
# COURSE DATA
# =========================================================

courses_data = [
    {
        "title": "Python Fundamentals",
        "category": "Programming",
        "level": "Beginner",
        "description": (
            "Learn Python from the basics including variables, "
            "conditions, loops, functions and problem solving."
        )
    },
    {
        "title": "Web Development",
        "category": "Development",
        "level": "Beginner",
        "description": (
            "Learn HTML, CSS, JavaScript and Flask "
            "to build modern web applications."
        )
    },
    {
        "title": "Data Analysis",
        "category": "Data",
        "level": "Beginner",
        "description": (
            "Understand data analysis concepts and "
            "learn how to work with structured data."
        )
    }
]


# =========================================================
# TRAINING PROGRAM DATA
# =========================================================

training_data = [
    {
        "title": "Digital Skills Program",
        "duration": "4 Weeks",
        "description": (
            "Build essential digital skills required "
            "for today's workplace."
        )
    },
    {
        "title": "Programming Starter Program",
        "duration": "6 Weeks",
        "description": (
            "A beginner-friendly pathway to start "
            "programming and problem solving."
        )
    },
    {
        "title": "Career Readiness Program",
        "duration": "4 Weeks",
        "description": (
            "Improve communication, resume building, "
            "interview preparation and professional skills."
        )
    }
]


# =========================================================
# CERTIFICATION DATA
# =========================================================

certifications_data = [
    {
        "title": "Python Fundamentals Certificate",
        "course": "Python Fundamentals",
        "issuer": "Capacity Connect",
        "duration": "4 Weeks",
        "skills": "Python, Programming Basics, Problem Solving",
        "status": "Available"
    },
    {
        "title": "Web Development Certificate",
        "course": "Web Development",
        "issuer": "Capacity Connect",
        "duration": "6 Weeks",
        "skills": "HTML, CSS, JavaScript, Flask",
        "status": "Available"
    },
    {
        "title": "Data Analysis Certificate",
        "course": "Data Analysis",
        "issuer": "Capacity Connect",
        "duration": "5 Weeks",
        "skills": "Data Analysis, Data Handling, Visualization",
        "status": "Available"
    }
]


# =========================================================
# HOME
# =========================================================

@app.route("/")
def home():
    return render_template("login.html")


# =========================================================
# ABOUT
# =========================================================

@app.route("/about")
def about():
    return render_template("about.html")


# =========================================================
# COURSES
# =========================================================

@app.route("/courses")
def courses():
    return render_template(
        "courses.html",
        courses=courses_data
    )


# =========================================================
# TRAINING PROGRAMS
# =========================================================

@app.route("/training")
def training():
    return render_template(
        "training.html",
        training=training_data
    )


# =========================================================
# CERTIFICATIONS
# =========================================================

@app.route("/certifications")
def certifications():

    completed_courses = session.get(
        "completed_courses",
        []
    )

    certificates = []

    for course in courses_data:

        certificates.append({
            "title": course["title"],
            "category": course["category"],
            "level": course["level"],
            "completed": (
                course["title"]
                in completed_courses
            )
        })

    return render_template(
        "certifications.html",
        certificates=certificates
    )


# =========================================================
# LOGIN
# =========================================================

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        purpose = request.form.get("purpose")
        email = request.form.get("email")
        password = request.form.get("password")

        # Prototype login validation
        if purpose and email and password:

            session["user"] = email
            session["purpose"] = purpose

            return redirect(
                url_for("dashboard")
            )

    return render_template("login.html")


# =========================================================
# REGISTER
# =========================================================

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")

        # Prototype registration
        if name and email and password:

            session["user"] = email
            session["purpose"] = "Learner"

            return redirect(
                url_for("dashboard")
            )

    return render_template("register.html")


# =========================================================
# DASHBOARD
# =========================================================

@app.route("/dashboard")
def dashboard():

    if "user" not in session:

        return redirect(
            url_for("login")
        )

    return render_template(
        "index.html",
        user=session.get("user"),
        purpose=session.get(
            "purpose",
            "Learner"
        )
    )


# =========================================================
# LOGOUT
# =========================================================

@app.route("/logout")
def logout():

    session.clear()

    return redirect(
        url_for("login")
    )


# =========================================================
# GENERAL QUIZ PAGE
# =========================================================

@app.route("/quiz")
def quiz():
    return render_template("quiz.html")


# =========================================================
# ADMIN
# =========================================================

@app.route("/admin")
def admin():
    return render_template("admin.html")


# =========================================================
# START COURSE ASSESSMENT
# =========================================================

@app.route("/complete-course/<course_name>")
def complete_course(course_name):

    return redirect(
        url_for(
            "course_quiz",
            course_name=course_name
        )
    )


# =========================================================
# COURSE ASSESSMENT
# =========================================================

@app.route(
    "/course-quiz/<course_name>",
    methods=["GET", "POST"]
)
def course_quiz(course_name):

    questions = [
        {
            "question": (
                "What is the main purpose of learning a skill?"
            ),
            "options": [
                "To build knowledge and practical ability",
                "To avoid practice",
                "To skip assessments",
                "None of these"
            ],
            "answer": (
                "To build knowledge and practical ability"
            )
        },
        {
            "question": (
                "What should a learner do after studying a topic?"
            ),
            "options": [
                "Practice and apply it",
                "Forget it",
                "Skip the topic",
                "Do nothing"
            ],
            "answer": "Practice and apply it"
        },
        {
            "question": (
                "Why is assessment useful?"
            ),
            "options": [
                "It helps understand learning progress",
                "It prevents learning",
                "It removes the need to practice",
                "None of these"
            ],
            "answer": (
                "It helps understand learning progress"
            )
        }
    ]

    # -----------------------------------------------------
    # WHEN USER SUBMITS THE ASSESSMENT
    # -----------------------------------------------------

    if request.method == "POST":

        score = 0

        for index, question in enumerate(questions):

            selected_answer = request.form.get(
                f"question_{index}"
            )

            if selected_answer == question["answer"]:

                score += 1

        # -------------------------------------------------
        # PASS CONDITION
        # 2 OUT OF 3
        # -------------------------------------------------

        if score >= 2:

            if "completed_courses" not in session:

                session["completed_courses"] = []

            completed_courses = session[
                "completed_courses"
            ]

            if course_name not in completed_courses:

                completed_courses.append(
                    course_name
                )

                session[
                    "completed_courses"
                ] = completed_courses

            return render_template(
                "quiz_result.html",
                course_name=course_name,
                score=score,
                passed=True
            )

        # -------------------------------------------------
        # FAILED ASSESSMENT
        # -------------------------------------------------

        return render_template(
            "quiz_result.html",
            course_name=course_name,
            score=score,
            passed=False
        )

    # -----------------------------------------------------
    # SHOW ASSESSMENT
    # -----------------------------------------------------

    return render_template(
        "course_quiz.html",
        course_name=course_name,
        questions=questions
    )


# =========================================================
# VIEW CERTIFICATE
# =========================================================

@app.route("/certificate/<course_name>")
def certificate(course_name):

    completed_courses = session.get(
        "completed_courses",
        []
    )

    # Certificate is available only after passing
    # the assessment.
    if course_name not in completed_courses:

        return redirect(
            url_for("certifications")
        )

    certificate_id = (
        "CC-"
        + course_name.upper().replace(" ", "-")
        + "-001"
    )

    return render_template(
        "certificate.html",
        course_name=course_name,
        certificate_id=certificate_id,
        learner=session.get(
            "user",
            "Capacity Connect Learner"
        )
    )


# =========================================================
# RUN APPLICATION
# =========================================================

if __name__ == "__main__":
    app.run(debug=True)