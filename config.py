import os

class Config:
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))  # Obtiene la ruta absoluta del directorio actual
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(BASE_DIR, 'database.db')}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
