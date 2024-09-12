from flask import Blueprint, request, render_template, redirect, url_for, flash
from flask_login import login_required
from ..models.filtros import Filtros
from ..models.estante import Estantes
from .. import db

bp = Blueprint('filtros', __name__)

@bp.route('/filtros', methods=['GET'])
@login_required
def get_filtros():
    filtros = Filtros.query.all()
    return render_template('filtros/index.html', filtros=filtros)

@bp.route('/filtros/add', methods=['GET', 'POST'])
@login_required
def add_filtros():
    if request.method == 'POST':
        marca = request.form['marca']
        tipo_de_filtro = request.form['tipo_de_filtro']
        estante_id = request.form['estante_id']
        referencia = request.form['referencia']
        cantidad = int(request.form['cantidad'])
        observacion = request.form['observacion']  # Asegúrate de que este nombre coincida

        estante = Estantes.query.get(estante_id)
        if estante is None:
            flash('El estante con el ID proporcionado no existe.', 'error')
            return redirect(url_for('filtros.add_filtros'))
                                      
        new_filtro = Filtros(marca=marca, referencia=referencia, tipo_de_filtro=tipo_de_filtro, observacion=observacion, estante_id=estante_id, cantidad=cantidad)
        db.session.add(new_filtro)
        db.session.commit()
        flash('Filtro agregado exitosamente','success')
        return redirect(url_for('filtros.get_filtros'))
    
    estantes = Estantes.query.all()
    
    return render_template('filtros/add.html', estantes=estantes)

@bp.route('/filtros/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_filtros(id):
    filtros = Filtros.query.get_or_404(id)

    if request.method == 'POST':
        filtros.marca = request.form['marca']
        filtros.tipo_de_filtro = request.form['tipo_de_filtro']
        filtros.estante_id = request.form['estante_id']
        filtros.referencia = request.form['referencia']
        filtros.cantidad = int(request.form['cantidad'])
        filtros.observacion = request.form['observacion']  # Asegúrate de que este nombre coincida

        try:
            db.session.commit()
            flash('Filtro actualizado correctamente', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Error al actualizar el filtro: {str(e)}', 'error')
            return render_template('filtros/edit.html', filtros=filtros, estantes=Estantes.query.all())

        return redirect(url_for('filtros.get_filtros'))

    estantes = Estantes.query.all()
    return render_template('filtros/edit.html', filtros=filtros, estantes=estantes)

@bp.route('/filtros/delete/<int:id>', methods=['POST'])
@login_required
def delete_filtros(id):
    filtros = Filtros.query.get_or_404(id)
    db.session.delete(filtros)
    db.session.commit()
    flash('Filtro eliminado exitosamente', 'success')
    return redirect(url_for('filtros.get_filtros'))
