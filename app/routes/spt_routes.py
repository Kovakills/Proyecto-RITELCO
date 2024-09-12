from flask import Blueprint, render_template

bp = Blueprint('spt', __name__)

@bp.route('/spt')
def get_spt():
    return render_template('spt.html')