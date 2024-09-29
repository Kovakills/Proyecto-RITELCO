from flask import Blueprint, render_template, jsonify

bp = Blueprint('page', __name__)

@bp.route('/')
def get_spt():
    return render_template('page.html')


@bp.route('/api/data')
def get_data():
    return jsonify({"message": "¡Hola desde Flask!"})
