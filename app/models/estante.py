from .. import db

class Estantes(db.Model):
    __tablename__ = 'estante'
    id_estante = db.Column(db.Integer, primary_key=True)
    descripcion_producto = db.Column(db.String(100), nullable=False)
    nombre = db.Column(db.String(100), nullable=False)
    aceites = db.relationship('Aceites', back_populates='estante')
    herramientas_electricas = db.relationship('HerramientasElectricas', back_populates='estante')
    herramientas_inalambricas = db.relationship('HerramientasInalambricas', back_populates='estante')
    respels = db.relationship('Respels', back_populates='estante')
    baja_tension = db.relationship('BajaTension', back_populates='estante')
    equipos_media_tension = db.relationship('EquiposMediaTension', back_populates='estante')
    filtros = db.relationship('Filtros', back_populates='estante')
    sistema_pt = db.relationship('SistemaPT', back_populates='estante')
    equipos_altura = db.relationship('EquiposAltura', back_populates='estante')
    equipos_rescate = db.relationship('EquiposRescate', back_populates='estante')

