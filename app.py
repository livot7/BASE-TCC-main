from flask import Flask
from flask_migrate import Migrate

from config import Config
from modelos.modelo import db
from controladores.controlador_principal import principal_blueprint
from controladores.controlador_painel import painel_blueprint
from controladores.controlador_admin import admin_blueprint

app = Flask(__name__)
app.config.from_object(Config)

# Banco de dados + migração
db.init_app(app)
migrate = Migrate(app, db)

# Registra as blueprints
app.register_blueprint(principal_blueprint)
app.register_blueprint(painel_blueprint)
app.register_blueprint(admin_blueprint)

if __name__ == "__main__":
    app.run(debug=True)
