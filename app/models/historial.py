from app import db

class Historial(db.Model):
    __tablename__ = 'historial'
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)  # Cambia 'users' a 'usuario'
    tabla = db.Column(db.String(50), nullable=False)
    accion = db.Column(db.String(255), nullable=False)
    registro_id = db.Column(db.Integer, nullable=True)  # ID del registro afectado (aceite, estante, etc.)
    fecha = db.Column(db.DateTime, nullable=False)

    usuario = db.relationship('Usuario', backref='historiales')  # Cambia 'Users' a 'Usuario'
