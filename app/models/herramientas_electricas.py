from .. import db

class HerramientasElectricas(db.Model):
    __tablename__ = 'herramientas_electricas'
    idherramientaselectricas = db.Column(db.Integer, primary_key=True)
    marca = db.Column(db.String(100), nullable=False)
    nombre = db.Column(db.String(100), nullable=False)#responsable
    modelo = db.Column(db.String(100), nullable=False)
    descripcion_producto = db.Column(db.String(100), nullable=False) #estado
    fecha_adquisicion = db.Column(db.String(100), nullable=False) #estado
    observacion = db.Column(db.String(100))
    estante_id = db.Column(db.Integer, db.ForeignKey('estante.id_estante'), nullable=False)
    estante = db.relationship('Estantes', back_populates='herramientas_electricas')

