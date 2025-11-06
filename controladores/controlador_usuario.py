from flask import Blueprint, request, render_template, redirect
from modelos.usuario import Usuario

usuario_blueprint = Blueprint("usuario", __name__, template_folder="../vistas/templates")

@usuario_blueprint.route("/usuarios", methods=["GET", "POST"])
def listar_usuarios():
    if request.method == "GET":
        usuarios = Usuario.query.all()
        return render_template("usuarios.html", usuarios=usuarios)

    dados = request.form
    novo_usuario = Usuario(nome=dados["nome"], email=dados["email"])
    novo_usuario.salvar()
    return redirect("/usuarios")


@usuario_blueprint.route("/usuarios/validar_acesso/<int:usuario_id>", methods=["GET"])
def validar_acesso(usuario_id):
    usuario = Usuario.query.get_or_404(usuario_id)
    return usuario.validar_acesso()


@usuario_blueprint.route("/api/usuarios/<int:usuario_id>", methods=["DELETE"])
def deletar_usuario(usuario_id):
    usuario = Usuario.query.get_or_404(usuario_id)
    usuario.deletar()
    return {"mensagem": "Usuario deletado"}
