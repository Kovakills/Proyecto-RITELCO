# app/models/sistema_pt.py
from .. import db

class SistemaPT(db.Model):
    __tablename__ = 'sistema_pt'
    idsistemapt = db.Column(db.Integer, primary_key=True)
    unidad_medida = db.Column(db.String(100), nullable=False)
    descripcion_producto = db.Column(db.String(100), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False, default=1)
    observacion = db.Column(db.String(100))
    estante_id = db.Column(db.Integer, db.ForeignKey('estante.id_estante'), nullable=False)
    estante = db.relationship('Estantes', back_populates='sistema_pt')