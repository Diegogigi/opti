#!/usr/bin/env python3
"""
Script de migración para inicializar la base de datos de OPTI
"""

import os
import sys
from datetime import datetime

# Agregar el directorio actual al path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import app, db
from database import (
    User,
    ShiftPattern,
    Calendar,
    Vacation,
    AISuggestion,
    Holiday,
    UserSettings,
    CompanyEmployee,
    CompanySettings,
    UserAppSettings,
)


def init_database():
    """Inicializar la base de datos y crear tablas"""
    print("🔄 Inicializando base de datos...")

    with app.app_context():
        try:
            # Crear todas las tablas
            db.create_all()
            print("✅ Tablas creadas correctamente")

            # Verificar que las tablas existen (compatible con SQLAlchemy 2.0)
            try:
                from sqlalchemy import inspect

                inspector = inspect(db.engine)
                tables = inspector.get_table_names()
                print(f"📋 Tablas disponibles: {', '.join(tables)}")
            except:
                print("📋 Tablas creadas (verificación omitida)")

            return True

        except Exception as e:
            print(f"❌ Error al crear tablas: {e}")
            return False


def create_sample_data():
    """Crear datos de ejemplo para pruebas"""
    print("🔄 Creando datos de ejemplo...")

    with app.app_context():
        try:
            # Verificar si ya hay usuarios
            if User.query.first():
                print("ℹ️ Ya existen usuarios en la base de datos")
                return True

            # Crear usuario particular de ejemplo
            individual_user = User(
                email="demo@opti.cl",
                name="Usuario Demo",
                company="Empresa Demo",
                position="Trabajador",
                user_type="individual",
            )
            db.session.add(individual_user)
            db.session.commit()

            # Crear configuración por defecto para usuario particular
            individual_settings = UserSettings(user_id=individual_user.id)
            db.session.add(individual_settings)
            db.session.commit()

            # Crear empresa de ejemplo
            company_user = User(
                email="empresa@demo.cl",
                name="Empresa Demo SPA",
                company="Empresa Demo SPA",
                position="Administrador",
                user_type="company",
                company_size="medium",
                industry="technology",
                is_company_admin=True,
            )
            db.session.add(company_user)
            db.session.commit()

            # Crear configuración por defecto para empresa
            company_settings = UserSettings(user_id=company_user.id)
            db.session.add(company_settings)
            db.session.commit()

            # Crear configuración de empresa
            company_config = CompanySettings(
                company_id=company_user.id,
                default_vacation_days=21,
                approval_required=True,
                auto_approve_vacations=False,
            )
            db.session.add(company_config)
            db.session.commit()

            # Crear empleado de ejemplo para la empresa
            employee = User(
                email="empleado@demo.cl",
                name="Juan Pérez",
                position="Desarrollador",
                user_type="individual",
            )
            db.session.add(employee)
            db.session.commit()

            # Relacionar empleado con empresa
            company_employee = CompanyEmployee(
                company_id=company_user.id,
                employee_id=employee.id,
                employee_code="EMP001",
                department="Tecnología",
                hire_date=datetime(2024, 1, 15).date(),
                vacation_days_available=21,
            )
            db.session.add(company_employee)
            db.session.commit()

            print("✅ Datos de ejemplo creados correctamente")
            print(f"👤 Usuario particular: {individual_user.email}")
            print(f"🏢 Empresa: {company_user.email}")
            print(f"👷 Empleado: {employee.email}")

            return True

        except Exception as e:
            print(f"❌ Error al crear datos de ejemplo: {e}")
            db.session.rollback()
            return False


def main():
    """Función principal"""
    print("🚀 Iniciando migración de base de datos OPTI")
    print("=" * 50)

    # Inicializar base de datos
    if not init_database():
        print("❌ Falló la inicialización de la base de datos")
        sys.exit(1)

    # Crear datos de ejemplo
    create_sample_data()

    print("=" * 50)
    print("✅ Migración completada exitosamente")
    print("🌐 La aplicación está lista para usar")


if __name__ == "__main__":
    main()
