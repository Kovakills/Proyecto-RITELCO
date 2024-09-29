from flask import Blueprint, request, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from ..models.respels import Respels
from ..models.estante import Estantes
from ..models.historial import Historial
from .. import db
from datetime import datetime

bp = Blueprint('respel', __name__)

@bp.route('/respel', methods=['GET'])
@login_required
def get_respel():
    data = Respels.query.all()
    return render_template('respel/index.html', data=data)

@bp.route('/respel/add', methods=['GET', 'POST'])
@login_required
def add_respel():
    if request.method == 'POST':
        nombre = request.form['nombre']
        descripcion_producto = request.form['descripcion_producto']
        estante_id = request.form['estante_id']
        cantidad = request.form['cantidad']
        observacion = request.form['observacion']

        
        estante = Estantes.query.get(estante_id)
        if estante is None:
            flash('El estante con el ID proporcionado no existe.', 'error')
            return redirect(url_for('respel.add_respel'))

        new_respel = Respels(
            nombre=nombre,
            descripcion_producto=descripcion_producto,
            observacion=observacion,
            cantidad=cantidad,
            estante_id=estante_id
        )
        db.session.add(new_respel)
        db.session.commit()

    
        nuevo_historial = Historial(
            usuario_id=current_user.id,
            tabla="Respels",
            accion=f"Agregó refrigerante: Nombre: {nombre}, Descripción: {descripcion_producto}, Cantidad: {cantidad}, Estante ID: {estante_id}, Observación: {observacion}",
            fecha=datetime.utcnow()
        )
        db.session.add(nuevo_historial)
        db.session.commit()

        flash('Refrigerante añadido exitosamente', 'success')   
        return redirect(url_for('respel.get_respel'))
    
    estantes = Estantes.query.all()
    return render_template('respel/add.html', estantes=estantes)


@bp.route('/respel/edit/<int:idrespel>', methods=['GET', 'POST'])
@login_required
def edit_respel(idrespel):
    respel = Respels.query.get_or_404(idrespel)

    if request.method == 'POST':
        datos_anteriores = f"Nombre: {respel.nombre}, Descripción: {respel.descripcion_producto}, Cantidad: {respel.cantidad}, Estante ID: {respel.estante_id}, Observación: {respel.observacion}"

        respel.nombre = request.form['nombre']
        respel.descripcion_producto = request.form['descripcion_producto']
        respel.estante_id = request.form['estante_id']
        respel.cantidad = request.form['cantidad']
        respel.observacion = request.form['observacion']

        try:
            db.session.commit()
        
            nuevo_historial = Historial(
                usuario_id=current_user.id,
                tabla="Respels",
                accion=f"Editó refrigerante (antes: {datos_anteriores}, después: Nombre: {respel.nombre}, Descripción: {respel.descripcion_producto}, Cantidad: {respel.cantidad}, Estante ID: {respel.estante_id}, Observación: {respel.observacion})",
                fecha=datetime.utcnow()
            )
            db.session.add(nuevo_historial)
            db.session.commit()

            flash('Refrigerante actualizado correctamente', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Error al actualizar el respel: {str(e)}', 'error')
            return render_template('respel/edit.html', respel=respel, estantes=Estantes.query.all())

        return redirect(url_for('respel.get_respel'))

    estantes = Estantes.query.all()
    return render_template('respel/edit.html', respel=respel, estantes=estantes)


@bp.route('/respel/delete/<int:idrespel>', methods=['POST'])
@login_required
def delete_respel(idrespel):
    respel = Respels.query.get_or_404(idrespel)

    detalles = f"Nombre: {respel.nombre}, Descripción: {respel.descripcion_producto}, Cantidad: {respel.cantidad}, Estante ID: {respel.estante_id}, Observación: {respel.observacion}"

    db.session.delete(respel)
    db.session.commit()


    nuevo_historial = Historial(
        usuario_id=current_user.id,
        tabla="Respels",
        accion=f"Eliminó refrigerante: {detalles}",
        fecha=datetime.utcnow()
    )
    db.session.add(nuevo_historial)
    db.session.commit()

    flash('Refrigerante eliminado exitosamente', 'success')
    return redirect(url_for('respel.get_respel'))
