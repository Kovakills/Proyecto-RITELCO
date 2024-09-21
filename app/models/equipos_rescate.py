from app import db

class EquiposRescate(db.Model):
    __tablename__ = 'equipos_rescate'
    idequiposrescate = db.Column(db.Integer, primary_key=True)
    arnes = db.Column(db.String(100), nullable=False)
    eslingas = db.Column(db.String(100), nullable=False)
    posicionamiento = db.Column(db.String(100), nullable=False)
    caida_en_y = db.Column(db.String(100), nullable=False)
    conectores = db.Column(db.String(100), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False, default=1)
    estante_id = db.Column(db.Integer, db.ForeignKey('estante.id_estante'), nullable=False)
    estante = db.relationship('Estantes', back_populates='equipos_rescate')
