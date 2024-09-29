from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required
from ..models import Historial
from .. import db


bp = Blueprint('historial', __name__, url_prefix='/historial')


@bp.route('/', methods=['GET'])
@login_required
def ver_historial():
    historial = Historial.query.order_by(Historial.fecha.desc()).all()
    return render_template('historial/index.html', historial=historial)

@bp.route('/eliminar', methods=['POST'])
@login_required
def eliminar_historial():
    try:
        db.session.query(Historial).delete()  
        db.session.commit()
        flash('Historial de cambios eliminado exitosamente.', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error al eliminar el historial: {str(e)}', 'error')
    
    return redirect(url_for('historial.ver_historial'))
