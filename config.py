import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or "dev-secret-key-change-in-production"

    # Configuración de la base de datos
    DATABASE_URL = os.environ.get("DATABASE_URL")
    if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
        DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

    # Si no hay DATABASE_URL, usar SQLite para desarrollo
    if DATABASE_URL:
        SQLALCHEMY_DATABASE_URI = DATABASE_URL
    else:
        SQLALCHEMY_DATABASE_URI = "sqlite:///opti.db"

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Configuración de la aplicación
    DEBUG = os.environ.get("FLASK_ENV") == "development"
