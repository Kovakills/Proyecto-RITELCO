from flask import Blueprint, request, render_template, redirect, url_for, flash
from flask_login import login_required
from ..models.herramientas_electricas import HerramientasElectricas
from ..models.estante import Estantes
from .. import db

bp = Blueprint('herramientas_electricas', __name__)

@bp.route('/herramientas_electricas', methods=['GET'])
@login_required
def get_herramientas_electricas():
    data = HerramientasElectricas.query.all()
    return render_template('electricas/index.html', data=data)

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
            return redirect(url_for('herramientas_electricas.add_herramientas_electricas'))

        new_equipo = HerramientasElectricas(nombre=nombre, descripcion_producto=descripcion_producto, marca=marca, modelo=modelo, fecha_adquisicion=fecha_adquisicion, observacion=observacion, estante_id=estante_id)
        db.session.add(new_equipo)
        db.session.commit()
        flash('Herramienta electrica añadida exitosamente', 'success')
        return redirect(url_for('herramientas_electricas.get_herramientas_electricas'))
    estantes = Estantes.query.all()
    
    return render_template('electricas/add.html', estantes=estantes)

@bp.route('/herramientas_electricas/edit/<int:idherramientaselectricas>', methods=['GET', 'POST'])
@login_required
def edit_herramientas_electricas(idherramientaselectricas):
    herramientas_electricas = HerramientasElectricas.query.get_or_404(idherramientaselectricas)

    if request.method == 'POST':
        herramientas_electricas.nombre = request.form['nombre']
        herramientas_electricas.descripcion_producto = request.form['descripcion_producto']
        herramientas_electricas.estante_id = request.form['estante_id']
        herramientas_electricas.marca = request.form['marca']    
        herramientas_electricas.modelo = request.form['modelo']
        herramientas_electricas.observacion = request.form['observacion']
        herramientas_electricas.fecha_adquisicion = request.form['fecha_adquisicion']

        db.session.commit()
        flash('Herramienta electrica actualizada exitosamente', 'success')
        return redirect(url_for('herramientas_electricas.get_herramientas_electricas'))
    
    estantes = Estantes.query.all()

    return render_template('electricas/edit.html', herramientas_electricas=herramientas_electricas, estantes=estantes)

@bp.route('/herramientas_electricas/delete/<int:idherramientaselectricas>', methods=['POST'])
@login_required
def delete_herramientas_electricas(idherramientaselectricas):
    herramientas_electricas = HerramientasElectricas.query.get_or_404(idherramientaselectricas)
    db.session.delete(herramientas_electricas)
    db.session.commit()
    flash('Herramienta electrica eliminada exitosamente', 'success')
    return redirect(url_for('herramientas_electricas.get_herramientas_electricas'))
