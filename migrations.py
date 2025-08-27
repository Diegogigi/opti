from app import app, db
from database import (
    User,
    ShiftPattern,
    Calendar,
    Vacation,
    AISuggestion,
    Holiday,
    UserSettings,
)
from datetime import datetime, date


def init_db():
    """Inicializar la base de datos con las tablas"""
    with app.app_context():
        # Crear todas las tablas
        db.create_all()
        print("✅ Base de datos inicializada correctamente")


def create_sample_data():
    """Crear datos de ejemplo para testing"""
    with app.app_context():
        # Crear usuario de ejemplo
        user = User(
            email="usuario@ejemplo.com",
            name="Usuario Ejemplo",
            company="Empresa ABC",
            position="Operador",
        )
        db.session.add(user)
        db.session.commit()

        # Crear patrón de turnos de ejemplo
        pattern = ShiftPattern(
            user_id=user.id,
            name="Mi Patrón 2x2",
            pattern="D,D,L,L,N,N,L,L",
            shift_type="mixed",
            description="Turno personalizado 2x2 mixto",
        )
        db.session.add(pattern)
        db.session.commit()

        # Crear configuración de usuario
        settings = UserSettings(
            user_id=user.id,
            theme="dark",
            auto_save=True,
            notifications=True,
            language="es",
        )
        db.session.add(settings)
        db.session.commit()

        print("✅ Datos de ejemplo creados correctamente")


if __name__ == "__main__":
    init_db()
    create_sample_data()
