from flask import Blueprint, render_template

bp = Blueprint('page', __name__)

@bp.route('/')
def get_spt():
    return render_template('page.html')