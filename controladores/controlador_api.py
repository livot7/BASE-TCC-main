from flask import Blueprint, request, render_template, redirect, session, flash,jsonify
from modelos import Cartao, Acesso

api_blueprint = Blueprint(
    "api", __name__, template_folder="../vistas/templates")

@api_blueprint.route("/api_cartao", methods=["POST"])
def api_cartao():
    try:
        cartao_info = request.get_json()
        if not cartao_info or "uid" not in cartao_info:
            return jsonify({"status": "erro", "mensagem": "JSON inválido"}), 400

        cartao_id = cartao_info["uid"]
        cartao_encontrado = Cartao.query.filter_by(chave_cartao=cartao_id).first()

        if cartao_encontrado:
            if cartao_encontrado.tem_acesso:
                acesso = Acesso(
                    usuario_id=cartao_encontrado.dono_id,
                    cartao_id=cartao_id,
                    tipo_acesso="Entrada",
                    local="Portaria Principal"
                )
                acesso.salvar()
                return jsonify({"status": "ok", "mensagem": "Acesso liberado"}), 200
            else:
                return jsonify({"status": "negado", "mensagem": "Acesso bloqueado"}), 403
        else:
            cartao = Cartao(
                dono_id=" ",
                chave_cartao=cartao_id,
                tem_acesso=False
            )
            cartao.salvar()
            return jsonify({"status": "negado", "mensagem": "Cartão registrado, acesso bloqueado"}), 403

    except Exception as e:
        # Isso retorna o erro para debug
        print("Erro na rota /api_cartao:", e)
        return jsonify({"status": "erro", "mensagem": str(e)}), 500
