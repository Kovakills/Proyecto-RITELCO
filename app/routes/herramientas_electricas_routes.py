from flask import Blueprint, request, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from ..models.herramientas_electricas import HerramientasElectricas
from ..models.estante import Estantes
from ..models.historial import Historial
from .. import db
from datetime import datetime

bp = Blueprint('herramientas_electricas', __name__)

# Ruta para obtener todas las herramientas eléctricas
@bp.route('/herramientas_electricas', methods=['GET'])
@login_required
def get_herramientas_electricas():
    data = HerramientasElectricas.query.all()
    return render_template('electricas/index.html', data=data)

# Ruta para agregar una nueva herramienta eléctrica
@bp.route('/herramientas_electricas/add', methods=['GET', 'POST'])
@login_required
def add_herramientas_electricas():
    if request.method == 'POST':
        nombre = request.form['nombre']
        marca = request.form['marca']
        modelo = request.form['modelo']
        fecha_adquisicion = request.form['fecha_adquisicion']
        descripcion_producto = request.form['descripcion_producto']
        observacion = request.form['observacion']
        estante_id = request.form['estante_id']

        # Verificar si el estante_id existe
        estante = Estantes.query.get(estante_id)
        if estante is None:
            flash('El estante con el ID proporcionado no existe.', 'error')
            return redirect(url_for('herramientas_electricas.add_herramientas_electricas'))

        new_equipo = HerramientasElectricas(
            nombre=nombre,
            descripcion_producto=descripcion_producto,
            marca=marca,
            modelo=modelo,
            fecha_adquisicion=fecha_adquisicion,
            observacion=observacion,
            estante_id=estante_id
        )
        db.session.add(new_equipo)
        db.session.commit()

        # Registro en el historial
        nuevo_historial = Historial(
            usuario_id=current_user.id,
            tabla="HerramientasElectricas",
            accion=f"Agregó herramienta eléctrica: Nombre: {nombre}, Marca: {marca}, Modelo: {modelo}, Fecha de adquisición: {fecha_adquisicion}, Descripción: {descripcion_producto}, Observación: {observacion}, Estante ID: {estante_id}",
            fecha=datetime.utcnow()
        )
        db.session.add(nuevo_historial)
        db.session.commit()

        flash('Herramienta eléctrica añadida exitosamente', 'success')
        return redirect(url_for('herramientas_electricas.get_herramientas_electricas'))

    estantes = Estantes.query.all()
    return render_template('electricas/add.html', estantes=estantes)

# Ruta para editar una herramienta eléctrica
@bp.route('/herramientas_electricas/edit/<int:idherramientaselectricas>', methods=['GET', 'POST'])
@login_required
def edit_herramientas_electricas(idherramientaselectricas):
    herramientas_electricas = HerramientasElectricas.query.get_or_404(idherramientaselectricas)

    if request.method == 'POST':
        # Guardamos los datos antiguos para registrar cambios
        datos_anteriores = f"Nombre: {herramientas_electricas.nombre}, Marca: {herramientas_electricas.marca}, Modelo: {herramientas_electricas.modelo}, Fecha de adquisición: {herramientas_electricas.fecha_adquisicion}, Descripción: {herramientas_electricas.descripcion_producto}, Observación: {herramientas_electricas.observacion}, Estante ID: {herramientas_electricas.estante_id}"

        herramientas_electricas.nombre = request.form['nombre']
        herramientas_electricas.descripcion_producto = request.form['descripcion_producto']
        herramientas_electricas.estante_id = request.form['estante_id']
        herramientas_electricas.marca = request.form['marca']    
        herramientas_electricas.modelo = request.form['modelo']
        herramientas_electricas.observacion = request.form['observacion']
        herramientas_electricas.fecha_adquisicion = request.form['fecha_adquisicion']

        db.session.commit()

        # Registro en el historial
        nuevo_historial = Historial(
            usuario_id=current_user.id,
            tabla="HerramientasElectricas",
            accion=f"Editó herramienta eléctrica (antes: {datos_anteriores}, después: Nombre: {herramientas_electricas.nombre}, Marca: {herramientas_electricas.marca}, Modelo: {herramientas_electricas.modelo}, Fecha de adquisición: {herramientas_electricas.fecha_adquisicion}, Descripción: {herramientas_electricas.descripcion_producto}, Observación: {herramientas_electricas.observacion}, Estante ID: {herramientas_electricas.estante_id})",
            fecha=datetime.utcnow()
        )
        db.session.add(nuevo_historial)
        db.session.commit()

        flash('Herramienta eléctrica actualizada exitosamente', 'success')
        return redirect(url_for('herramientas_electricas.get_herramientas_electricas'))

    estantes = Estantes.query.all()
    return render_template('electricas/edit.html', herramientas_electricas=herramientas_electricas, estantes=estantes)

# Ruta para eliminar una herramienta eléctrica
@bp.route('/herramientas_electricas/delete/<int:idherramientaselectricas>', methods=['POST'])
@login_required
def delete_herramientas_electricas(idherramientaselectricas):
    herramientas_electricas = HerramientasElectricas.query.get_or_404(idherramientaselectricas)

    # Guardamos los detalles de la herramienta eliminada para el historial
    detalles = f"Nombre: {herramientas_electricas.nombre}, Marca: {herramientas_electricas.marca}, Modelo: {herramientas_electricas.modelo}, Fecha de adquisición: {herramientas_electricas.fecha_adquisicion}, Descripción: {herramientas_electricas.descripcion_producto}, Observación: {herramientas_electricas.observacion}, Estante ID: {herramientas_electricas.estante_id}"

    db.session.delete(herramientas_electricas)
    db.session.commit()

    # Registro en el historial
    nuevo_historial = Historial(
        usuario_id=current_user.id,
        tabla="HerramientasElectricas",
        accion=f"Eliminó herramienta eléctrica: {detalles}",
        fecha=datetime.utcnow()
    )
    db.session.add(nuevo_historial)
    db.session.commit()

    flash('Herramienta eléctrica eliminada exitosamente', 'success')
    return redirect(url_for('herramientas_electricas.get_herramientas_electricas'))
