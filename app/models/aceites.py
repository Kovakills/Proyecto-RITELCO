from .. import db

class Aceites(db.Model):
    __tablename__ = 'aceite'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    tipo_de_aceite = db.Column(db.String(100), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False, default=1)
    estante_id = db.Column(db.Integer, db.ForeignKey('estante.id_estante'), nullable=False)

    estante = db.relationship('Estantes', back_populates='aceites')
