from flask import Blueprint, request, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from ..models.aceites import Aceites
from ..models.estante import Estantes
from ..models.historial import Historial  # Asegúrate de que el modelo Historial esté definido
from .. import db
from datetime import datetime

bp = Blueprint('aceites', __name__)

@bp.route('/aceites', methods=['GET'])
@login_required
def get_aceites():
    aceites = Aceites.query.all()
    return render_template('aceites/index.html', aceites=aceites)

@bp.route('/aceites/add', methods=['GET', 'POST'])
@login_required
def add_aceites():
    if request.method == 'POST':
        nombre = request.form['nombre']
        tipo_de_aceite = request.form['tipo_de_aceite']
        cantidad = int(request.form['cantidad'])
        estante_id = request.form['estante_id']

        # Verificar si el estante_id existe
        estante = Estantes.query.get(estante_id)
        if estante is None:
            flash('El estante con el ID proporcionado no existe.', 'error')
            return redirect(url_for('aceites.add_aceites'))

        new_aceite = Aceites(nombre=nombre, tipo_de_aceite=tipo_de_aceite, cantidad=cantidad, estante_id=estante_id)
        db.session.add(new_aceite)
        db.session.commit()

        # Registrar en el historial
        nuevo_historial = Historial(
            usuario_id=current_user.id,
            tabla="Aceites",
            accion=f"Agregó aceite '{nombre}'",
            fecha=datetime.utcnow()
        )
        db.session.add(nuevo_historial)
        db.session.commit()

        flash('Aceite agregado exitosamente', 'success')
        return redirect(url_for('aceites.get_aceites'))

    estantes = Estantes.query.all()
    return render_template('aceites/add.html', estantes=estantes)

@bp.route('/aceites/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_aceites(id):
    aceite = Aceites.query.get_or_404(id)

    if request.method == 'POST':
        aceite.nombre = request.form['nombre']
        aceite.tipo_de_aceite = request.form['tipo_de_aceite']
        aceite.estante_id = request.form['estante_id']
        aceite.cantidad = request.form['cantidad']

        db.session.commit()

        # Registrar en el historial
        nuevo_historial = Historial(
            usuario_id=current_user.id,
            tabla="Aceites",
            accion=f"Editó aceite '{aceite.nombre}'",
            fecha=datetime.utcnow()
        )
        db.session.add(nuevo_historial)
        db.session.commit()

        flash('Aceite actualizado exitosamente', 'success')
        return redirect(url_for('aceites.get_aceites'))

    estantes = Estantes.query.all()
    return render_template('aceites/edit.html', aceite=aceite, estantes=estantes)

@bp.route('/aceites/delete/<int:id>', methods=['POST'])
@login_required
def delete_aceites(id):
    aceite = Aceites.query.get_or_404(id)
    db.session.delete(aceite)
    db.session.commit()

    # Registrar en el historial
    nuevo_historial = Historial(
        usuario_id=current_user.id,
        tabla="Aceites",
        accion=f"Eliminó aceite '{aceite.nombre}'",
        fecha=datetime.utcnow()
    )
    db.session.add(nuevo_historial)
    db.session.commit()

    flash('Aceite eliminado exitosamente', 'success')
    return redirect(url_for('aceites.get_aceites'))
