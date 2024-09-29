from flask import Blueprint, request, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from ..models.equipos_media_tension import EquiposMediaTension
from ..models.estante import Estantes
from ..models.historial import Historial
from .. import db
from datetime import datetime

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

        # Verificar si el estante_id existe
        estante = Estantes.query.get(estante_id)
        if estante is None:
            flash('El estante con el ID proporcionado no existe.', 'error')
            return redirect(url_for('equipos_media_tension.add_media_tension'))

        new_equipobt = EquiposMediaTension(
            unidad_medida=unidad_medida,
            descripcion_producto=descripcion_producto,
            cantidad=cantidad,
            observacion=observacion,
            estante_id=estante_id
        )
        db.session.add(new_equipobt)
        db.session.commit()

        # Registro en el historial
        nuevo_historial = Historial(
            usuario_id=current_user.id,
            tabla="EquiposMediaTension",
            accion=f"Agregó equipo de media tensión: Unidad medida: {unidad_medida}, Descripción: {descripcion_producto}, Cantidad: {cantidad}, Observación: {observacion}, Estante ID: {estante_id}",
            fecha=datetime.utcnow()
        )
        db.session.add(nuevo_historial)
        db.session.commit()

        flash('Equipo de media tensión agregado exitosamente', 'success')
        return redirect(url_for('equipos_media_tension.get_media_tension'))
    
    estantes = Estantes.query.all()
    return render_template('Mtension/add.html', estantes=estantes)

@bp.route('/equipos_media_tension/edit/<int:idmediatension>', methods=['GET', 'POST'])
@login_required
def edit_media_tension(idmediatension):
    media_tension = EquiposMediaTension.query.get_or_404(idmediatension)

    if request.method == 'POST':
        # Guardamos los datos antiguos para registrar cambios
        datos_anteriores = f"Unidad medida: {media_tension.unidad_medida}, Descripción: {media_tension.descripcion_producto}, Cantidad: {media_tension.cantidad}, Observación: {media_tension.observacion}, Estante ID: {media_tension.estante_id}"

        media_tension.unidad_medida = request.form['unidad_medida']
        media_tension.estante_id = request.form['estante_id']
        media_tension.descripcion_producto = request.form['descripcion_producto']
        media_tension.observacion = request.form['observacion']
        media_tension.cantidad = int(request.form['cantidad'])

        db.session.commit()

        # Registro en el historial
        nuevo_historial = Historial(
            usuario_id=current_user.id,
            tabla="EquiposMediaTension",
            accion=f"Editó equipo de media tensión (antes: {datos_anteriores}, después: Unidad medida: {media_tension.unidad_medida}, Descripción: {media_tension.descripcion_producto}, Cantidad: {media_tension.cantidad}, Observación: {media_tension.observacion}, Estante ID: {media_tension.estante_id})",
            fecha=datetime.utcnow()
        )
        db.session.add(nuevo_historial)
        db.session.commit()

        flash('Equipo de media tensión actualizado exitosamente', 'success')
        return redirect(url_for('equipos_media_tension.get_media_tension'))
    
    estantes = Estantes.query.all()
    return render_template('Mtension/edit.html', media_tension=media_tension, estantes=estantes)

@bp.route('/equipos_media_tension/delete/<int:idmediatension>', methods=['POST'])
@login_required
def delete_media_tension(idmediatension):
    equipobt = EquiposMediaTension.query.get_or_404(idmediatension)

    # Guardamos los detalles del equipo eliminado para el historial
    detalles = f"Unidad medida: {equipobt.unidad_medida}, Descripción: {equipobt.descripcion_producto}, Cantidad: {equipobt.cantidad}, Observación: {equipobt.observacion}, Estante ID: {equipobt.estante_id}"

    db.session.delete(equipobt)
    db.session.commit()

    # Registro en el historial
    nuevo_historial = Historial(
        usuario_id=current_user.id,
        tabla="EquiposMediaTension",
        accion=f"Eliminó equipo de media tensión: {detalles}",
        fecha=datetime.utcnow()
    )
    db.session.add(nuevo_historial)
    db.session.commit()

    flash('Equipo de media tensión eliminado exitosamente', 'success')
    return redirect(url_for('equipos_media_tension.get_media_tension'))
