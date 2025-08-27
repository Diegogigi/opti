# 🚀 Configuración de Railway para OPTI

## 📋 Pasos para Configurar PostgreSQL en Railway

### 1. **Crear Base de Datos PostgreSQL**

1. Ve a tu proyecto en Railway
2. Haz clic en **"New Service"**
3. Selecciona **"Database"** → **"PostgreSQL"**
4. Dale un nombre como `opti-postgres`

### 2. **Configurar Variable de Entorno**

1. Ve a tu servicio de aplicación (no el de la base de datos)
2. Haz clic en **"Variables"**
3. Agrega una nueva variable:
   - **Nombre:** `DATABASE_URL`
   - **Valor:** `${{Postgres.DATABASE_URL}}`
4. Haz clic en **"Add"**

### 3. **Verificar Configuración**

La variable `DATABASE_URL` debe tener un formato como:

```
postgresql://username:password@host:port/database
```

### 4. **Reiniciar Aplicación**

1. Ve a tu servicio de aplicación
2. Haz clic en **"Deploy"** → **"Deploy Now**
3. Esto ejecutará automáticamente `python init_db.py` para crear las tablas

### 5. **Verificar Tablas Creadas**

1. Ve a tu servicio PostgreSQL
2. Haz clic en **"Connect"** → \*\*"PostgreSQL"
3. Deberías ver las siguientes tablas:
   - `users`
   - `shift_patterns`
   - `calendars`
   - `vacations`
   - `ai_suggestions`
   - `holidays`
   - `user_settings`
   - `company_employees`
   - `company_settings`

## 🔧 Solución de Problemas

### **Problema: No aparecen tablas**

- Verifica que `DATABASE_URL` esté configurada correctamente
- Revisa los logs de la aplicación en Railway
- Ejecuta manualmente: `python init_db.py`

### **Problema: Error de conexión**

- Verifica que el servicio PostgreSQL esté activo
- Asegúrate de que la variable `DATABASE_URL` use `${{Postgres.DATABASE_URL}}`

### **Problema: Aplicación no inicia**

- Verifica que todas las dependencias estén en `requirements.txt`
- Revisa los logs de Railway para errores específicos

## 📊 Verificar Estado

### **Endpoint de Salud:**

```
GET /health
```

### **Endpoint de Base de Datos:**

```
GET /api/db-status
```

### **Respuesta Esperada:**

```json
{
  "status": "healthy",
  "database_url": "configured",
  "user_count": 3,
  "tables": ["users", "shift_patterns", ...],
  "table_count": 9
}
```

## 🎯 Usuarios de Prueba

Una vez configurado, tendrás estos usuarios disponibles:

- **👤 Usuario Particular:** `demo@opti.cl`
- **🏢 Empresa:** `empresa@demo.cl`
- **👷 Empleado:** `empleado@demo.cl`

## 🔄 Reinicializar Base de Datos

Si necesitas reinicializar la base de datos:

1. Ve a Railway CLI o ejecuta en tu aplicación:

```bash
python init_db.py
```

2. O reinicia el servicio de aplicación (ejecutará automáticamente la inicialización)

## 📝 Notas Importantes

- **No elimines** el servicio PostgreSQL una vez creado
- **Mantén** la variable `DATABASE_URL` configurada
- **Los datos** se mantienen entre reinicios
- **Las tablas** se crean automáticamente en el primer despliegue

---

**¡Con estos pasos tu aplicación OPTI estará completamente funcional en Railway con PostgreSQL!** 🎉
