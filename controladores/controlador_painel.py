from flask import Blueprint, request, render_template, redirect, session
from modelos import Moderador, Cliente, Cartao, Acesso
from datetime import date
from sqlalchemy import func

painel_blueprint = Blueprint(
    "painel", __name__, template_folder="../vistas/templates")


@painel_blueprint.before_request
def painel_before_request():
    if session.get("usuario") is None:
        return redirect("/")


@painel_blueprint.route("/painel")
def painel_home():
    moderador = Moderador.query.get_or_404(session["usuario"])
    quantidade_moderadores = len(Moderador.query.all())
    quantidade_clientes = len(Cliente.query.filter_by(tem_acesso=True).all())
    quantidade_cartoes = len(Cartao.query.filter_by(tem_acesso=True).all())
    acessos_hoje = len(Acesso.query.filter(
        func.date(Acesso.data_criacao) == date.today()).all())
    return render_template("home.html", moderador=moderador, quantidade_moderadores=quantidade_moderadores,
                           quantidade_clientes=quantidade_clientes, quantidade_cartoes=quantidade_cartoes, acessos_hoje=acessos_hoje)


@painel_blueprint.route("/logout")
def logout():
    session.clear()
    return redirect("/")


@painel_blueprint.route("/painel/historico")
def painel_historico():
    return render_template("historico.html")
