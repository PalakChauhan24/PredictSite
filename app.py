from flask import Flask, render_template, request, redirect, url_for, session
import joblib
import os
import json
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)


# ============================================================
# PROJECT PATH
# ============================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


# ============================================================
# FILE PATHS
# ============================================================

MODEL_FILE = os.path.join(
    BASE_DIR,
    "model",
    "disease_model.pkl"
)

SYMPTOMS_FILE = os.path.join(
    BASE_DIR,
    "model",
    "symptoms.pkl"
)

USERS_FILE = os.path.join(
    BASE_DIR,
    "users.json"
)

HISTORY_FILE = os.path.join(
    BASE_DIR,
    "prediction_history.json"
)

FEEDBACK_FILE = os.path.join(
    BASE_DIR,
    "feedback.json"
)


# ============================================================
# FLASK CONFIGURATION
# ============================================================

app.secret_key = "predictsite_secret_key_2026"


# ============================================================
# LOAD MODEL
# ============================================================

model = joblib.load(MODEL_FILE)
symptoms = joblib.load(SYMPTOMS_FILE)


# ============================================================
# CONDITION INFORMATION
# ============================================================

condition_info = {

    "Fungal infection":
        "A fungal infection is caused by fungi and can affect the skin or other parts of the body.",

    "Allergy":
        "An allergy occurs when the immune system reacts to a substance that is normally harmless.",

    "GERD":
        "GERD is a digestive condition in which stomach contents can flow back into the esophagus.",

    "Chronic cholestasis":
        "Cholestasis involves reduced or blocked flow of bile from the liver.",

    "Drug Reaction":
        "A drug reaction is an unwanted response that may occur after taking a medication.",

    "Peptic ulcer disease":
        "Peptic ulcers are sores that develop in the lining of the stomach or upper intestine.",

    "Gastroenteritis":
        "Gastroenteritis is inflammation of the stomach and intestines, often caused by infection.",

    "Bronchial Asthma":
        "Asthma is a condition in which the airways can become inflamed and narrowed.",

    "Hypertension":
        "Hypertension means blood pressure is consistently higher than the recommended range.",

    "Migraine":
        "Migraine is a neurological condition that can cause recurring headaches and other symptoms."
}


# ============================================================
# USER FUNCTIONS
# ============================================================

def load_users():

    if not os.path.exists(USERS_FILE):
        return {}

    try:

        with open(
            USERS_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            users = json.load(file)

            if isinstance(users, dict):
                return users

            return {}

    except (
        json.JSONDecodeError,
        OSError
    ):

        return {}


def save_users(users):

    try:

        with open(
            USERS_FILE,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                users,
                file,
                indent=4,
                ensure_ascii=False
            )

    except OSError:

        pass


# ============================================================
# HISTORY FUNCTIONS
# ============================================================

def load_history():

    if not os.path.exists(HISTORY_FILE):
        return {}

    try:

        with open(
            HISTORY_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            history = json.load(file)

            if isinstance(history, dict):
                return history

            return {}

    except (
        json.JSONDecodeError,
        OSError
    ):

        return {}


def save_history(history):

    try:

        with open(
            HISTORY_FILE,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                history,
                file,
                indent=4,
                ensure_ascii=False
            )

    except OSError:

        pass


def add_prediction_to_history(
    email,
    prediction,
    confidence,
    selected_symptoms
):

    history = load_history()

    if email not in history:
        history[email] = []

    history_entry = {

        "prediction": prediction,

        "confidence": confidence,

        "symptoms": selected_symptoms,

        "date": datetime.now().strftime(
            "%d %B %Y"
        ),

        "time": datetime.now().strftime(
            "%I:%M %p"
        )
    }

    history[email].insert(
        0,
        history_entry
    )

    # Keep only latest 20 predictions
    history[email] = history[email][:20]

    save_history(history)


# ============================================================
# FEEDBACK FUNCTIONS
# ============================================================

def load_feedback():

    if not os.path.exists(FEEDBACK_FILE):
        return {}

    try:

        with open(
            FEEDBACK_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            feedback = json.load(file)

            if isinstance(feedback, dict):
                return feedback

            return {}

    except (
        json.JSONDecodeError,
        OSError
    ):

        return {}


def save_feedback(feedback):

    try:

        with open(
            FEEDBACK_FILE,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                feedback,
                file,
                indent=4,
                ensure_ascii=False
            )

    except OSError:

        pass


def add_feedback(
    email,
    prediction,
    confidence,
    selected_symptoms,
    feedback_value
):

    feedback_data = load_feedback()

    if email not in feedback_data:
        feedback_data[email] = []

    feedback_entry = {

        "prediction": prediction,

        "confidence": confidence,

        "symptoms": selected_symptoms,

        "feedback": feedback_value,

        "date": datetime.now().strftime(
            "%d %B %Y"
        ),

        "time": datetime.now().strftime(
            "%I:%M %p"
        )
    }

    feedback_data[email].insert(
        0,
        feedback_entry
    )

    # Keep latest 20 feedback entries
    feedback_data[email] = feedback_data[email][:20]

    save_feedback(feedback_data)


# ============================================================
# LOGIN CHECK
# ============================================================

def is_logged_in():

    return "user_email" in session


# ============================================================
# LOGIN PAGE
# ============================================================

@app.route(
    "/login",
    methods=["GET", "POST"]
)
def login():

    if is_logged_in():

        return redirect(
            url_for("home")
        )

    error = None

    if request.method == "POST":

        email = request.form.get(
            "email",
            ""
        ).strip().lower()

        password = request.form.get(
            "password",
            ""
        )

        users = load_users()

        if email not in users:

            error = "No account found with this email."

        elif not check_password_hash(
            users[email]["password"],
            password
        ):

            error = "Incorrect password."

        else:

            session["user_email"] = email

            session["user_name"] = users[email]["name"]

            return redirect(
                url_for("home")
            )

    return render_template(
        "login.html",
        error=error
    )


# ============================================================
# FORGOT PASSWORD
# ============================================================

@app.route(
    "/forgot-password",
    methods=["GET", "POST"]
)
def forgot_password():

    if is_logged_in():

        return redirect(
            url_for("home")
        )

    error = None
    success = None

    if request.method == "POST":

        email = request.form.get(
            "email",
            ""
        ).strip().lower()

        new_password = request.form.get(
            "new_password",
            ""
        )

        confirm_password = request.form.get(
            "confirm_password",
            ""
        )

        users = load_users()

        # --------------------------------
        # VALIDATION
        # --------------------------------

        if not email:

            error = "Please enter your email address."

        elif "@" not in email:

            error = "Please enter a valid email address."

        elif email not in users:

            error = "No account found with this email."

        elif len(new_password) < 6:

            error = "Password must contain at least 6 characters."

        elif new_password != confirm_password:

            error = "Passwords do not match."

        else:

            # --------------------------------
            # UPDATE PASSWORD
            # --------------------------------

            users[email]["password"] = (
                generate_password_hash(
                    new_password
                )
            )

            save_users(users)

            success = (
                "Password reset successfully! "
                "You can now login with your new password."
            )

    return render_template(
        "forgot_password.html",
        error=error,
        success=success
    )


# ============================================================
# SIGNUP PAGE
# ============================================================

@app.route(
    "/signup",
    methods=["GET", "POST"]
)
def signup():

    if is_logged_in():

        return redirect(
            url_for("home")
        )

    error = None

    if request.method == "POST":

        name = request.form.get(
            "name",
            ""
        ).strip()

        email = request.form.get(
            "email",
            ""
        ).strip().lower()

        password = request.form.get(
            "password",
            ""
        )

        confirm_password = request.form.get(
            "confirm_password",
            ""
        )

        users = load_users()

        # ------------------------------
        # VALIDATION
        # ------------------------------

        if not name:

            error = "Please enter your name."

        elif not email:

            error = "Please enter your email."

        elif "@" not in email:

            error = "Please enter a valid email address."

        elif len(password) < 6:

            error = "Password must contain at least 6 characters."

        elif password != confirm_password:

            error = "Passwords do not match."

        elif email in users:

            error = "An account with this email already exists."

        # ------------------------------
        # CREATE ACCOUNT
        # ------------------------------

        else:

            users[email] = {

                "name": name,

                "email": email,

                "password":
                    generate_password_hash(
                        password
                    )
            }

            save_users(users)

            # Create empty history
            history = load_history()

            if email not in history:

                history[email] = []

                save_history(history)

            # Create empty feedback
            feedback = load_feedback()

            if email not in feedback:

                feedback[email] = []

                save_feedback(feedback)

            session["user_email"] = email

            session["user_name"] = name

            return redirect(
                url_for("home")
            )

    return render_template(
        "signup.html",
        error=error
    )


# ============================================================
# LOGOUT
# ============================================================

@app.route("/logout")
def logout():

    session.clear()

    return redirect(
        url_for("login")
    )


# ============================================================
# HOME
# ============================================================

@app.route("/")
def home():

    if not is_logged_in():

        return redirect(
            url_for("login")
        )

    display_symptoms = []

    for symptom in symptoms:

        display_name = symptom.replace(
            "_",
            " "
        ).title()

        display_symptoms.append({

            "value": symptom,

            "name": display_name
        })

    return render_template(
        "index.html",
        symptoms=display_symptoms,
        user_name=session.get(
            "user_name",
            "User"
        )
    )


# ============================================================
# PREDICTION
# ============================================================

@app.route(
    "/predict",
    methods=["POST"]
)
def predict():

    if not is_logged_in():

        return redirect(
            url_for("login")
        )

    selected_symptoms = request.form.getlist(
        "symptoms"
    )

    input_data = [
        0
    ] * len(symptoms)

    for symptom in selected_symptoms:

        if symptom in symptoms:

            index = symptoms.index(
                symptom
            )

            input_data[index] = 1

    prediction = model.predict(
        [input_data]
    )[0]

    confidence = None

    if hasattr(
        model,
        "predict_proba"
    ):

        probabilities = model.predict_proba(
            [input_data]
        )[0]

        confidence = round(
            max(probabilities) * 100,
            2
        )

    information = condition_info.get(

        prediction,

        "Educational information for this condition is not available yet."
    )

    # Save history
    add_prediction_to_history(

        session["user_email"],

        prediction,

        confidence,

        selected_symptoms
    )

    return render_template(

        "result.html",

        prediction=prediction,

        confidence=confidence,

        information=information,

        selected_symptoms=selected_symptoms,

        user_name=session.get(
            "user_name",
            "User"
        )
    )


# ============================================================
# PREDICTION FEEDBACK
# ============================================================

@app.route(
    "/feedback",
    methods=["POST"]
)
def feedback():

    if not is_logged_in():

        return redirect(
            url_for("login")
        )

    prediction = request.form.get(
        "prediction",
        ""
    ).strip()

    confidence_value = request.form.get(
        "confidence",
        ""
    ).strip()

    selected_symptoms = request.form.getlist(
        "symptoms"
    )

    feedback_value = request.form.get(
        "feedback",
        ""
    ).strip().lower()

    # --------------------------------
    # VALID FEEDBACK VALUES
    # --------------------------------

    if feedback_value not in [
        "yes",
        "no"
    ]:

        return redirect(
            url_for("home")
        )

    # --------------------------------
    # CONVERT CONFIDENCE
    # --------------------------------

    confidence = None

    if confidence_value:

        try:

            confidence = float(
                confidence_value
            )

        except ValueError:

            confidence = None

    # --------------------------------
    # SAVE FEEDBACK
    # --------------------------------

    add_feedback(

        session["user_email"],

        prediction,

        confidence,

        selected_symptoms,

        feedback_value
    )

    information = condition_info.get(

        prediction,

        "Educational information for this condition is not available yet."
    )

    return render_template(

        "result.html",

        prediction=prediction,

        confidence=confidence,

        information=information,

        selected_symptoms=selected_symptoms,

        user_name=session.get(
            "user_name",
            "User"
        ),

        feedback_submitted=True,

        feedback_value=feedback_value
    )


# ============================================================
# HISTORY
# ============================================================

@app.route("/history")
def history():

    if not is_logged_in():

        return redirect(
            url_for("login")
        )

    history_data = load_history()

    user_history = history_data.get(

        session["user_email"],

        []
    )

    return render_template(

        "history.html",

        history=user_history,

        user_name=session.get(
            "user_name",
            "User"
        )
    )


# ============================================================
# CLEAR USER HISTORY
# ============================================================

@app.route(
    "/clear-history",
    methods=["POST"]
)
def clear_history():

    if not is_logged_in():

        return redirect(
            url_for("login")
        )

    history = load_history()

    email = session["user_email"]

    history[email] = []

    save_history(history)

    return redirect(
        url_for("history")
    )


# ============================================================
# RUN APPLICATION
# ============================================================

if __name__ == "__main__":

    app.run(
        debug=True
    )