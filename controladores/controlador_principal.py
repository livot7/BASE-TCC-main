from flask import Blueprint, request, render_template, redirect

principal_blueprint = Blueprint("principal", __name__, template_folder="../vistas/templates")

@principal_blueprint.route("/")
def index():
    return render_template("login.html")