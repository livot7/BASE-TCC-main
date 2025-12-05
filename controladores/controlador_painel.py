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


@painel_blueprint.route("/painel/historico/<int:pagina>", methods=["GET", "POST"])
def painel_historico(pagina):
    if request.method == "GET":
        nomes = Cliente.query.paginate(
            per_page=10, page=pagina, error_out=False)

        acessos = Acesso.query.paginate(
            per_page=10, page=pagina, error_out=False)
        return render_template("historico.html", acessos=acessos, page=pagina)


@painel_blueprint.route("/painel/cartoes/<int:pagina>", methods=["GET", "POST"])
def painel_cartao(pagina):
    if request.method == "GET":
        cartoes = Cartao.query.paginate(
            per_page=10, page=pagina, error_out=False)
        return render_template("cartoes.html", cartoes=cartoes, page=pagina)


@painel_blueprint.route("/painel/clientes/<int:pagina>")
def painel_clientes(pagina):
    clientes = Cliente.query.order_by(Cliente.id).paginate(
        page=pagina, per_page=6, error_out=False)
    return render_template("ver_clientes.html", clientes=clientes, page=pagina)


@painel_blueprint.put("/htmx/editar_cliente/<int:id>")
def editar_cliente(id):
    cliente = Cliente.query.get_or_404(id)

    cliente.nome = request.form.get("nome")
    cliente.documento = request.form.get("documento")
    cliente.tipo = request.form.get("tipo")
    cliente.tem_acesso = "tem_acesso" in request.form
    cliente.documento_valido = "documento_valido" in request.form

    cliente.salvar()

    return render_template("componentes/card_cliente_unico.html", cliente=cliente)


@painel_blueprint.route("/htmx/buscar_clientes")
def buscar_clientes():
    pesquisa = request.args.get("nome", "").strip()
    clientes_filtrados = Cliente.query.filter(
        Cliente.nome.ilike(f"%{pesquisa}%")
    ).paginate(per_page=6)

    return render_template("componentes/card_cliente.html", clientes=clientes_filtrados)
