from flask import Blueprint, request, render_template, redirect, url_for, flash
from flask_login import login_required
from ..models.equipos_altura import EquiposAltura
from ..models.estante import Estantes
from .. import db

bp = Blueprint('equipos_altura', __name__)

@bp.route('/equipos_altura', methods=['GET'])
@login_required
def get_equipos_altura():
    data = EquiposAltura.query.all()
    return render_template('alturas/index.html', data=data)

@bp.route('/equipos_altura/add', methods=['GET', 'POST'])
@login_required
def add_equipos_altura():
    if request.method == 'POST':
        nombre = request.form['nombre']
        descripcion_producto = request.form['descripcion_producto']
        estante_id = request.form['estante_id']

        # Verificar si el estante_id existe
        estante = Estantes.query.get(estante_id)
        if estante is None:
            flash('El estante con el ID proporcionado no existe.', 'error')
            return redirect(url_for('equipos_altura.add_equipos_altura'))

        new_equipo = EquiposAltura(nombre=nombre, descripcion_producto=descripcion_producto, estante_id=estante_id)
        db.session.add(new_equipo)
        db.session.commit()
        flash('Equipo de altura agregado exitosamente', 'success')
        return redirect(url_for('equipos_altura.get_equipos_altura'))
    estantes = Estantes.query.all()
    
    return render_template('alturas/add.html', estantes=estantes)

@bp.route('/equipos_altura/edit/<int:idequiposaltura>', methods=['GET', 'POST'])
@login_required
def edit_equipos_altura(idequiposaltura):
    equipos_altura = EquiposAltura.query.get_or_404(idequiposaltura)

    if request.method == 'POST':
        equipos_altura.nombre = request.form['nombre']
        equipos_altura.descripcion_producto = request.form['descripcion_producto']
        equipos_altura.estante_id = request.form['estante_id']

        db.session.commit()
        flash('Equipo de altura actualizado exitosamente', 'success')
        return redirect(url_for('equipos_altura.get_equipos_altura'))
    
    estantes = Estantes.query.all()

    return render_template('alturas/edit.html', equipos_altura=equipos_altura, estantes=estantes)

@bp.route('/equipos_altura/delete/<int:idequiposaltura>', methods=['POST'])
@login_required
def delete_equipos_altura(idequiposaltura):
    equipos_altura = EquiposAltura.query.get_or_404(idequiposaltura)
    db.session.delete(equipos_altura)
    db.session.commit()
    flash('Equipo de altura eliminado exitosamente', 'success')
    return redirect(url_for('equipos_altura.get_equipos_altura'))
