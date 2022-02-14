from flask import Blueprint, render_template, request, redirect

auth_bp = Blueprint("auth", __name__, template_folder='templates')


@auth_bp.route('/login')
def login():
    return render_template('auth/login.html')


@auth_bp.route('/logout')
def logout():
    return 'logout'
