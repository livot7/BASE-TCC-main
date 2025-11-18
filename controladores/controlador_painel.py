from flask import Blueprint, request, render_template, redirect, session
from modelos import Moderador

painel_blueprint = Blueprint(
    "painel", __name__, template_folder="../vistas/templates")


@painel_blueprint.before_request
def painel_before_request():
    if session.get("usuario") is None:
        return redirect("/")


@painel_blueprint.route("/painel")
def painel_home():
    moderador = Moderador.query.get_or_404(session["usuario"])
    return render_template("home.html", moderador=moderador)


@painel_blueprint.route("/logout")
def logout():
    session.clear()
    return redirect("/")
