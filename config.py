class Config:
    SQLALCHEMY_DATABASE_URI = "sqlite:///via.sqlite3"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # TODO: Esconder chave secreta
    SECRET_KEY = "dev"
