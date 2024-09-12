from flask import Blueprint, request, render_template, redirect, url_for, flash
from flask_login import login_required
from ..models.sistema_pt import SistemaPT
from ..models.estante import Estantes
from .. import db

bp = Blueprint('sistema_pt', __name__)

@bp.route('/sistema_pt', methods=['GET'])
@login_required
def get_sistema_pt(): 
    data = SistemaPT.query.all()
    return render_template('pt/index.html', data=data)

@bp.route('/sistema_pt/add', methods=['GET', 'POST'])
@login_required
def add_sistema_pt():
    if request.method == 'POST':
        unidad_medida = request.form['unidad_medida']
        descripcion_producto = request.form['descripcion_producto']
        cantidad = int(request.form['cantidad'])
        observacion = request.form['observacion']
        estante_id = request.form['estante_id']

        estante = Estantes.query.get(estante_id)
        if estante is None:
            flash('El estante con el ID proporcionado no existe.', 'error')
            return redirect(url_for('sistema_pt.add_sistema_pt'))

        new_equipobt = SistemaPT(unidad_medida=unidad_medida, descripcion_producto=descripcion_producto, cantidad=cantidad, observacion=observacion, estante_id=estante_id)
        db.session.add(new_equipobt)
        db.session.commit()
        flash('Sistema puesta a tierra añadido exitosamente', 'success')
        return redirect(url_for('sistema_pt.get_sistema_pt'))
    
    estantes = Estantes.query.all()
    
    return render_template('pt/add.html', estantes=estantes)

@bp.route('/sistema_pt/edit/<int:idsistemapt>', methods=['GET', 'POST'])
@login_required
def edit_sistema_pt(idsistemapt):
    sistema_pt = SistemaPT.query.get_or_404(idsistemapt)

    if request.method == 'POST':
        sistema_pt.unidad_medida = request.form['unidad_medida']
        sistema_pt.estante_id = request.form['estante_id']
        sistema_pt.descripcion_producto = request.form['descripcion_producto']
        sistema_pt.observacion = request.form['observacion']
        sistema_pt.cantidad = int(request.form['cantidad'])
        db.session.commit()
        return redirect(url_for('sistema_pt.get_sistema_pt', idsistemapt=idsistemapt))
    estantes = Estantes.query.all()
    return render_template('pt/edit.html', sistema_pt=sistema_pt, estantes=estantes)



@bp.route('/sistema_pt/delete/<int:idsistemapt>', methods=['POST'])
@login_required
def delete_sistema_pt(idsistemapt):
    equipobt = SistemaPT.query.get_or_404(idsistemapt)
    db.session.delete(equipobt)
    db.session.commit()
    flash('Sistema puesta a tierra eliminado exitosamente', 'success')
    return redirect(url_for('sistema_pt.get_sistema_pt'))