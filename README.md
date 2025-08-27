# Planificador de Turnos y Vacaciones — Chile

Una aplicación web moderna para planificar turnos de trabajo y optimizar el uso de vacaciones en Chile, considerando feriados nacionales, electorales y regionales.

## ✨ Características Principales

### 🎨 **Modo Claro/Oscuro**

- Toggle automático entre temas claro y oscuro
- Preferencias guardadas en localStorage
- Transiciones suaves entre temas

### 📅 **Calendario Inteligente**

- Visualización mensual del calendario completo
- **Patrones de turnos predefinidos**: 2x2, 4x3, 5x2, 7x7, 3x1, 6x1
- **Tipos de turno**: Solo Día, Solo Noche, Mixto (Día/Noche)
- Patrones personalizables (Libre/Día/Noche)
- Feriados y fines de semana incluidos automáticamente
- Click para marcar vacaciones, Shift+click para alternar turnos

### 🤖 **IA Inteligente Avanzada para Sugerencias**

- **Sistema de IA Avanzado**: Analiza múltiples estrategias con algoritmos mejorados
- **6 Estrategias de IA**:
  - 🔄 **Consecutivos**: Maximiza días libres consecutivos con análisis de segmentos cúbicos
  - 🎉 **Feriados**: Optimiza alrededor de feriados con centrado inteligente y bonus por noches
  - 💪 **Trabajo**: Evita días de trabajo difíciles con análisis de puentes y eficiencia
  - 🌉 **Puentes**: Crea puentes con fines de semana (jueves a martes) optimizados
  - 🌞 **Temporada**: Prioriza temporadas preferidas con bonus estacional mejorado
  - 🔍 **Patrón**: Analiza patrones de turnos para identificar clusters de noches y oportunidades
- **Score Inteligente Mejorado**: Combina múltiples factores con pesos optimizados
- **15 Sugerencias Diversas**: Máximo 3 por estrategia para mayor variedad
- **Aplicación Inteligente**: Funciona correctamente con rangos que cruzan meses
- **Configuración Simplificada**: Estrategia automática y cupo generoso (15 días)
- **Explicación Detallada**: Modal que explica por qué la IA sugirió esos días específicos

### 💾 **Persistencia de Datos**

- Guardado automático de preferencias
- Carga automática al iniciar la aplicación
- Indicador visual de guardado

### 📊 **Estadísticas en Tiempo Real**

- Resumen de días por tipo de turno
- Contador de vacaciones usadas/restantes

### 📤 **Exportación Avanzada**

- **ICS**: Para Google Calendar, Outlook, etc.
- **CSV**: Para RR.HH. con detalles completos
- Agrupación automática de rangos contiguos

## 🚀 Nuevas Funcionalidades

### 📅 **API de Feriados de Chile**

- **API Automática**: Carga feriados desde API oficial de Chile para años futuros (2027+)
- **Datos Locales**: Feriados 2025-2026 almacenados localmente
- **Fallback Inteligente**: Si la API falla, usa datos locales como respaldo
- **Endpoint API**: `/api/holidays/<año>` para obtener feriados específicos
- Incluye feriados nacionales, electorales y regionales

### 🔌 **API Endpoints**

#### `GET /api/holidays/<año>`

Obtiene feriados de Chile para un año específico.

**Ejemplo de respuesta:**

```json
{
  "year": 2027,
  "holidays": [
    {
      "date": "2027-01-01",
      "name": "Año Nuevo",
      "irrenunciable": true,
      "scope": "nacional"
    }
  ],
  "count": 15,
  "source": "api"
}
```

### 🎛️ **Panel de Preferencias**

- Guardado automático configurable

- Botones para guardar/cargar preferencias manualmente

### 📱 **Diseño Responsivo**

- Adaptación automática a dispositivos móviles
- Grid responsivo para estadísticas
- Botones optimizados para touch

## 🔄 **Sistema de Cálculo de Turnos**

### **Funcionamiento del Cálculo:**

El sistema calcula los turnos de la siguiente manera:

1. **Fecha de Inicio del Rango**: Se establece una fecha específica desde la cual comienza tanto el rango como el patrón
2. **Patrones Predefinidos**: Sistema de patrones comunes (2x2, 4x3, 5x2, 7x7, etc.)
3. **Tipos de Turno**: Solo Día, Solo Noche, o Mixto (alternando Día/Noche)
4. **Patrón Cíclico**: Se define un patrón que se repite indefinidamente desde el inicio del rango
5. **Sincronización Automática**: El "Inicio del patrón" se sincroniza automáticamente con el "Rango: inicio"

### **Patrones de Turnos Disponibles:**

| Patrón  | Descripción                  | Ejemplo                     |
| ------- | ---------------------------- | --------------------------- |
| **2x2** | 2 días trabajo, 2 días libre | D,D,L,L                     |
| **4x3** | 4 días trabajo, 3 días libre | D,D,D,D,L,L,L               |
| **5x2** | 5 días trabajo, 2 días libre | D,D,D,D,D,L,L               |
| **7x7** | 7 días trabajo, 7 días libre | D,D,D,D,D,D,D,L,L,L,L,L,L,L |
| **3x1** | 3 días trabajo, 1 día libre  | D,D,D,L                     |
| **6x1** | 6 días trabajo, 1 día libre  | D,D,D,D,D,D,L               |

### **Tipos de Turno:**

- **Solo Día**: Todos los días de trabajo son turno de día (D)
- **Solo Noche**: Todos los días de trabajo son turno de noche (N)
- **Mixto**: Alterna entre día y noche (D,N,D,N...)

### **Cálculo de Vacaciones:**

- **Tradicional (L-V)**: Solo lunes a viernes cuentan como días de trabajo. Sábados, domingos y feriados son libres automáticamente.
- **Según turnos**: Usa el patrón de turnos para determinar qué días son libres (L) y cuáles requieren vacaciones.
- **Todos los días**: Todos los días cuentan como trabajo, excepto feriados. Incluye fines de semana.

## 🤖 **Sistema de IA Inteligente Mejorado**

### **Estrategias de Análisis Avanzadas:**

El sistema de IA implementa 5 estrategias diferentes con algoritmos mejorados para encontrar las mejores fechas de vacaciones:

#### **🔄 Estrategia Consecutivos (Mejorada)**

- **Objetivo**: Maximizar días libres consecutivos con análisis de segmentos
- **Algoritmo**: Analiza múltiples segmentos de días libres consecutivos
- **Score**: `(Duración + Σ(segmento²) + Máximo consecutivo × 3) / Vacaciones × (1 + Ratio libre)`
- **Beneficio**: Vacaciones más largas sin interrupciones

#### **🎉 Estrategia Feriados (Mejorada)**

- **Objetivo**: Optimizar alrededor de feriados con centrado inteligente
- **Algoritmo**: Prueba múltiples posiciones alrededor de cada feriado
- **Score**: `(Duración + Feriados × 2.0 + Bonus centrado + Días libres × 0.5) / Vacaciones`
- **Beneficio**: Aprovecha feriados para extender vacaciones

#### **💪 Estrategia Trabajo (Mejorada)**

- **Objetivo**: Evitar días de trabajo difíciles con análisis de patrones
- **Algoritmo**: Prioriza evitar turnos de noche (bonus x3) y analiza secuencias
- **Score**: `(Duración + Días salvados + Bonus noches × 2 - Penalización secuencias) / Vacaciones`
- **Beneficio**: Mejor calidad de vida durante vacaciones

#### **🌉 Estrategia Puentes (Mejorada)**

- **Objetivo**: Crear puentes con fines de semana (jueves a martes)
- **Algoritmo**: Bonus para viernes/lunes (x2.0), jueves/martes (x1.0)
- **Score**: `(Duración + Bonus puentes + Conexiones fin de semana × 1.5) / Vacaciones`
- **Beneficio**: Maximiza días libres con menos vacaciones

#### **🌞 Estrategia Temporada (Nueva)**

- **Objetivo**: Priorizar temporadas preferidas
- **Algoritmo**: Bonus por temporada (Verano x2.0, Primavera x1.5, Otoño x1.0, Invierno x0.5)
- **Score**: `(Duración + Bonus temporada) / Vacaciones`
- **Beneficio**: Vacaciones en las mejores épocas del año

### **Score Inteligente Mejorado:**

El sistema combina múltiples factores con pesos optimizados:

```
Score = (Duración + Bonus Específicos + Factores Adicionales) / Vacaciones Usadas
```

- **Duración**: Número total de días en la ventana
- **Bonus Consecutivos**: Σ(segmento²) + Máximo consecutivo × 3
- **Bonus Feriados**: Feriados × 2.0 + Bonus centrado
- **Bonus Trabajo**: Días salvados + Bonus noches × 2 - Penalización secuencias
- **Bonus Puentes**: Bonus puentes + Conexiones fin de semana × 1.5
- **Bonus Temporada**: Según temporada preferida
- **Vacaciones Usadas**: Días de vacaciones necesarios

## 🎯 **Explicación Detallada de Sugerencias**

### **Modal Informativo:**

Cuando el usuario aplica una sugerencia de la IA, se muestra un modal detallado que explica:

#### **📅 Información del Período:**

- Fechas exactas de inicio y fin
- Número total de días en el período

#### **📊 Desglose de Días:**

- **Días de trabajo**: Cuántos días laborales se evitan
- **Días libres**: Días libres en el patrón de turnos
- **Feriados**: Feriados incluidos en el período
- **Fines de semana**: Días de fin de semana

#### **💼 Análisis de Turnos:**

- **Turnos de día evitados**: Número y tipo
- **Turnos de noche evitados**: Número y tipo
- **Priorización**: Se destacan los turnos más difíciles

#### **🎉 Feriados Incluidos:**

- Lista de feriados con fechas y nombres
- Beneficio adicional de cada feriado

#### **🤖 Explicación de la IA:**

- **Estrategia utilizada**: Por qué se eligió esa estrategia
- **Razón específica**: Explicación técnica de la IA
- **Beneficios**: Qué ventajas ofrece esta sugerencia

#### **📈 Eficiencia:**

- **Uso de vacaciones**: Días de vacaciones utilizados
- **Barra de eficiencia**: Porcentaje visual de días libres
- **Ratio de eficiencia**: Porcentaje de días libres vs. total

### **Ejemplo de Explicación:**

```
🎯 Explicación de Vacaciones Sugeridas

📅 Período: lunes, 25 de agosto de 2025 al viernes, 5 de septiembre de 2025
12 días totales

📊 Desglose:
┌─────────────┬─────────────┬─────────────┬─────────────┐
│ Días trabajo│ Días libres │  Feriados   │ Fines semana│
│      8      │      2      │      1      │      1      │
└─────────────┴─────────────┴─────────────┴─────────────┘

💼 Turnos que evitas:
[5 turnos de día] [3 turnos de noche]

🎉 Feriados incluidos:
25 Ago - Independencia Nacional

🤖 Por qué la IA sugirió estos días:
Esta sugerencia optimiza alrededor de 1 feriado para maximizar tus días libres.
"Optimiza 1 feriados (centrado: 2.0)"

📈 Uso de vacaciones:
Usarás 8 días de vacaciones para obtener 12 días totales
███████████████████████████████████████████████████████ 75%
Eficiencia: 75% de días libres
```

### **Comportamiento con Patrones Personalizados:**

El tipo de turno modifica automáticamente el patrón personalizado:

- **Días libres (L)**: Se mantienen igual
- **Días de trabajo (D/N)**: Se modifican según el tipo seleccionado

**Ejemplos:**

- Patrón: `D,D,L,L,N,N` + **Solo Día** = `D,D,L,L,D,D`
- Patrón: `D,D,L,L,N,N` + **Solo Noche** = `N,N,L,L,N,N`
- Patrón: `D,D,L,L,N,N` + **Mixto** = `D,N,L,L,D,N`

### **Patrones Predefinidos Mixtos:**

- **2x2 Mixto**: `D,D,L,L,N,N,L,L` (2 días + 2 libres + 2 noches + 2 libres)
- **4x3 Mixto**: `D,D,N,N,L,L,L` (2 días + 2 noches + 3 libres)
- **5x2 Mixto**: `D,D,D,N,N,L,L` (3 días + 2 noches + 2 libres)
- **7x7 Mixto**: `D,D,D,D,N,N,N,L,L,L,L,L,L,L` (4 días + 3 noches + 7 libres)
- **3x1 Mixto**: `D,D,N,L` (2 días + 1 noche + 1 libre)
- **6x1 Mixto**: `D,D,D,N,N,N,L` (3 días + 3 noches + 1 libre)

### **Ejemplo Práctico:**

**Configuración:**

- **Patrón**: `D,D,L,L,N,N,L,L,D,D,L,L` (12 días)
- **Rango de inicio**: 18 de agosto 2025 (también inicio del patrón)
- **Rango de visualización**: 18 de agosto a 31 de diciembre 2025

**Resultado:**

- **18 agosto 2025**: Día (día 0 del patrón)
- **19 agosto 2025**: Día (día 1 del patrón)
- **20 agosto 2025**: Libre (día 2 del patrón)
- **21 agosto 2025**: Libre (día 3 del patrón)
- **22 agosto 2025**: Noche (día 4 del patrón)
- **23 agosto 2025**: Noche (día 5 del patrón)
- **24 agosto 2025**: Libre (día 6 del patrón)
- **25 agosto 2025**: Libre (día 7 del patrón)

### **Lógica del Cálculo:**

```python
# Para cada día en el rango de visualización
for día in rango:
    días_desde_inicio = (día - fecha_inicio_patrón).days

    # Calcular índice cíclico en el patrón
    índice = días_desde_inicio % longitud_patrón
    turno = patrón[índice]
```

## 🛠️ Instalación y Uso

### Requisitos

- Python 3.8+
- Flask

### Instalación

```bash
# Clonar o descargar el proyecto
cd opti

# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar aplicación
python app.py
```

### Uso

1. Abrir http://localhost:5000 en el navegador
2. Configurar rango de fechas y patrón de turnos
3. Ajustar preferencias (guardado automático)
4. Generar calendario y explorar sugerencias
5. Marcar vacaciones haciendo click en los días
6. Exportar calendario en formato ICS o CSV

## 📋 APIs Disponibles

### POST `/api/build`

Genera el calendario según parámetros:

```json
{
  "start": "2025-08-22",
  "end": "2025-12-31",
  "patternStart": "2025-08-23",
  "pattern": "D,D,L,L,N,N,L,L,D,D,L,L"
}
```

### POST `/api/suggest`

Sugiere ventanas de vacaciones optimizadas usando IA inteligente:

```json
{
  "start": "2025-08-22",
  "end": "2025-12-31",
  "patternStart": "2025-08-23",
  "pattern": "D,D,L,L,N,N,L,L,D,D,L,L",
  "vacationCalculation": "traditional",
  "minWin": 7,
  "maxWin": 14
}
```

**Respuesta con estrategias de IA:**

```json
{
  "suggestions": [
    {
      "start": "2025-08-25",
      "end": "2025-09-05",
      "len": 12,
      "used": 8,
      "holCount": 1,
      "irrCount": 0,
      "score": 2.1,
      "strategy": "holiday_optimization",
      "ai_reason": "Optimiza 1 feriados (centrado: 2.0)"
    },
    {
      "start": "2025-09-15",
      "end": "2025-09-22",
      "len": 8,
      "used": 3,
      "holCount": 0,
      "irrCount": 0,
      "score": 3.2,
      "strategy": "max_consecutive",
      "ai_reason": "Maximiza 5 días libres consecutivos + 2 segmentos"
    },
    {
      "start": "2025-12-20",
      "end": "2025-12-31",
      "len": 12,
      "used": 6,
      "holCount": 2,
      "irrCount": 1,
      "score": 2.8,
      "strategy": "seasonal_optimization",
      "ai_reason": "Temporada preferida + 24.0 bonus"
    }
  ]
}
```

**Nota**: La estrategia siempre es "max_free" (maximizar días libres) y el cupo de vacaciones por defecto es 15 días.

### POST `/api/export_ics`

Exporta vacaciones en formato ICS:

```json
{
  "vacationDates": ["2025-08-25", "2025-08-26", "2025-08-27"]
}
```

### POST `/api/export_csv`

Exporta calendario completo en CSV:

```json
{
  "schedule": [...],
  "holidays": {...},
  "vacations": [...]
}
```

## 🎨 Personalización

### Temas

- **Oscuro**: Colores azules y grises oscuros
- **Claro**: Colores claros y blancos
- Transiciones suaves entre temas

### Variables CSS

```css
:root[data-theme="dark"] {
  --bg: #0f172a;
  --panel: #111827;
  --text: #e5e7eb;
  --border: #1f2937;
  --input-bg: #0b1227;
  --input-border: #374151;
}
```

## 📈 Próximas Mejoras

- [x] ✅ **IA Inteligente para Sugerencias** - Implementado
- [x] ✅ **API de Feriados de Chile** - Implementado
- [x] ✅ **Diseño Responsivo** - Implementado
- [ ] Base de datos SQLite para persistencia
- [ ] Generación de reportes PDF
- [ ] Múltiples usuarios y perfiles
- [ ] Notificaciones push para recordatorios
- [ ] Machine Learning para mejorar sugerencias basado en uso

## 🤝 Contribución

Las mejoras y sugerencias son bienvenidas. Para contribuir:

1. Fork el proyecto
2. Crear una rama para tu feature
3. Commit tus cambios
4. Push a la rama
5. Abrir un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo LICENSE para más detalles.

---

**Desarrollado con ❤️ para optimizar la planificación de turnos en Chile**
