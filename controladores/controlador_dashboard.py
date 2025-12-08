from flask import Blueprint, request, render_template, redirect, session, flash
from modelos import Moderador, Cliente

import json
import urllib.parse

dashboard_blueprint = Blueprint(
    "dashboard", __name__, template_folder="../vistas/templates")


@dashboard_blueprint.before_request
def admin_before_request():
    if session.get("usuario") is None:
        flash("Você não está logado", "danger")
        return redirect("/")
    moderador = Moderador.query.filter_by(id=session.get("usuario")).first()
    print(moderador.nome)
    if moderador.admin == False:
        flash("Você não tem permissões", "danger")
        return redirect("/painel")


@dashboard_blueprint.route("/painel/admin/dashboard")
def dashboard():
    grafico_moderador = criar_grafico_moderador()
    grafico_tipo_cliente = criar_grafico_tipo_cliente()
    return render_template("dashboard.html", grafico_moderador=grafico_moderador, grafico_tipo_cliente=grafico_tipo_cliente)


def criar_grafico(dicionario_grafico):
    return f"https://quickchart.io/chart?c={urllib.parse.quote(json.dumps(dicionario_grafico))}"


def criar_grafico_moderador():
    moderadores_ativos = Moderador.query.filter_by(ativo=True).count()
    moderadores_inativos = Moderador.query.filter_by(ativo=False).count()
    grafico = {
        "type": "outlabeledPie",
        "data": {
            "labels": ["Moderadores ativos", "Moderadores inativos"],
            "datasets": [{
                "backgroundColor": ["#1996C7", "#C52727"],
                "data": [moderadores_ativos, moderadores_inativos]
            }]
        },
        "options": {
            "plugins": {
                "legend": False,
                "outlabels": {
                    "text": "%l %p",
                    "color": "white",
                    "stretch": 35,
                    "font": {
                        "resizable": True,
                        "minSize": 12,
                        "maxSize": 18
                    }
                }
            }
        }
    }
    return criar_grafico(grafico)


def criar_grafico_tipo_cliente():
    alunos = Cliente.query.filter_by(tipo="aluno").count()
    professores = Cliente.query.filter_by(tipo="professor").count()
    visitantes = Cliente.query.filter_by(tipo="visitante").count()
    grafico = {
        "type": "bar",
        "data": {
            "labels": [
                "Visitantes",
                "Alunos",
                "Professores",
            ],
            "datasets": [
                {
                    "label": "Dataset 1",
                    "backgroundColor": ["rgba(52, 152, 219, 0.8)", "rgba(46, 204, 113, 0.8)", "rgba(230, 126, 34, 0.8)"],
                    "borderWidth": 1,
                    "data": [
                        visitantes,
                        alunos,
                        professores,
                    ]
                },
            ]
        },
        "options": {
            "responsive": True,
            "legend": {
                "display": False
            },
            "plugins": {

                "roundedBars": True
            }
        }
    }
    return criar_grafico(grafico)
