from flask import Blueprint, request, render_template, redirect, url_for, flash
from flask_login import login_required
from ..models.equipos_altura import EquiposAltura
from ..models.estante import Estantes
from .. import db

bp = Blueprint('equipos_alturas', __name__)

# Ruta para obtener todos los equipos de alturas
@bp.route('/equipos_alturas', methods=['GET'])
@login_required
def get_equipos_alturas():
    data = EquiposAltura.query.all()
    return render_template('alturas/index.html', data=data)

# Ruta para agregar un nuevo equipo de alturas
@bp.route('/equipos_alturas/add', methods=['GET', 'POST'])
@login_required
def add_equipos_alturas():
    if request.method == 'POST':
        arnes = request.form['arnes']
        eslingas = request.form['eslingas']
        posicionamiento = request.form['posicionamiento']
        caida_en_y = request.form['caida_en_y']
        conectores = request.form['conectores']
        cantidad = request.form['cantidad']
        estante_id = request.form['estante_id']

        # Verificar si el estante_id existe
        estante = Estantes.query.get(estante_id)
        if estante is None:
            flash('El estante con el ID proporcionado no existe.', 'error')
            return redirect(url_for('equipos_alturas.add_equipos_alturas'))

        new_equipo = EquiposAltura(
            arnes=arnes,
            eslingas=eslingas,
            posicionamiento=posicionamiento,
            caida_en_y=caida_en_y,
            conectores=conectores,
            cantidad=cantidad,
            estante_id=estante_id
        )
        db.session.add(new_equipo)
        db.session.commit()
        flash('Equipo de alturas agregado exitosamente', 'success')
        return redirect(url_for('equipos_alturas.get_equipos_alturas'))
    
    estantes = Estantes.query.all()
    return render_template('alturas/add.html', estantes=estantes)

# Ruta para editar un equipo de altura
@bp.route('/equipos_alturas/edit/<int:idequiposaltura>', methods=['GET', 'POST'])
@login_required
def edit_equipos_alturas(idequiposaltura):
    equipos_alturas = EquiposAltura.query.get_or_404(idequiposaltura)

    if request.method == 'POST':
        equipos_alturas.arnes = request.form['arnes']
        equipos_alturas.eslingas = request.form['eslingas']
        equipos_alturas.posicionamiento = request.form['posicionamiento']
        equipos_alturas.caida_en_y = request.form['caida_en_y']
        equipos_alturas.conectores = request.form['conectores']
        equipos_alturas.cantidad = request.form['cantidad']
        equipos_alturas.estante_id = request.form['estante_id']

        db.session.commit()
        flash('Equipo de altuequipos_altura actualizado exitosamente', 'success')
        return redirect(url_for('equipos_alturas.get_equipos_alturas'))
    
    estantes = Estantes.query.all()

    return render_template('alturas/edit.html', equipos_alturas=equipos_alturas, estantes=estantes)

# Ruta para eliminar un equipo de altura
@bp.route('/equipos_alturas/delete/<int:idequiposaltura>', methods=['POST'])
@login_required
def delete_equipos_alturas(idequiposaltura):
    equipos_alturas = EquiposAltura.query.get_or_404(idequiposaltura)
    db.session.delete(equipos_alturas)
    db.session.commit()
    flash('Equipo de altura eliminado exitosamente', 'success')
    return redirect(url_for('equipos_alturas.get_equipos_alturas'))
