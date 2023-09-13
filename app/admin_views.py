from app import app

@app.route("/admin/dashboard")
def admin_dashboard():
    return "admin dashboard"

@app.route("/admin/profile")
def admin_profile():
    return "admin profile"