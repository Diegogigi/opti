#!/usr/bin/env python3
"""
Script para inicializar la base de datos PostgreSQL en Railway
"""

import os
import sys
from datetime import datetime

# Agregar el directorio actual al path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))


def init_railway_database():
    """Inicializar base de datos en Railway"""
    print("🚀 Inicializando base de datos en Railway...")

    # Verificar variables de entorno
    database_url = os.environ.get("DATABASE_URL")
    print(f"📋 DATABASE_URL configurada: {'Sí' if database_url else 'No'}")

    if database_url:
        print(f"🔗 URL de base de datos: {database_url[:50]}...")
    else:
        print("❌ DATABASE_URL no está configurada")
        print("💡 Asegúrate de configurar la variable DATABASE_URL en Railway")
        return False

    try:
        # Importar después de verificar la configuración
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

        with app.app_context():
            print("🔄 Creando tablas en PostgreSQL...")
            db.create_all()
            print("✅ Tablas creadas correctamente")

            # Verificar que las tablas existen
            try:
                from sqlalchemy import inspect

                inspector = inspect(db.engine)
                tables = inspector.get_table_names()
                print(f"📋 Tablas disponibles: {', '.join(tables)}")

                # Crear datos de ejemplo si no existen
                if not User.query.first():
                    print("🔄 Creando datos de ejemplo...")
                    create_sample_data()
                else:
                    print("ℹ️ Ya existen usuarios en la base de datos")

                return True

            except Exception as e:
                print(f"❌ Error al verificar tablas: {e}")
                return False

    except Exception as e:
        print(f"❌ Error al inicializar base de datos: {e}")
        return False


def create_sample_data():
    """Crear datos de ejemplo"""
    try:
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
        )

        with app.app_context():
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
            
            # Crear configuración de aplicación para usuario particular
            individual_app_settings = UserAppSettings(
                user_id=individual_user.id,
                default_pattern="D,D,L,L,N,N",
                default_pattern_preset="2x2",
                default_shift_type="day",
                default_vacation_calculation="traditional",
                default_vacation_budget=15,
                default_min_win=7,
                default_max_win=14,
                auto_save_enabled=True
            )
            db.session.add(individual_app_settings)
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

    except Exception as e:
        print(f"❌ Error al crear datos de ejemplo: {e}")


if __name__ == "__main__":
    print("=" * 60)
    print("🚀 INICIALIZACIÓN DE BASE DE DATOS RAILWAY")
    print("=" * 60)

    success = init_railway_database()

    if success:
        print("=" * 60)
        print("✅ Base de datos inicializada exitosamente")
        print("🌐 La aplicación está lista para usar")
        print("=" * 60)
    else:
        print("=" * 60)
        print("❌ Error al inicializar la base de datos")
        print("🔧 Verifica la configuración en Railway")
        print("=" * 60)
        sys.exit(1)
