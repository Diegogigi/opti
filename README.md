# OPTI - Planificador de Turnos y Vacaciones

🌙 **Sistema inteligente para optimizar turnos y vacaciones en Chile**

## 🚀 Características

### ✨ **Funcionalidades Principales**

- **Gestión de Turnos**: Patrones personalizables (2x2, 4x3, 5x2, etc.)
- **IA Inteligente**: Sugerencias optimizadas de vacaciones
- **Cálculo de Vacaciones**: Tradicional, según turnos, o todos los días
- **Exportación**: Archivos ICS y CSV
- **Feriados Chile**: Incluye feriados nacionales, electorales y regionales
- **Sistema de Usuarios**: Login y sesiones individuales

### 🔐 **Sistema de Autenticación**

- **Login por Email**: Sistema simple y seguro
- **Registro de Usuarios**: Crear cuentas personalizadas
- **Sesiones Persistentes**: Mantener sesión activa
- **Perfiles de Usuario**: Información personal y configuración

### 🤖 **IA Avanzada**

- **Múltiples Estrategias**: 6 algoritmos diferentes de optimización
- **Análisis de Patrones**: Identificación de oportunidades
- **Optimización de Puentes**: Conexión con fines de semana
- **Temporadas Preferidas**: Priorización por estaciones

## 🛠️ Instalación

### Requisitos

- Python 3.8+
- PostgreSQL (opcional, SQLite por defecto)

### Pasos de Instalación

1. **Clonar el repositorio**

```bash
git clone <repository-url>
cd opti
```

2. **Crear entorno virtual**

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# o
venv\Scripts\activate     # Windows
```

3. **Instalar dependencias**

```bash
pip install -r requirements.txt
```

4. **Configurar variables de entorno**

```bash
# Crear archivo .env
SECRET_KEY=tu-clave-secreta-aqui
DATABASE_URL=postgresql://usuario:password@localhost/opti_db
FLASK_ENV=development
```

5. **Inicializar base de datos**

```bash
python migrations.py
```

6. **Ejecutar la aplicación**

```bash
python app.py
```

## 📱 Uso

### **Primera vez**

1. Ir a `http://localhost:5000`
2. Crear una cuenta nueva en `/register`
3. Iniciar sesión con tu email

### **Usuario Demo**

- **Email**: `demo@opti.cl`
- **Contraseña**: Solo email (sistema simplificado)

### **Funcionalidades**

1. **Configurar Patrón**: Seleccionar o crear patrón de turnos
2. **Definir Rango**: Establecer período de análisis
3. **Generar Calendario**: Crear horario de turnos
4. **Obtener Sugerencias**: IA recomienda mejores fechas
5. **Exportar**: Descargar archivos ICS/CSV

## 🏗️ Arquitectura

### **Backend**

- **Flask**: Framework web
- **SQLAlchemy**: ORM para base de datos
- **Flask-Login**: Sistema de autenticación
- **PostgreSQL/SQLite**: Base de datos

### **Frontend**

- **HTML5/CSS3**: Interfaz moderna y responsive
- **JavaScript**: Funcionalidades dinámicas
- **Tema Oscuro/Claro**: Interfaz adaptable

### **Base de Datos**

- **Users**: Información de usuarios
- **ShiftPatterns**: Patrones de turnos
- **Calendars**: Calendarios generados
- **Vacations**: Vacaciones planificadas
- **AISuggestions**: Sugerencias de IA
- **Holidays**: Feriados de Chile
- **UserSettings**: Configuraciones de usuario

## 🔧 API Endpoints

### **Autenticación**

- `POST /api/user/register` - Registrar usuario
- `POST /api/user/login` - Iniciar sesión
- `GET /api/user/profile` - Perfil del usuario

### **Turnos**

- `POST /api/build` - Generar calendario
- `POST /api/pattern/save` - Guardar patrón
- `GET /api/patterns` - Obtener patrones

### **Vacaciones**

- `POST /api/suggest` - Sugerencias de IA
- `POST /api/vacation/save` - Guardar vacación
- `GET /api/vacations` - Obtener vacaciones

### **Exportación**

- `POST /api/export_ics` - Exportar ICS
- `POST /api/export_csv` - Exportar CSV

### **Utilidades**

- `GET /health` - Estado de la aplicación
- `GET /api/holidays/<year>` - Feriados por año

## 🚀 Despliegue

### **Railway (Recomendado)**

1. Conectar repositorio a Railway
2. Configurar variables de entorno
3. Desplegar automáticamente

### **Heroku**

```bash
heroku create opti-app
heroku config:set SECRET_KEY=tu-clave-secreta
heroku config:set DATABASE_URL=postgresql://...
git push heroku main
```

### **Docker**

```bash
docker build -t opti .
docker run -p 5000:5000 opti
```

## 📊 Características Técnicas

### **Optimización de IA**

- **Algoritmo 1**: Maximizar días libres consecutivos
- **Algoritmo 2**: Optimizar alrededor de feriados
- **Algoritmo 3**: Minimizar pérdida de días de trabajo
- **Algoritmo 4**: Crear puentes con fines de semana
- **Algoritmo 5**: Priorizar temporadas preferidas
- **Algoritmo 6**: Análisis inteligente de patrones

### **Seguridad**

- **Sesiones seguras**: Cookies HTTPOnly
- **Autenticación**: Sistema robusto de login
- **Validación**: Verificación de datos de entrada
- **CSRF Protection**: Protección contra ataques

### **Rendimiento**

- **Caché de feriados**: Optimización de consultas
- **Lazy loading**: Carga diferida de datos
- **Compresión**: Respuestas optimizadas
- **CDN**: Archivos estáticos optimizados

## 🤝 Contribuir

1. Fork el proyecto
2. Crear rama de feature (`git checkout -b feature/AmazingFeature`)
3. Commit cambios (`git commit -m 'Add AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abrir Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver `LICENSE` para más detalles.

## 🆘 Soporte

- **Issues**: Reportar bugs en GitHub
- **Documentación**: Ver código y comentarios
- **Comunidad**: Discusiones en GitHub Discussions

---

**OPTI** - Optimizando turnos y vacaciones para trabajadores chilenos 🌟
