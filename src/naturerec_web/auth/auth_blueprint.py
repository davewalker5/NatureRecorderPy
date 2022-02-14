from flask import Blueprint, render_template, request, redirect
from flask_login import login_user, logout_user
from naturerec_model.logic import authenticate

auth_bp = Blueprint("auth", __name__, template_folder='templates')


@auth_bp.route('/login', methods=["GET", "POST"])
def login():
    """
    Show the login form and authenticate when the user attempts to login

    :return: The HTML for the login page
    """
    if request.method == "POST":
        try:
            username = request.form["username"]
            password = request.form["password"]
            remember = "remember" in request.form
            user = authenticate(username, password)
            login_user(user, remember=remember)
            return redirect("/sightings/edit")
        except ValueError:
            return render_template("auth/login.html", error="Invalid login details")
    else:
        return render_template("auth/login.html", error=None)


@auth_bp.route('/logout')
def logout():
    """
    Log the current user out

    :return: Redirect to the login page
    """
    logout_user()
    return redirect("/auth/login")
