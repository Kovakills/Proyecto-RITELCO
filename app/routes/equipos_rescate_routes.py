from flask import Blueprint, request, render_template, redirect, url_for, flash
from flask_login import login_required
from ..models.equipos_rescate import EquiposRescate
from ..models.estante import Estantes
from .. import db

bp = Blueprint('equipos_rescate', __name__)

@bp.route('/equipos_rescate', methods=['GET'])
@login_required
def get_equipos_rescate():
    data = EquiposRescate.query.all()
    return render_template('rescate/index.html', data=data)

@bp.route('/equipos_rescate/add', methods=['GET', 'POST'])
@login_required
def add_equipos_rescate():
    if request.method == 'POST':
        nombre = request.form['nombre']
        descripcion_producto = request.form['descripcion_producto']
        estante_id = request.form['estante_id']

        # Verificar si el estante_id existe
        estante = Estantes.query.get(estante_id)
        if estante is None:
            flash('El estante con el ID proporcionado no existe.', 'error')
            return redirect(url_for('equipos_rescate.add_equipos_rescate'))

        new_equipo = EquiposRescate(nombre=nombre, descripcion_producto=descripcion_producto, estante_id=estante_id)
        db.session.add(new_equipo)
        db.session.commit()
        flash('Equipo de rescate agregado exitosamente', 'success')
        return redirect(url_for('equipos_rescate.get_equipos_rescate'))
    estantes = Estantes.query.all()
    
    return render_template('rescate/add.html', estantes=estantes)

@bp.route('/equipos_rescate/edit/<int:idequiposrescate>', methods=['GET', 'POST'])
@login_required
def edit_equipos_rescate(idequiposrescate):
    equipos_rescate = EquiposRescate.query.get_or_404(idequiposrescate)

    if request.method == 'POST':
        equipos_rescate.nombre = request.form['nombre']
        equipos_rescate.descripcion_producto = request.form['descripcion_producto']
        equipos_rescate.estante_id = request.form['estante_id']

        db.session.commit()
        flash('Equipo de rescate actualizado exitosamente', 'success')
        return redirect(url_for('equipos_rescate.get_equipos_rescate'))
    
    estantes = Estantes.query.all()

    return render_template('rescates/edit.html', equipos_rescate=equipos_rescate, estantes=estantes)

@bp.route('/equipos_rescate/delete/<int:idequiposrescate>', methods=['POST'])
@login_required
def delete_equipos_rescate(idequiposrescate):
    equipos_rescate = EquiposRescate.query.get_or_404(idequiposrescate)
    db.session.delete(equipos_rescate)
    db.session.commit()
    flash('Equipo de rescate eliminado exitosamente', 'success')
    return redirect(url_for('equipos_rescate.get_equipos_rescate'))
