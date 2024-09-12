# app/models/filtros.py
from .. import db

class Filtros(db.Model):
    __tablename__ = 'filtro'
    id = db.Column(db.Integer, primary_key=True)
    marca = db.Column(db.String(100), nullable=False)
    tipo_de_filtro = db.Column(db.String(100), nullable=False)
    referencia = db.Column(db.String(100), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False, default=1)
    observacion = db.Column(db.String(100))
    estante_id = db.Column(db.Integer, db.ForeignKey('estante.id_estante'), nullable=False)
    estante = db.relationship('Estantes', back_populates='filtros')
