from flask import Blueprint, request, render_template, redirect, url_for, flash
from flask_login import login_required
from ..models.equipos_media_tension import EquiposMediaTension
from ..models.estante import Estantes
from .. import db

bp = Blueprint('equipos_media_tension', __name__)

@bp.route('/equipos_media_tension', methods=['GET'])
@login_required
def get_media_tension(): 
    data = EquiposMediaTension.query.all()
    return render_template('Mtension/index.html', data=data)

@bp.route('/equipos_media_tension/add', methods=['GET', 'POST'])
@login_required
def add_media_tension():
    if request.method == 'POST':
        unidad_medida = request.form['unidad_medida']
        descripcion_producto = request.form['descripcion_producto']
        cantidad = int(request.form['cantidad'])
        observacion = request.form['observacion']
        estante_id = request.form['estante_id']

        estante = Estantes.query.get(estante_id)
        if estante is None:
            flash('El estante con el ID proporcionado no existe.', 'error')
            return redirect(url_for('media_tension.add_media_tension'))

        new_equipobt = EquiposMediaTension(unidad_medida=unidad_medida, descripcion_producto=descripcion_producto, cantidad=cantidad, observacion=observacion, estante_id=estante_id)
        db.session.add(new_equipobt)
        db.session.commit()
        flash('Equipo de baja tension agregado exitosamente', 'success')
        return redirect(url_for('equipos_media_tension.get_media_tension'))
    
    estantes = Estantes.query.all()
    
    return render_template('Mtension/add.html', estantes=estantes)

@bp.route('/equipos_media_tension/edit/<int:idmediatension>', methods=['GET', 'POST'])
@login_required
def edit_media_tension(idmediatension):
    media_tension = EquiposMediaTension.query.get_or_404(idmediatension)

    if request.method == 'POST':
        media_tension.unidad_medida = request.form['unidad_medida']
        media_tension.estante_id = request.form['estante_id']
        media_tension.descripcion_producto = request.form['descripcion_producto']
        media_tension.observacion = request.form['observacion']
        media_tension.cantidad = int(request.form['cantidad'])
        db.session.commit()
        return redirect(url_for('equipos_media_tension.get_media_tension', idmediatension=idmediatension))
    
    estantes = Estantes.query.all()
    
    return render_template('Mtension/edit.html', media_tension=media_tension, estantes=estantes)




@bp.route('/equipos_media_tension/delete/<int:idmediatension>', methods=['POST'])
@login_required
def delete_media_tension(idmediatension):
    equipobt = EquiposMediaTension.query.get_or_404(idmediatension)
    db.session.delete(equipobt)
    db.session.commit()
    flash('Equipo eliminado exitosamente', 'success')
    return redirect(url_for('equipos_media_tension.get_media_tension'))