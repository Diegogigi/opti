from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    company = db.Column(db.String(100))
    position = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_access = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)

    # Relaciones
    shift_patterns = db.relationship("ShiftPattern", backref="user", lazy=True)
    calendars = db.relationship("Calendar", backref="user", lazy=True)
    vacations = db.relationship("Vacation", backref="user", lazy=True)
    ai_suggestions = db.relationship("AISuggestion", backref="user", lazy=True)
    user_settings = db.relationship("UserSettings", backref="user", uselist=False)


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
