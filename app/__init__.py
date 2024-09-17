from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.urandom(24)
    app.config.from_object('config.Config')

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    @login_manager.user_loader
    def load_user(user_id):
        
        from .models.usuario import Usuario
        return Usuario.query.get(int(user_id))

    from app.routes import (
    aceites_routes, equipos_altura_routes, sistema_pt_routes,
    baja_tension_routes, equipos_media_tension_routes,
    estante_routes, electronica_routes, herramientas_electricas_routes,
    herramientas_inalambricas_routes, respels_routes,
    filtros_routes, auth_routes, planta_routes, herramientas_routes, spt_routes, page_routes, equipos_routes, equipos_rescate_routes
)


    app.register_blueprint(aceites_routes.bp)
    app.register_blueprint(equipos_altura_routes.bp)
    app.register_blueprint(sistema_pt_routes.bp)
    app.register_blueprint(baja_tension_routes.bp)
    app.register_blueprint(equipos_media_tension_routes.bp)
    app.register_blueprint(estante_routes.bp)
    app.register_blueprint(electronica_routes.bp)
    app.register_blueprint(herramientas_electricas_routes.bp)
    app.register_blueprint(herramientas_inalambricas_routes.bp)
    app.register_blueprint(respels_routes.bp)
    app.register_blueprint(filtros_routes.bp)
    app.register_blueprint(auth_routes.bp)  
    app.register_blueprint(planta_routes.bp)
    app.register_blueprint(herramientas_routes.bp)
    app.register_blueprint(spt_routes.bp)
    app.register_blueprint(page_routes.bp)
    app.register_blueprint(equipos_routes.bp)
    app.register_blueprint(equipos_rescate_routes.bp)


    with app.app_context():
        db.create_all()

    return app
