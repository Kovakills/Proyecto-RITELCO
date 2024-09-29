from flask import Blueprint, request, jsonify
from ..models.estante import Estantes 
from .. import db

bp = Blueprint('estantes', __name__)

@bp.route('/1', methods=['GET'])
def get_estantes():
    estantes = Estantes.query.all()
    result = [{'id_estante': estante.id_estante, 'descripcion_producto': estante.descripcion_producto} for estante in estantes]
    return jsonify(result)

@bp.route('/2', methods=['POST'])
def add_estante():
    data = request.get_json()
    new_estante = Estantes(descripcion_producto=data['descripcion_producto'])
    db.session.add(new_estante)
    db.session.commit()
    return jsonify({'message': 'Estante added successfully'}), 201
