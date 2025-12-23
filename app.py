from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, login_required, UserMixin, current_user
from werkzeug.security import generate_password_hash, check_password_hash

# -------------------- APP CONFIG --------------------
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# -------------------- USER MODEL --------------------
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))
    email = db.Column(db.String(150), unique=True)
    password_hash = db.Column(db.String(150))
    security_q1 = db.Column(db.String(200))
    security_a1 = db.Column(db.String(200))
    security_q2 = db.Column(db.String(200))
    security_a2 = db.Column(db.String(200))
    bmr = db.Column(db.Float)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# -------------------- ROUTES --------------------
@app.route("/")
def index():
    return render_template("index.html")

# -------------------- REGISTER --------------------
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]
        confirm_password = request.form["confirm_password"]
        q1 = request.form["security_q1"]
        a1 = request.form["security_a1"]
        q2 = request.form["security_q2"]
        a2 = request.form["security_a2"]

        if password != confirm_password:
            flash("Passwords do not match")
            return redirect(url_for("register"))

        if User.query.filter_by(email=email).first():
            flash("Email already registered")
            return redirect(url_for("register"))

        new_user = User(
            name=name,
            email=email,
            password_hash=generate_password_hash(password),
            security_q1=q1,
            security_a1=generate_password_hash(a1),
            security_q2=q2,
            security_a2=generate_password_hash(a2)
        )
        db.session.add(new_user)
        db.session.commit()
        flash("Account created successfully! Please login.")
        return redirect(url_for("login"))

    return render_template("register.html")

# -------------------- LOGIN --------------------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for("index"))
        else:
            flash("Invalid email or password")
            return redirect(url_for("login"))

    return render_template("login.html")

# -------------------- LOGOUT --------------------
@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Logged out successfully")
    return redirect(url_for("index"))

# -------------------- FORGOT PASSWORD --------------------
@app.route("/forget-password", methods=["GET", "POST"])
def forget_password():
    step = 1
    message = None
    email = None
    question1 = None
    question2 = None

    if request.method == "POST":
        # Step 1: email
        if "email" in request.form and "a1" not in request.form:
            email = request.form["email"]
            user = User.query.filter_by(email=email).first()
            if user:
                question1 = user.security_q1
                question2 = user.security_q2
                step = 2
            else:
                message = "Email not found."

        # Step 2: security answers
        elif "a1" in request.form and "new_password" not in request.form:
            email = request.form["email"]
            a1 = request.form["a1"]
            a2 = request.form["a2"]
            user = User.query.filter_by(email=email).first()
            if user and check_password_hash(user.security_a1, a1) and check_password_hash(user.security_a2, a2):
                step = 3
            else:
                message = "Answers do not match. Try again."
                question1 = user.security_q1
                question2 = user.security_q2

        # Step 3: reset password
        elif "new_password" in request.form:
            email = request.form["email"]
            new_pass = request.form["new_password"]
            confirm_pass = request.form["confirm_password"]
            if new_pass != confirm_pass:
                message = "Passwords do not match."
                step = 3
            else:
                user = User.query.filter_by(email=email).first()
                user.password_hash = generate_password_hash(new_pass)
                db.session.commit()
                message = "Password reset successfully. You can now login."
                step = 1

    return render_template(
        "forget_password.html",
        step=step,
        message=message,
        email=email,
        question1=question1,
        question2=question2
    )

# -------------------- BMR CALCULATOR --------------------
def calculate_bmr(age, gender, height, weight):
    if gender == "male":
        return 88.362 + (13.397 * weight) + (4.799 * height) - (5.677 * age)
    else:
        return 447.593 + (9.247 * weight) + (3.098 * height) - (4.330 * age)

@app.route("/bmr", methods=["GET", "POST"])
@login_required
def bmr():
    bmr_result = None
    bmr_message = None

    if request.method == "POST":
        age = int(request.form["age"])
        gender = request.form["gender"]
        height = float(request.form["height"])
        weight = float(request.form["weight"])

        bmr_value = calculate_bmr(age, gender, height, weight)
        bmr_result = round(bmr_value, 2)

        current_user.bmr = bmr_result
        db.session.commit()

        if bmr_result < 1400:
            bmr_message = "Your BMR is low. You may need to improve calorie intake."
        elif bmr_result < 1800:
            bmr_message = "Your BMR is within a normal range."
        else:
            bmr_message = "Your BMR is high. You burn calories faster than average."

    return render_template("bmr_calculator.html", bmr_result=bmr_result, bmr_message=bmr_message)

# -------------------- HEALTH ASSESSMENT --------------------
@app.route("/health-assessment", methods=["GET", "POST"])
@login_required
def health_assessment():
    assessment_result = None
    assessment_message = None

    if request.method == "POST":
        score = (
            int(request.form["smoking"]) +
            int(request.form["alcohol"]) +
            int(request.form["exercise"]) +
            int(request.form["sleep"]) +
            int(request.form["stress"])
        )

        if score <= 5:
            assessment_result = "Low Risk"
            assessment_message = "Your lifestyle habits are generally healthy."
        elif score <= 12:
            assessment_result = "Moderate Risk"
            assessment_message = "Some improvements in lifestyle are recommended."
        else:
            assessment_result = "High Risk"
            assessment_message = "Immediate lifestyle changes are advised."

    return render_template(
        "health_assessment.html",
        assessment_result=assessment_result,
        assessment_message=assessment_message
    )

# -------------------- DIET PLAN --------------------
@app.route("/diet-plan", methods=["GET", "POST"])
@login_required
def diet_plan():
    diet_plan = None
    calories = None
    diet_message = None

    if request.method == "POST":
        bmr = float(request.form["bmr_value"])
        calories = round(bmr * 1.5)  # assume moderate activity
        diet_plan = [
            "Breakfast: Oatmeal with fruits + milk",
            "Snack: Handful of nuts",
            "Lunch: Grilled chicken / tofu + brown rice + vegetables",
            "Snack: Yogurt or fruit smoothie",
            "Dinner: Fish / lentils + salad + whole grains"
        ]
        diet_message = "This is a general diet plan. Adjust portions as per your needs."

    return render_template(
        "diet_plan.html",
        diet_plan=diet_plan,
        calories=calories,
        diet_message=diet_message
    )

# -------------------- TERMS & PRIVACY --------------------
@app.route("/terms")
def terms():
    return render_template("terms.html")

@app.route("/privacy")
def privacy():
    return render_template("privacy.html")

# -------------------- RUN APP --------------------
if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # create tables if not exist
    app.run(debug=True)
