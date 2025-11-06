from modelos.modelo import db, Modelo

class Usuario(Modelo):
    __tablename__ = "usuarios"

    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def verificar_usuario(self):
        pass

    def validar_acesso(self):
        pass
