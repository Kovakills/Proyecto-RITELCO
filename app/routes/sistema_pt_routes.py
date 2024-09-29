from flask import Blueprint, request, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from ..models.sistema_pt import SistemaPT
from ..models.estante import Estantes
from ..models.historial import Historial
from .. import db
from datetime import datetime

bp = Blueprint('sistema_pt', __name__)

# Ruta para obtener todos los sistemas de puesta a tierra
@bp.route('/sistema_pt', methods=['GET'])
@login_required
def get_sistema_pt(): 
    data = SistemaPT.query.all()
    return render_template('pt/index.html', data=data)

# Ruta para agregar un nuevo sistema de puesta a tierra
@bp.route('/sistema_pt/add', methods=['GET', 'POST'])
@login_required
def add_sistema_pt():
    if request.method == 'POST':
        unidad_medida = request.form['unidad_medida']
        descripcion_producto = request.form['descripcion_producto']
        cantidad = int(request.form['cantidad'])
        observacion = request.form['observacion']
        estante_id = request.form['estante_id']

        estante = Estantes.query.get(estante_id)
        if estante is None:
            flash('El estante con el ID proporcionado no existe.', 'error')
            return redirect(url_for('sistema_pt.add_sistema_pt'))

        new_equipobt = SistemaPT(
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
            tabla="SistemaPT",
            accion=f"Agregó sistema de puesta a tierra: Unidad de medida: {unidad_medida}, Descripción: {descripcion_producto}, Cantidad: {cantidad}, Estante ID: {estante_id}, Observación: {observacion}",
            fecha=datetime.utcnow()
        )
        db.session.add(nuevo_historial)
        db.session.commit()

        flash('Sistema puesta a tierra añadido exitosamente', 'success')
        return redirect(url_for('sistema_pt.get_sistema_pt'))
    
    estantes = Estantes.query.all()
    return render_template('pt/add.html', estantes=estantes)

# Ruta para editar un sistema de puesta a tierra
@bp.route('/sistema_pt/edit/<int:idsistemapt>', methods=['GET', 'POST'])
@login_required
def edit_sistema_pt(idsistemapt):
    sistema_pt = SistemaPT.query.get_or_404(idsistemapt)

    if request.method == 'POST':
        # Guardamos los datos antiguos para registrar cambios
        datos_anteriores = f"Unidad de medida: {sistema_pt.unidad_medida}, Descripción: {sistema_pt.descripcion_producto}, Cantidad: {sistema_pt.cantidad}, Estante ID: {sistema_pt.estante_id}, Observación: {sistema_pt.observacion}"

        sistema_pt.unidad_medida = request.form['unidad_medida']
        sistema_pt.estante_id = request.form['estante_id']
        sistema_pt.descripcion_producto = request.form['descripcion_producto']
        sistema_pt.observacion = request.form['observacion']
        sistema_pt.cantidad = int(request.form['cantidad'])
        
        db.session.commit()
        
        # Registro en el historial
        nuevo_historial = Historial(
            usuario_id=current_user.id,
            tabla="SistemaPT",
            accion=f"Editó sistema de puesta a tierra (antes: {datos_anteriores}, después: Unidad de medida: {sistema_pt.unidad_medida}, Descripción: {sistema_pt.descripcion_producto}, Cantidad: {sistema_pt.cantidad}, Estante ID: {sistema_pt.estante_id}, Observación: {sistema_pt.observacion})",
            fecha=datetime.utcnow()
        )
        db.session.add(nuevo_historial)
        db.session.commit()

        flash('Sistema puesta a tierra actualizado exitosamente', 'success')
        return redirect(url_for('sistema_pt.get_sistema_pt'))

    estantes = Estantes.query.all()
    return render_template('pt/edit.html', sistema_pt=sistema_pt, estantes=estantes)

# Ruta para eliminar un sistema de puesta a tierra
@bp.route('/sistema_pt/delete/<int:idsistemapt>', methods=['POST'])
@login_required
def delete_sistema_pt(idsistemapt):
    equipobt = SistemaPT.query.get_or_404(idsistemapt)

    # Guardamos los detalles del sistema de puesta a tierra eliminado para el historial
    detalles = f"Unidad de medida: {equipobt.unidad_medida}, Descripción: {equipobt.descripcion_producto}, Cantidad: {equipobt.cantidad}, Estante ID: {equipobt.estante_id}, Observación: {equipobt.observacion}"

    db.session.delete(equipobt)
    db.session.commit()

    # Registro en el historial
    nuevo_historial = Historial(
        usuario_id=current_user.id,
        tabla="SistemaPT",
        accion=f"Eliminó sistema de puesta a tierra: {detalles}",
        fecha=datetime.utcnow()
    )
    db.session.add(nuevo_historial)
    db.session.commit()

    flash('Sistema puesta a tierra eliminado exitosamente', 'success')
    return redirect(url_for('sistema_pt.get_sistema_pt'))
