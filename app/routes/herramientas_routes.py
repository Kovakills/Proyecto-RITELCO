from flask import Blueprint, render_template

bp = Blueprint('herramientas', __name__)

@bp.route('/herramientas')
def get_herramientas():
    return render_template('herramientas.html')