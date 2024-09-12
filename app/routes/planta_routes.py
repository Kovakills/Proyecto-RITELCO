# planta_routes.py
from flask import Blueprint, render_template

bp = Blueprint('planta', __name__)

@bp.route('/planta')
def get_planta():
    return render_template('planta.html')
