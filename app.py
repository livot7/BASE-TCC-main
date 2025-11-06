from flask import Flask
from flask_migrate import Migrate

from config import Config
from modelos.modelo import db
from controladores.controlador_usuario import usuario_blueprint

app = Flask(__name__)
app.config.from_object(Config)

# Banco de dados + migração
db.init_app(app)
migrate = Migrate(app, db)

# Registra as blueprints
app.register_blueprint(usuario_blueprint)

if __name__ == "__main__":
    app.run(debug=True)
