from flask import Blueprint, request, render_template, redirect, session

painel_blueprint = Blueprint("painel", __name__, template_folder="../vistas/templates")

@painel_blueprint.before_request
def painel_before_request():
    if session.get("usuario") is None:
        return redirect("/")

@painel_blueprint.route("/painel")
def painel_home():
    return render_template("home.html")

@painel_blueprint.route("/logout")
def logout():
    session.clear()
    return redirect("/")
