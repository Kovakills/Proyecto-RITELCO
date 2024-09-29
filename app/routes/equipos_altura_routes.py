from flask import Blueprint, request, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from ..models.equipos_altura import EquiposAltura
from ..models.estante import Estantes
from ..models.historial import Historial
from .. import db
from datetime import datetime

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

        # Registro en el historial con todos los detalles
        nuevo_historial = Historial(
            usuario_id=current_user.id,
            tabla="EquiposAltura",
            accion=f"Agregó equipo de altura: Arnes: {arnes}, Eslingas: {eslingas}, Posicionamiento: {posicionamiento}, Caída en Y: {caida_en_y}, Conectores: {conectores}, Cantidad: {cantidad}, Estante ID: {estante_id}",
            fecha=datetime.utcnow()
        )
        db.session.add(nuevo_historial)
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
        # Guardamos los datos antiguos para registrar cambios
        datos_anteriores = f"Arnes: {equipos_alturas.arnes}, Eslingas: {equipos_alturas.eslingas}, Posicionamiento: {equipos_alturas.posicionamiento}, Caída en Y: {equipos_alturas.caida_en_y}, Conectores: {equipos_alturas.conectores}, Cantidad: {equipos_alturas.cantidad}, Estante ID: {equipos_alturas.estante_id}"

        equipos_alturas.arnes = request.form['arnes']
        equipos_alturas.eslingas = request.form['eslingas']
        equipos_alturas.posicionamiento = request.form['posicionamiento']
        equipos_alturas.caida_en_y = request.form['caida_en_y']
        equipos_alturas.conectores = request.form['conectores']
        equipos_alturas.cantidad = request.form['cantidad']
        equipos_alturas.estante_id = request.form['estante_id']

        db.session.commit()

        # Registro en el historial con los cambios
        nuevo_historial = Historial(
            usuario_id=current_user.id,
            tabla="EquiposAltura",
            accion=f"Editó equipo de altura (antes: {datos_anteriores}, después: Arnes: {equipos_alturas.arnes}, Eslingas: {equipos_alturas.eslingas}, Posicionamiento: {equipos_alturas.posicionamiento}, Caída en Y: {equipos_alturas.caida_en_y}, Conectores: {equipos_alturas.conectores}, Cantidad: {equipos_alturas.cantidad}, Estante ID: {equipos_alturas.estante_id})",
            fecha=datetime.utcnow()
        )
        db.session.add(nuevo_historial)
        db.session.commit()

        flash('Equipo de altura actualizado exitosamente', 'success')
        return redirect(url_for('equipos_alturas.get_equipos_alturas'))
    
    estantes = Estantes.query.all()
    return render_template('alturas/edit.html', equipos_alturas=equipos_alturas, estantes=estantes)

# Ruta para eliminar un equipo de altura
@bp.route('/equipos_alturas/delete/<int:idequiposaltura>', methods=['POST'])
@login_required
def delete_equipos_alturas(idequiposaltura):
    equipos_alturas = EquiposAltura.query.get_or_404(idequiposaltura)

    # Guardamos los detalles del equipo eliminado para el historial
    detalles = f"Arnes: {equipos_alturas.arnes}, Eslingas: {equipos_alturas.eslingas}, Posicionamiento: {equipos_alturas.posicionamiento}, Caída en Y: {equipos_alturas.caida_en_y}, Conectores: {equipos_alturas.conectores}, Cantidad: {equipos_alturas.cantidad}, Estante ID: {equipos_alturas.estante_id}"

    db.session.delete(equipos_alturas)
    db.session.commit()

    # Registro en el historial
    nuevo_historial = Historial(
        usuario_id=current_user.id,
        tabla="EquiposAltura",
        accion=f"Eliminó equipo de altura: {detalles}",
        fecha=datetime.utcnow()
    )
    db.session.add(nuevo_historial)
    db.session.commit()

    flash('Equipo de altura eliminado exitosamente', 'success')
    return redirect(url_for('equipos_alturas.get_equipos_alturas'))
