from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json
from flask_login import UserMixin

db = SQLAlchemy()


class User(db.Model, UserMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    company = db.Column(db.String(100))
    position = db.Column(db.String(100))
    user_type = db.Column(
        db.String(20), default="individual"
    )  # "individual" o "company"
    company_size = db.Column(db.String(20))  # "small", "medium", "large"
    industry = db.Column(db.String(100))  # Sector de la empresa
    is_company_admin = db.Column(
        db.Boolean, default=False
    )  # Para administradores de empresa
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_access = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)

    # Relaciones
    shift_patterns = db.relationship("ShiftPattern", backref="user", lazy=True)
    calendars = db.relationship("Calendar", backref="user", lazy=True)
    vacations = db.relationship("Vacation", backref="user", lazy=True)
    ai_suggestions = db.relationship("AISuggestion", backref="user", lazy=True)
    user_settings = db.relationship("UserSettings", backref="user", uselist=False)

    def get_id(self):
        """Método requerido por Flask-Login"""
        return str(self.id)

    def is_authenticated(self):
        """Método requerido por Flask-Login"""
        return True

    def is_anonymous(self):
        """Método requerido por Flask-Login"""
        return False

    @property
    def is_company_user(self):
        """Verificar si es usuario de empresa"""
        return self.user_type == "company"

    @property
    def is_individual_user(self):
        """Verificar si es usuario particular"""
        return self.user_type == "individual"


class ShiftPattern(db.Model):
    __tablename__ = "shift_patterns"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    pattern = db.Column(db.String(200), nullable=False)  # "D,D,L,L,N,N,L,L"
    shift_type = db.Column(db.String(20), nullable=False)  # "day", "night", "mixed"
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)


class Calendar(db.Model):
    __tablename__ = "calendars"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    pattern_id = db.Column(db.Integer, db.ForeignKey("shift_patterns.id"))
    overrides = db.Column(db.Text)  # JSON string de overrides
    holidays_included = db.Column(db.String(50), default="nacional+electoral")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def get_overrides(self):
        """Convertir overrides JSON a diccionario"""
        if self.overrides:
            return json.loads(self.overrides)
        return {}

    def set_overrides(self, overrides_dict):
        """Convertir diccionario de overrides a JSON"""
        self.overrides = json.dumps(overrides_dict)


class Vacation(db.Model):
    __tablename__ = "vacations"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    days_used = db.Column(db.Integer, nullable=False)
    calculation_type = db.Column(
        db.String(20), default="traditional"
    )  # "traditional", "shift-based", "all-days"
    status = db.Column(
        db.String(20), default="pending"
    )  # "pending", "approved", "rejected"
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class AISuggestion(db.Model):
    __tablename__ = "ai_suggestions"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    strategy = db.Column(
        db.String(50), nullable=False
    )  # "max_consecutive", "holiday_optimization", etc.
    score = db.Column(db.Float, nullable=False)
    work_days = db.Column(db.Integer, nullable=False)
    holidays_included = db.Column(db.Integer, default=0)
    ai_reason = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Holiday(db.Model):
    __tablename__ = "holidays"

    id = db.Column(db.Integer, primary_key=True)
    year = db.Column(db.Integer, nullable=False)
    date = db.Column(db.Date, nullable=False)
    name = db.Column(db.String(200), nullable=False)
    is_irrenunciable = db.Column(db.Boolean, default=False)
    scope = db.Column(
        db.String(50), default="nacional"
    )  # "nacional", "regional", "local"
    source = db.Column(db.String(20), default="api")  # "api", "local"
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    __table_args__ = (
        db.UniqueConstraint("year", "date", name="unique_holiday_year_date"),
    )


class UserSettings(db.Model):
    __tablename__ = "user_settings"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    theme = db.Column(db.String(20), default="dark")  # "dark", "light"
    auto_save = db.Column(db.Boolean, default=True)
    notifications = db.Column(db.Boolean, default=True)
    language = db.Column(db.String(10), default="es")
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )


class CompanyEmployee(db.Model):
    __tablename__ = "company_employees"

    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    employee_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    employee_code = db.Column(db.String(50))  # Código interno del empleado
    department = db.Column(db.String(100))  # Departamento
    supervisor_id = db.Column(db.Integer, db.ForeignKey("users.id"))  # Supervisor
    hire_date = db.Column(db.Date)  # Fecha de contratación
    vacation_days_available = db.Column(
        db.Integer, default=21
    )  # Días de vacaciones disponibles
    vacation_days_used = db.Column(db.Integer, default=0)  # Días de vacaciones usados
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    # Relaciones
    company = db.relationship("User", foreign_keys=[company_id], backref="employees")
    employee = db.relationship(
        "User", foreign_keys=[employee_id], backref="employments"
    )
    supervisor = db.relationship(
        "User", foreign_keys=[supervisor_id], backref="subordinates"
    )


class CompanySettings(db.Model):
    __tablename__ = "company_settings"

    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    default_vacation_days = db.Column(
        db.Integer, default=21
    )  # Días de vacaciones por defecto
    vacation_policy = db.Column(db.Text)  # Política de vacaciones
    shift_policy = db.Column(db.Text)  # Política de turnos
    approval_required = db.Column(
        db.Boolean, default=True
    )  # Requiere aprobación de vacaciones
    auto_approve_vacations = db.Column(
        db.Boolean, default=False
    )  # Aprobación automática
    notification_email = db.Column(db.String(120))  # Email para notificaciones
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    # Relación
    company = db.relationship("User", backref="company_settings")


class UserAppSettings(db.Model):
    __tablename__ = "user_app_settings"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    # Configuración de rangos de fechas
    default_start_date = db.Column(db.String(10))  # YYYY-MM-DD
    default_end_date = db.Column(db.String(10))  # YYYY-MM-DD
    default_pattern_start = db.Column(db.String(10))  # YYYY-MM-DD

    # Configuración de patrones
    default_pattern = db.Column(db.String(200))  # "D,D,L,L,N,N"
    default_pattern_preset = db.Column(db.String(20))  # "2x2", "4x3", etc.
    default_shift_type = db.Column(db.String(20))  # "day", "night", "mixed"

    # Configuración de vacaciones
    default_vacation_calculation = db.Column(
        db.String(20)
    )  # "traditional", "shift-based", "all-days"
    default_vacation_budget = db.Column(db.Integer, default=15)
    default_min_win = db.Column(db.Integer, default=7)
    default_max_win = db.Column(db.Integer, default=14)

    # Configuración de overrides
    overrides = db.Column(db.Text)  # JSON string de overrides

    # Configuración de preferencias
    auto_save_enabled = db.Column(db.Boolean, default=True)
    last_used_config = db.Column(
        db.Text
    )  # JSON string de la última configuración usada

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    # Relación
    user = db.relationship("User", backref="app_settings")

    def get_overrides(self):
        """Convertir overrides JSON a diccionario"""
        if self.overrides:
            return json.loads(self.overrides)
        return {}

    def set_overrides(self, overrides_dict):
        """Convertir diccionario de overrides a JSON"""
        self.overrides = json.dumps(overrides_dict)

    def get_last_config(self):
        """Obtener la última configuración usada"""
        if self.last_used_config:
            return json.loads(self.last_used_config)
        return {}

    def set_last_config(self, config_dict):
        """Guardar la última configuración usada"""
        self.last_used_config = json.dumps(config_dict)
