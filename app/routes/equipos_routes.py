from flask import Blueprint, render_template

bp = Blueprint('equipos', __name__)

@bp.route('/equipos')
def get_spt():
    return render_template('equipos.html')