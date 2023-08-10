from flask import Blueprint, render_template, request, redirect
from flask_login import login_user, logout_user, current_user
from naturerec_model.logic import authenticate
from naturerec_web.auth.requires_roles import has_roles

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

            # If the user can edit sightings, redirect to the sightings editing page. Otherwise, redirect
            # to the sightings listing page
            if has_roles(["Administrator", "Reporter"]):
                return redirect("/sightings/edit")
            else:
                return redirect("/sightings/list")
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


def unauthorised(_):
    """
    Renders the "unauthorised" page when abort(401) is called

    :param _: The error, which is currently ignored
    """
    if not current_user:
        return render_template("auth/login.html", error=None)
    else:
        return render_template("auth/unauthorised.html"), 401
