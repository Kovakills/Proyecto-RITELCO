from flask import Blueprint, request, render_template, redirect, url_for, flash
from flask_login import login_required
from ..models.herramientas_inalambricas import HerramientasInalambricas
from ..models.estante import Estantes
from .. import db

bp = Blueprint('herramientas_inalambricas', __name__)

@bp.route('/herramientas_inalambricas', methods=['GET'])
@login_required
def get_herramientas_inalambricas():
    data = HerramientasInalambricas.query.all()
    return render_template('inalambricas/index.html', data=data)

@bp.route('/herramientas_inalambricas/add', methods=['GET', 'POST'])
@login_required
def add_herramientas_inalambricas():
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
            return redirect(url_for('herramientas_inalambricas.add_herramientas_inalambricas'))

        new_equipo = HerramientasInalambricas(nombre=nombre, descripcion_producto=descripcion_producto, marca=marca, modelo=modelo, fecha_adquisicion=fecha_adquisicion, observacion=observacion, estante_id=estante_id)
        db.session.add(new_equipo)
        db.session.commit()
        flash('Herramienta inalambrica añadida exitosamente', 'success')
        return redirect(url_for('herramientas_inalambricas.get_herramientas_inalambricas'))
    estantes = Estantes.query.all()
    
    return render_template('inalambricas/add.html', estantes=estantes)

@bp.route('/herramientas_inalambricas/edit/<int:idherramientasinalambricas>', methods=['GET', 'POST'])
@login_required
def edit_herramientas_inalambricas(idherramientasinalambricas):
    herramientas_inalambricas = HerramientasInalambricas.query.get_or_404(idherramientasinalambricas)

    if request.method == 'POST':
        herramientas_inalambricas.nombre = request.form['nombre']
        herramientas_inalambricas.descripcion_producto = request.form['descripcion_producto']
        herramientas_inalambricas.estante_id = request.form['estante_id']
        herramientas_inalambricas.marca = request.form['marca']    
        herramientas_inalambricas.modelo = request.form['modelo']
        herramientas_inalambricas.observacion = request.form['observacion']
        herramientas_inalambricas.fecha_adquisicion = request.form['fecha_adquisicion']

        db.session.commit()
        flash('Herramienta inalambrica actualizada exitosamente', 'success')
        return redirect(url_for('herramientas_inalambricas.get_herramientas_inalambricas'))
    
    estantes = Estantes.query.all()

    return render_template('inalambricas/edit.html', herramientas_inalambricas=herramientas_inalambricas, estantes=estantes)

@bp.route('/herramientas_inalambricas/delete/<int:idherramientasinalambricas>', methods=['POST'])
@login_required
def delete_herramientas_inalambricas(idherramientasinalambricas):
    herramientas_inalambricas = HerramientasInalambricas.query.get_or_404(idherramientasinalambricas)
    db.session.delete(herramientas_inalambricas)
    db.session.commit()
    flash('Herramienta inalambrica eliminada exitosamente', 'success')
    return redirect(url_for('herramientas_inalambricas.get_herramientas_inalambricas'))
