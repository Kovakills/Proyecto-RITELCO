from flask import Blueprint, request, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from ..models.baja_tension import BajaTension
from ..models.estante import Estantes
from ..models.historial import Historial
from .. import db
from datetime import datetime

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

        new_equipobt = BajaTension(
            unidad_medida=unidad_medida,
            descripcion_producto=descripcion_producto,
            cantidad=cantidad,
            observacion=observacion,
            estante_id=estante_id
        )
        db.session.add(new_equipobt)
        db.session.commit()

        nuevo_historial = Historial(
            usuario_id=current_user.id,
            tabla="BajaTension",
            accion=f"Agregó equipo: {descripcion_producto}, Cantidad: {cantidad}, Unidad: {unidad_medida}, Observación: {observacion}, Estante ID: {estante_id}",
            fecha=datetime.utcnow()
        )
        db.session.add(nuevo_historial)
        db.session.commit()

        flash('Equipo de baja tensión agregado exitosamente', 'success')
        return redirect(url_for('baja_tension.get_baja_tension'))

    estantes = Estantes.query.all()
    return render_template('Btension/add.html', estantes=estantes)


@bp.route('/Btension/edit/<int:idbajatension>', methods=['GET', 'POST'])
@login_required
def edit_bajatension(idbajatension):
    baja_tension = BajaTension.query.get_or_404(idbajatension)

    if request.method == 'POST':
        unidad_medida = request.form['unidad_medida']
        descripcion_producto = request.form['descripcion_producto']
        cantidad = int(request.form['cantidad'])
        observacion = request.form['observacion']
        estante_id = request.form['estante_id']


        datos_anteriores = f"Equipo: {baja_tension.descripcion_producto}, Cantidad: {baja_tension.cantidad}, Unidad: {baja_tension.unidad_medida}, Observación: {baja_tension.observacion}, Estante ID: {baja_tension.estante_id}"

        baja_tension.unidad_medida = unidad_medida
        baja_tension.descripcion_producto = descripcion_producto
        baja_tension.cantidad = cantidad
        baja_tension.observacion = observacion
        baja_tension.estante_id = estante_id

        db.session.commit()

        nuevo_historial = Historial(
            usuario_id=current_user.id,
            tabla="BajaTension",
            accion=f"Editó equipo (antes: {datos_anteriores}, después: Equipo: {descripcion_producto}, Cantidad: {cantidad}, Unidad: {unidad_medida}, Observación: {observacion}, Estante ID: {estante_id})",
            fecha=datetime.utcnow()
        )
        db.session.add(nuevo_historial)
        db.session.commit()

        flash('Equipo de baja tensión actualizado exitosamente', 'success')
        return redirect(url_for('baja_tension.get_baja_tension'))

    estantes = Estantes.query.all()
    return render_template('Btension/edit.html', baja_tension=baja_tension, estantes=estantes)


@bp.route('/Btension/delete/<int:idbajatension>', methods=['POST'])
@login_required
def delete_baja_tension(idbajatension):
    equipobt = BajaTension.query.get_or_404(idbajatension)

    detalles = f"Equipo: {equipobt.descripcion_producto}, Cantidad: {equipobt.cantidad}, Unidad: {equipobt.unidad_medida}, Observación: {equipobt.observacion}, Estante ID: {equipobt.estante_id}"

    db.session.delete(equipobt)
    db.session.commit()

    nuevo_historial = Historial(
        usuario_id=current_user.id,
        tabla="BajaTension",
        accion=f"Eliminó equipo: {detalles}",
        fecha=datetime.utcnow()
    )
    db.session.add(nuevo_historial)
    db.session.commit()

    flash('Equipo eliminado exitosamente', 'success')
    return redirect(url_for('baja_tension.get_baja_tension'))
