import argparse
from werkzeug.security import generate_password_hash

from app import app
from modelos.moderador import Moderador

parser = argparse.ArgumentParser(description="VIA")
parser.add_argument("--criar_admin", help="Cria um admin", action="store_true")

args = parser.parse_args()

if args.criar_admin:
    nome = input("Nome: ")
    email = input("Email: ")
    senha = input("Senha: ")

    # Como estamos fazendo isso por fora do flash, temos que chamar essa função
    with app.app_context():
        novo_admin = Moderador(
            nome=nome,
            email=email,
            # Criptografia da senha
            senha_hash=generate_password_hash(senha),
            admin=True,
        )
        novo_admin.salvar()
