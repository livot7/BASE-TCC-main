from flask import Blueprint, request, render_template, redirect, session, flash, jsonify, url_for
from modelos import Moderador

admin_blueprint = Blueprint(
    "admin", __name__, template_folder="../vistas/templates")


@admin_blueprint.before_request
def admin_before_request():
    if session.get("usuario") is None:
        flash("Você não está logado", "danger")
        return redirect("/")
    moderador = Moderador.query.filter_by(id=session.get("usuario")).first()
    print(moderador.nome)
    if moderador.admin == False:
        flash("Você não tem permissões", "danger")
        return redirect("/painel")


@admin_blueprint.route("/painel/admin")
def painel_admin():
    return render_template("admin.html")


@admin_blueprint.route("/painel/admin/ver_moderadores/<int:pagina>", methods=["GET", "POST"])
def painel_ver_moderadores(pagina):
    if request.method == "GET":
        moderadores = Moderador.query.order_by(Moderador.id).paginate(
            page=pagina, per_page=10, error_out=False)

        return render_template("ver_moderadores.html", moderadores=moderadores, page=pagina)


@admin_blueprint.route("/painel/admin/editar_moderador/<int:id>", methods=["POST"])
def editar_moderador(id):
    moderador = Moderador.query.get_or_404(id)

    # Lendo os dados enviados via FormData
    moderador.nome = request.form.get("nome")
    moderador.admin = request.form.get("admin") == "1"
    moderador.ativo = request.form.get("ativo") == "1"

    moderador.salvar()

    return jsonify({
        "id": moderador.id,
        "nome": moderador.nome,
        "admin": moderador.admin,
        "ativo": moderador.ativo
    })


@admin_blueprint.route("/painel/admin/criar_moderador", methods=["GET", "POST"])
def painel_criar_moderador():
    if request.method == "GET":
        return render_template("criar_moderador.html")

    nome = request.form["nome"]
    email = request.form["email"]
    checkbox = request.form.get("administrador", "0") == "1"

    if Moderador.query.filter_by(email=email).first():
        flash("Esse moderador já existe", "warning")
        return redirect("/painel/admin/criar_moderador")
    moderador = Moderador(
        nome=nome,
        email=email,
        senha_hash="",
        admin=checkbox,
        ativo=True
    )
    moderador.salvar()
    flash(f"Moderador {nome} criado com sucesso", "success")
    return redirect("/painel/admin")
