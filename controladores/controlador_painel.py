from flask import Blueprint, request, render_template, redirect

painel_blueprint = Blueprint("painel", __name__, template_folder="../vistas/templates")

@painel_blueprint.route("/painel")
def painel_home():
    return render_template("home.html")