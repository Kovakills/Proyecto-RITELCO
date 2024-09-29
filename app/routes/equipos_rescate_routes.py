from flask import Blueprint, request, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from ..models.equipos_rescate import EquiposRescate
from ..models.estante import Estantes
from ..models.historial import Historial
from .. import db
from datetime import datetime

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
        arnes = request.form['arnes']
        eslingas = request.form['eslingas']
        posicionamiento = request.form['posicionamiento']
        caida_en_y = request.form['caida_en_y']
        conectores = request.form['conectores']
        cantidad = request.form['cantidad']
        estante_id = request.form['estante_id']

        estante = Estantes.query.get(estante_id)
        if estante is None:
            flash('El estante con el ID proporcionado no existe.', 'error')
            return redirect(url_for('equipos_rescate.add_equipos_rescate'))

        new_equipo = EquiposRescate(
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


        nuevo_historial = Historial(
            usuario_id=current_user.id,
            tabla="EquiposRescate",
            accion=f"Agregó equipo de rescate: Arnes: {arnes}, Eslingas: {eslingas}, Posicionamiento: {posicionamiento}, Caída en Y: {caida_en_y}, Conectores: {conectores}, Cantidad: {cantidad}, Estante ID: {estante_id}",
            fecha=datetime.utcnow()
        )
        db.session.add(nuevo_historial)
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
        datos_anteriores = f"Arnes: {equipos_rescate.arnes}, Eslingas: {equipos_rescate.eslingas}, Posicionamiento: {equipos_rescate.posicionamiento}, Caída en Y: {equipos_rescate.caida_en_y}, Conectores: {equipos_rescate.conectores}, Cantidad: {equipos_rescate.cantidad}, Estante ID: {equipos_rescate.estante_id}"

        equipos_rescate.arnes = request.form['arnes']
        equipos_rescate.eslingas = request.form['eslingas']
        equipos_rescate.posicionamiento = request.form['posicionamiento']
        equipos_rescate.caida_en_y = request.form['caida_en_y']
        equipos_rescate.conectores = request.form['conectores']
        equipos_rescate.cantidad = request.form['cantidad']
        equipos_rescate.estante_id = request.form['estante_id']

        db.session.commit()


        nuevo_historial = Historial(
            usuario_id=current_user.id,
            tabla="EquiposRescate",
            accion=f"Editó equipo de rescate (antes: {datos_anteriores}, después: Arnes: {equipos_rescate.arnes}, Eslingas: {equipos_rescate.eslingas}, Posicionamiento: {equipos_rescate.posicionamiento}, Caída en Y: {equipos_rescate.caida_en_y}, Conectores: {equipos_rescate.conectores}, Cantidad: {equipos_rescate.cantidad}, Estante ID: {equipos_rescate.estante_id})",
            fecha=datetime.utcnow()
        )
        db.session.add(nuevo_historial)
        db.session.commit()

        flash('Equipo de rescate actualizado exitosamente', 'success')
        return redirect(url_for('equipos_rescate.get_equipos_rescate'))
    
    estantes = Estantes.query.all()
    return render_template('rescate/edit.html', equipos_rescate=equipos_rescate, estantes=estantes)

@bp.route('/equipos_rescate/delete/<int:idequiposrescate>', methods=['POST'])
@login_required
def delete_equipos_rescate(idequiposrescate):
    equipos_rescate = EquiposRescate.query.get_or_404(idequiposrescate)

    detalles = f"Arnes: {equipos_rescate.arnes}, Eslingas: {equipos_rescate.eslingas}, Posicionamiento: {equipos_rescate.posicionamiento}, Caída en Y: {equipos_rescate.caida_en_y}, Conectores: {equipos_rescate.conectores}, Cantidad: {equipos_rescate.cantidad}, Estante ID: {equipos_rescate.estante_id}"

    db.session.delete(equipos_rescate)
    db.session.commit()

    nuevo_historial = Historial(
        usuario_id=current_user.id,
        tabla="EquiposRescate",
        accion=f"Eliminó equipo de rescate: {detalles}",
        fecha=datetime.utcnow()
    )
    db.session.add(nuevo_historial)
    db.session.commit()

    flash('Equipo de rescate eliminado exitosamente', 'success')
    return redirect(url_for('equipos_rescate.get_equipos_rescate'))
