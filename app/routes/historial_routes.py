from flask import Blueprint, render_template
from flask_login import login_required
from ..models import Historial

# Crear el blueprint para el historial
bp = Blueprint('historial', __name__, url_prefix='/historial')

# Ruta para ver el historial de cambios
@bp.route('/historial', methods=['GET'])
@login_required
def ver_historial():
    historial = Historial.query.order_by(Historial.fecha.desc()).all()
    return render_template('historial/index.html', historial=historial)
