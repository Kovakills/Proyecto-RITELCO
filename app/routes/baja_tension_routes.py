from flask import Blueprint, request, render_template, redirect, url_for, flash
from flask_login import login_required
from ..models.baja_tension import BajaTension
from ..models.estante import Estantes
from .. import db

bp = Blueprint('baja_tension', __name__)

@bp.route('/Btension', methods=['GET'])
@login_required
def get_baja_tension(): 
    data = BajaTension.query.all()
    return render_template('Btension/index.html', data=data)

@bp.route('/Btension/add', methods=['GET', 'POST'])
@login_required
def add_baja_tension():
    if request.method == 'POST':
        unidad_medida = request.form['unidad_medida']
        descripcion_producto = request.form['descripcion_producto']
        cantidad = int(request.form['cantidad'])
        observacion = request.form['observacion']
        estante_id = request.form['estante_id']

        estante = Estantes.query.get(estante_id)
        if estante is None:
            flash('El estante con el ID proporcionado no existe.', 'error')
            return redirect(url_for('baja_tension.add_baja_tension'))

        new_equipobt = BajaTension(unidad_medida=unidad_medida, descripcion_producto=descripcion_producto, cantidad=cantidad, observacion=observacion, estante_id=estante_id)
        db.session.add(new_equipobt)
        db.session.commit()
        flash('Equipo de baja tension agregado exitosamente', 'success')
        return redirect(url_for('baja_tension.get_baja_tension'))
    
    estantes = Estantes.query.all()
    
    return render_template('Btension/add.html', estantes=estantes)

@bp.route('/Btension/edit/<int:idbajatension>', methods=['GET', 'POST'])
@login_required
def edit_bajatension(idbajatension):
    baja_tension = BajaTension.query.get_or_404(idbajatension)

    if request.method == 'POST':
        baja_tension.unidad_medida = request.form['unidad_medida']
        baja_tension.estante_id = request.form['estante_id']
        baja_tension.descripcion_producto = request.form['descripcion_producto']
        baja_tension.observacion = request.form['observacion']
        baja_tension.cantidad = int(request.form['cantidad'])

        db.session.commit()
        return redirect(url_for('baja_tension.get_baja_tension', idbajatension=idbajatension))
    estantes = Estantes.query.all()
    return render_template('Btension/edit.html', baja_tension=baja_tension, estantes=estantes)



@bp.route('/Btension/delete/<int:idbajatension>', methods=['POST'])
@login_required
def delete_baja_tension(idbajatension):
    equipobt = BajaTension.query.get_or_404(idbajatension)
    db.session.delete(equipobt)
    db.session.commit()
    flash('Equipo eliminado exitosamente', 'success')
    return redirect(url_for('baja_tension.get_baja_tension'))