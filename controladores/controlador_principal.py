from flask import Blueprint, request, render_template, redirect, session, flash
from modelos import Moderador
from werkzeug.security import check_password_hash


principal_blueprint = Blueprint(
    "principal", __name__, template_folder="../vistas/templates")


@principal_blueprint.route("/", methods=["GET", "POST"])
def index():
    if session.get("usuario"):
        flash("Você já está logado.", "warning")
        return redirect("/painel")

    if request.method == "GET":
        return render_template("login.html")

    senha = request.form["senha"]
    email = request.form["email"]

    moderador = Moderador.query.filter_by(email=email).first()
    if moderador is None:
        flash("Email ou senha incorretos.", "danger")
        return redirect("/")

    if not check_password_hash(moderador.senha_hash, senha):
        flash("Email ou senha incorretos.", "danger")
        return redirect("/")

    session["usuario"] = moderador.id
    flash("Logado com sucesso!", "success")
    return redirect("/painel")
