from flask import Flask, render_template, request, redirect, url_for, session, abort
from services import firebase_services
from firebase_admin import auth

app = Flask(__name__)
app.secret_key = "super-secret-key"


# ======================
# Helpers
# ======================

def login_required(role=None):
    if "uid" not in session:
        return redirect("/login")

    if role and session.get("role") != role:
        abort(403)

# ======================
# Public Pages
# ======================

@app.route("/")
def landing():
    return render_template("landing.html")

@app.route("/search")
def search():
    return render_template("search.html")

@app.route("/profile/<slug>")
def worker_profile(slug):
    return render_template("worker_profile.html", slug=slug)

# ======================
# Firebase Login Handler
# ======================

@app.route("/firebase-login", methods=["POST"])
def firebase_login():

    id_token = request.json.get("idToken")

    decoded = auth.verify_id_token(id_token)
    uid = decoded["uid"]

    user_ref = db.collection("users").document(uid).get()

    if user_ref.exists:
        role = user_ref.to_dict()["role"]
    else:
        role = None

    session["uid"] = uid
    session["role"] = role

    return {"status": "ok", "role": role}

# ======================
# Role Setup (First Time)
# ======================

@app.route("/select-role", methods=["POST"])
def select_role():

    role = request.form.get("role")
    uid = session["uid"]

    db.collection("users").document(uid).set({
        "role": role
    })

    session["role"] = role

    if role == "worker":
        return redirect("/worker/dashboard")
    else:
        return redirect("/customer/dashboard")

# ======================
# Dashboards
# ======================

@app.route("/worker/dashboard")
def worker_dashboard():
    check = login_required("worker")
    if check: return check
    return render_template("worker_dashboard.html")

@app.route("/customer/dashboard")
def customer_dashboard():
    check = login_required("customer")
    if check: return check
    return render_template("customer_dashboard.html")

# ======================
# Logout
# ======================

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

# ======================
# Error
# ======================

@app.errorhandler(403)
def forbidden(e):
    return "Forbidden", 403

# ======================
# Run
# ======================

if __name__ == "__main__":
    app.run(debug=True)
