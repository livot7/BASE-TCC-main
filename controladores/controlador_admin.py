from flask import Blueprint, request, render_template, redirect

admin_blueprint = Blueprint("admin", __name__, template_folder="../vistas/templates")

@admin_blueprint.route("/painel/admin")
def painel_admin():
    return "painel admin"