# app/models/electronica.py
from .. import db

class Electronica(db.Model):
    __tablename__ = 'electronica'
    idelectronica = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    descripcion_producto = db.Column(db.String(100), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False, default=1)
    estante_id = db.Column(db.Integer, db.ForeignKey('estante.id_estante'), nullable=False)
    estante = db.relationship('Estantes', back_populates='electronica')