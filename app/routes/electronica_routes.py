from flask import Blueprint, request, render_template, redirect, url_for, flash
from flask_login import login_required
from ..models.electronica import Electronica
from ..models.estante import Estantes
from .. import db

bp = Blueprint('electronica', __name__)

@bp.route('/electronica', methods=['GET'])
@login_required
def get_electronica():
    data = Electronica.query.all()
    return render_template('electro/index.html', data=data)

@bp.route('/electronica/add', methods=['GET', 'POST'])
@login_required
def add_electronica():
    if request.method == 'POST':
        nombre = request.form['nombre']
        descripcion_producto = request.form['descripcion_producto']
        cantidad = int(request.form['cantidad'])
        estante_id = request.form['estante_id']

        # Verificar si el estante_id existe
        estante = Estantes.query.get(estante_id)
        if estante is None:
            flash('El estante con el ID proporcionado no existe.', 'error')
            return redirect(url_for('electronica.add_electronica'))

        new_electronica = Electronica(nombre=nombre, descripcion_producto=descripcion_producto, estante_id=estante_id)
        db.session.add(new_electronica)
        db.session.commit()
        flash('Electronica agregado exitosamente', 'success')
        return redirect(url_for('electronica.get_electronica'))
    estantes = Estantes.query.all()
    
    return render_template('electro/add.html', estantes=estantes)

@bp.route('/electronica/edit/<int:idelectronica>', methods=['GET', 'POST'])
@login_required
def edit_electronica(idelectronica):
    electronica = Electronica.query.get_or_404(idelectronica)

    if request.method == 'POST':
        electronica.nombre = request.form['nombre']
        electronica.descripcion_producto = request.form['descripcion_producto']
        electronica.estante_id = request.form['estante_id']
        electronica.cantidad = int(request.form['cantidad'])

        db.session.commit()
        flash('Electronica actualizado exitosamente', 'success')
        return redirect(url_for('electronica.get_electronica'))
    
    estantes = Estantes.query.all()

    return render_template('electro/edit.html', electronica=electronica, estantes=estantes)

@bp.route('/electronica/delete/<int:idelectronica>', methods=['POST'])
@login_required
def delete_electronica(idelectronica):
    electronica = Electronica.query.get_or_404(idelectronica)
    db.session.delete(electronica)
    db.session.commit()
    flash('Electronica eliminiado exitosamente', 'success')
    return redirect(url_for('electronica.get_electronica'))
