from flask import blueprints

from .aceites_routes import aceite_bp
from .baja_tension_routes import baja_tension_bp
from .electronica_routes import electronica_bp
from .equipos_altura_routes import equipos_altura_bp
from .equipos_media_tension_routes import equipos_media_tension_bp
from .estante_routes import estante_bp
from .filtros_routes import filtros_bp
from .herramientas_electricas_routes import herramientas_electricas_bp
from .herramientas_inalambricas_routes import herramientas_inalambricas_bp
from .respels_routes import respels_bp
from .sistema_pt_routes import sistema_pt_bp
from routes import planta_bp
from routes import herramientas_bp
from routes import spt_bp



def register_blueprints(app):
    app.register_blueprint(aceite_bp, url_prefix='/aceites')
    app.register_blueprint(baja_tension_bp, url_prefix='/baja_tension')
    app.register_blueprint(electronica_bp, url_prefix='/electronica')
    app.register_blueprint(equipos_altura_bp, url_prefix='/equipos_altura')
    app.register_blueprint(equipos_media_tension_bp, url_prefix='/equipos_media_tension')
    app.register_blueprint(estante_bp, url_prefix='/estante')
    app.register_blueprint(filtros_bp, url_prefix='/filtros')
    app.register_blueprint(herramientas_electricas_bp, url_prefix='/herramientas_electricas')
    app.register_blueprint(herramientas_inalambricas_bp, url_prefix='/herramientas_inalambricas')
    app.register_blueprint(respels_bp, url_prefix='/respels')
    app.register_blueprint(sistema_pt_bp, url_prefix='/sistema_pt')
    app.register_blueprint(planta_bp)
    app.register_blueprint(herramientas_bp)
    app.register_blueprint(spt_bp)
    

__all__ = ['register_blueprints']
