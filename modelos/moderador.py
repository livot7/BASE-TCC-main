from modelos.modelo import db, Modelo


class Moderador(Modelo):
    __tablename__ = "moderadores"

    nome = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    senha_hash = db.Column(db.String(512), nullable=False)
    admin = db.Column(db.Boolean, nullable=False)

    def verificar_usuario(self):
        pass

    def validar_acesso(self):
        pass
