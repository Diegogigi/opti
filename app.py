from __future__ import annotations
from flask import Flask, request, jsonify, render_template, make_response
from datetime import date, datetime, timedelta
import itertools
import io
import csv
import requests
from database import (
    db,
    User,
    ShiftPattern,
    Calendar,
    Vacation,
    AISuggestion,
    Holiday,
    UserSettings,
)
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

# Inicializar la base de datos
db.init_app(app)

# ====== FERIADOS CHILE 2025 ======
# Campos: date (YYYY-MM-DD), name, irrenunciable (bool), scope: "nacional" | "electoral" | "regional:XV" | "local:chillan"
HOLIDAYS_2025 = [
    # Nacionales
    {
        "date": "2025-01-01",
        "name": "Año Nuevo",
        "irrenunciable": True,
        "scope": "nacional",
    },
    {
        "date": "2025-04-18",
        "name": "Viernes Santo",
        "irrenunciable": False,
        "scope": "nacional",
    },
    {
        "date": "2025-04-19",
        "name": "Sábado Santo",
        "irrenunciable": False,
        "scope": "nacional",
    },
    {
        "date": "2025-05-01",
        "name": "Día del Trabajo",
        "irrenunciable": True,
        "scope": "nacional",
    },
    {
        "date": "2025-05-21",
        "name": "Glorias Navales",
        "irrenunciable": False,
        "scope": "nacional",
    },
    {
        "date": "2025-06-20",
        "name": "Día de los Pueblos Indígenas",
        "irrenunciable": False,
        "scope": "nacional",
    },
    {
        "date": "2025-06-29",
        "name": "San Pedro y San Pablo",
        "irrenunciable": False,
        "scope": "nacional",
    },
    {
        "date": "2025-07-16",
        "name": "Virgen del Carmen",
        "irrenunciable": False,
        "scope": "nacional",
    },
    {
        "date": "2025-08-15",
        "name": "Asunción de la Virgen",
        "irrenunciable": False,
        "scope": "nacional",
    },
    {
        "date": "2025-09-18",
        "name": "Independencia Nacional",
        "irrenunciable": True,
        "scope": "nacional",
    },
    {
        "date": "2025-09-19",
        "name": "Glorias del Ejército",
        "irrenunciable": True,
        "scope": "nacional",
    },
    {
        "date": "2025-10-12",
        "name": "Encuentro de Dos Mundos",
        "irrenunciable": False,
        "scope": "nacional",
    },
    {
        "date": "2025-10-31",
        "name": "Día de las Iglesias Evangélicas y Protestantes",
        "irrenunciable": False,
        "scope": "nacional",
    },
    {
        "date": "2025-11-01",
        "name": "Todos los Santos",
        "irrenunciable": False,
        "scope": "nacional",
    },
    {
        "date": "2025-12-08",
        "name": "Inmaculada Concepción",
        "irrenunciable": False,
        "scope": "nacional",
    },
    {
        "date": "2025-12-25",
        "name": "Navidad",
        "irrenunciable": True,
        "scope": "nacional",
    },
    # Electorales
    {
        "date": "2025-06-29",
        "name": "Primarias Presidenciales (feriado legal)",
        "irrenunciable": False,
        "scope": "electoral",
    },
    {
        "date": "2025-11-16",
        "name": "Elección Presidencial y Parlamentaria (feriado legal)",
        "irrenunciable": False,
        "scope": "electoral",
    },
    {
        "date": "2025-12-14",
        "name": "Segunda Vuelta Presidencial (feriado legal)",
        "irrenunciable": False,
        "scope": "electoral",
    },
    # Regional / Local
    {
        "date": "2025-06-07",
        "name": "Asalto y Toma del Morro de Arica (regional)",
        "irrenunciable": False,
        "scope": "regional:XV",
    },
    {
        "date": "2025-08-20",
        "name": "Natalicio de O'Higgins (Chillán y Chillán Viejo)",
        "irrenunciable": False,
        "scope": "local:chillan",
    },
]

# ====== FERIADOS CHILE 2026 ======
HOLIDAYS_2026 = [
    # Nacionales
    {
        "date": "2026-01-01",
        "name": "Año Nuevo",
        "irrenunciable": True,
        "scope": "nacional",
    },
    {
        "date": "2026-04-03",
        "name": "Viernes Santo",
        "irrenunciable": False,
        "scope": "nacional",
    },
    {
        "date": "2026-04-04",
        "name": "Sábado Santo",
        "irrenunciable": False,
        "scope": "nacional",
    },
    {
        "date": "2026-05-01",
        "name": "Día del Trabajo",
        "irrenunciable": True,
        "scope": "nacional",
    },
    {
        "date": "2026-05-21",
        "name": "Glorias Navales",
        "irrenunciable": False,
        "scope": "nacional",
    },
    {
        "date": "2026-06-20",
        "name": "Día de los Pueblos Indígenas",
        "irrenunciable": False,
        "scope": "nacional",
    },
    {
        "date": "2026-06-29",
        "name": "San Pedro y San Pablo",
        "irrenunciable": False,
        "scope": "nacional",
    },
    {
        "date": "2026-07-16",
        "name": "Virgen del Carmen",
        "irrenunciable": False,
        "scope": "nacional",
    },
    {
        "date": "2026-08-15",
        "name": "Asunción de la Virgen",
        "irrenunciable": False,
        "scope": "nacional",
    },
    {
        "date": "2026-09-18",
        "name": "Independencia Nacional",
        "irrenunciable": True,
        "scope": "nacional",
    },
    {
        "date": "2026-09-19",
        "name": "Glorias del Ejército",
        "irrenunciable": True,
        "scope": "nacional",
    },
    {
        "date": "2026-10-12",
        "name": "Encuentro de Dos Mundos",
        "irrenunciable": False,
        "scope": "nacional",
    },
    {
        "date": "2026-10-31",
        "name": "Día de las Iglesias Evangélicas y Protestantes",
        "irrenunciable": False,
        "scope": "nacional",
    },
    {
        "date": "2026-11-01",
        "name": "Todos los Santos",
        "irrenunciable": False,
        "scope": "nacional",
    },
    {
        "date": "2026-12-08",
        "name": "Inmaculada Concepción",
        "irrenunciable": False,
        "scope": "nacional",
    },
    {
        "date": "2026-12-25",
        "name": "Navidad",
        "irrenunciable": True,
        "scope": "nacional",
    },
    # Regional / Local
    {
        "date": "2026-06-07",
        "name": "Asalto y Toma del Morro de Arica (regional)",
        "irrenunciable": False,
        "scope": "regional:XV",
    },
    {
        "date": "2026-08-20",
        "name": "Natalicio de O'Higgins (Chillán y Chillán Viejo)",
        "irrenunciable": False,
        "scope": "local:chillan",
    },
]


def get_holidays_from_api(year: int) -> list[dict]:
    """Obtiene feriados de Chile desde una API externa"""
    try:
        # Usar la API de feriados de Chile (ejemplo con una API pública)
        url = f"https://apis.digital.gob.cl/fl/feriados/{year}"
        response = requests.get(url, timeout=10)

        if response.status_code == 200:
            data = response.json()
            holidays = []

            for holiday in data:
                # Convertir formato de la API al formato interno
                holiday_date = holiday.get("fecha", "")
                if holiday_date:
                    # Convertir fecha de DD/MM/YYYY a YYYY-MM-DD
                    try:
                        day, month, year_str = holiday_date.split("/")
                        formatted_date = f"{year_str}-{month.zfill(2)}-{day.zfill(2)}"

                        holidays.append(
                            {
                                "date": formatted_date,
                                "name": holiday.get("nombre", "Feriado"),
                                "irrenunciable": holiday.get("irrenunciable", False),
                                "scope": "nacional",  # Por defecto nacional
                            }
                        )
                    except:
                        continue

            return holidays
        else:
            print(f"Error al obtener feriados para {year}: {response.status_code}")
            return []

    except Exception as e:
        print(f"Error al conectar con API de feriados para {year}: {e}")
        return []


def get_holidays_for_year(year: int) -> list[dict]:
    """Retorna los feriados para un año específico"""
    if year == 2025:
        return HOLIDAYS_2025
    elif year == 2026:
        return HOLIDAYS_2026
    elif year >= 2027:
        # Para años futuros, intentar obtener desde API
        api_holidays = get_holidays_from_api(year)
        if api_holidays:
            return api_holidays
        else:
            # Fallback: usar 2026 como base y ajustar fechas
            holidays = []
            for h in HOLIDAYS_2026:
                h_copy = h.copy()
                h_copy["date"] = h_copy["date"].replace("2026", str(year))
                holidays.append(h_copy)
            return holidays
    else:
        # Para años pasados, usar 2025 como base
        holidays = []
        for h in HOLIDAYS_2025:
            h_copy = h.copy()
            h_copy["date"] = h_copy["date"].replace("2025", str(year))
            holidays.append(h_copy)
        return holidays


def parse_iso(d: str) -> date:
    return date.fromisoformat(d)


def df(d: date) -> str:
    return d.isoformat()


def daterange(d0: date, d1: date):
    cur = d0
    while cur <= d1:
        yield cur
        cur += timedelta(days=1)


def in_scope(h: dict, scope_sel: str) -> bool:
    if scope_sel == "nacional":
        return h["scope"] == "nacional"
    if scope_sel == "nacional+electoral":
        return h["scope"] in ("nacional", "electoral")
    if scope_sel == "nacional+electoral+arica":
        return h["scope"] in ("nacional", "electoral") or h["scope"].startswith(
            "regional:XV"
        )
    if scope_sel == "nacional+electoral+chillan":
        return h["scope"] in ("nacional", "electoral") or h["scope"].startswith(
            "local:chillan"
        )
    return True


def holidays_by_date(start: str, end: str, scope_sel: str) -> dict[str, list[dict]]:
    s, e = parse_iso(start), parse_iso(end)
    out: dict[str, list[dict]] = {}

    # Obtener feriados para todos los años en el rango
    years = set(range(s.year, e.year + 1))
    all_holidays = []
    for year in years:
        all_holidays.extend(get_holidays_for_year(year))

    for h in all_holidays:
        dh = parse_iso(h["date"])
        if s <= dh <= e and in_scope(h, scope_sel):
            out.setdefault(h["date"], []).append(h)
    return out  # "YYYY-MM-DD" -> [feriados]


def expand_pattern(pat: str) -> list[str]:
    """Expande el patrón de turnos en una lista"""
    if not pat or not pat.strip():
        return ["L"]

    # Limpiar y validar el patrón
    pattern_list = []
    for x in pat.split(","):
        x = x.strip().upper()
        if x in ["L", "D", "N"]:
            pattern_list.append(x)
        elif x:  # Si hay algo que no es L, D, N, ignorarlo
            continue

    # Si no hay patrones válidos, usar "L" por defecto
    if not pattern_list:
        return ["L"]

    return pattern_list


def build_schedule(
    start: str,
    end: str,
    pattern_start: str,
    pattern_str: str,
    overrides: dict[str, str] | None = None,  # NUEVO
) -> list[dict]:
    """
    Construye el calendario de turnos hacia adelante desde la fecha de inicio del rango.

    Args:
        start: Fecha de inicio del rango a mostrar (también inicio del patrón)
        end: Fecha de fin del rango a mostrar
        pattern_start: Fecha de inicio del patrón de turnos (usado solo para compatibilidad)
        pattern_str: Patrón de turnos (ej: "D,D,L,L,N,N")

    Returns:
        Lista de días con sus turnos asignados
    """
    pat = expand_pattern(pattern_str)  # e.g. ["D","D","L","L","N","N"]
    if not pat:
        pat = ["L"]

    s, e = parse_iso(start), parse_iso(end)
    days = []

    # Validar que las fechas sean válidas
    if s > e:
        return days

    # Para cada día en el rango de visualización
    for d in daterange(s, e):
        # Calcular cuántos días han pasado desde el inicio del patrón
        pattern_start_date = parse_iso(pattern_start)
        days_since_pattern_start = (d - pattern_start_date).days

        # Cálculo hacia adelante desde el inicio del patrón
        pat_idx = days_since_pattern_start % len(pat)
        kind = pat[pat_idx]

        # Aplicar override si existe
        iso = df(d)
        if overrides and iso in overrides:
            kind = overrides[iso]  # aplicar override si existe

        days.append({"date": iso, "kind": kind})  # L | D | N

    return days


def is_weekend(d: date) -> bool:
    """Determina si una fecha es fin de semana (sábado o domingo)"""
    # weekday(): lunes=0, martes=1, ..., domingo=6
    return d.weekday() in (5, 6)  # sábado/domingo


@app.get("/")
def index():
    return render_template("index.html")


@app.post("/api/build")
def api_build():
    data = request.get_json(force=True)
    start = data.get("start")
    end = data.get("end")
    pattern_start = data.get("patternStart")
    pattern = data.get("pattern")
    overrides = data.get("overrides") or {}  # NUEVO
    scope = "nacional+electoral"  # Siempre incluir feriados nacionales y electorales
    weekend = "si"  # Siempre contar fines de semana como libres

    sched = build_schedule(start, end, pattern_start, pattern, overrides=overrides)
    hols = holidays_by_date(start, end, scope)

    # resumen
    L = D = N = H = Irr = Loc = 0
    for d in sched:
        if d["kind"] == "L":
            L += 1
        elif d["kind"] == "D":
            D += 1
        elif d["kind"] == "N":
            N += 1
        hs = hols.get(d["date"], [])
        if hs:
            H += 1
            if any(h["irrenunciable"] for h in hs):
                Irr += 1
            if any(
                h["scope"].startswith("regional") or h["scope"].startswith("local")
                for h in hs
            ):
                Loc += 1

    return jsonify(
        {
            "schedule": sched,
            "holidays": hols,
            "summary": {"L": L, "D": D, "N": N, "H": H, "Irr": Irr, "Loc": Loc},
            "useWeekend": weekend == "si",
        }
    )


@app.post("/api/suggest")
def api_suggest():
    data = request.get_json(force=True)
    start = data["start"]
    end = data["end"]
    pattern_start = data["patternStart"]
    pattern = data["pattern"]
    weekend = "si"  # Siempre contar fines de semana como libres
    scope = "nacional+electoral"  # Siempre incluir feriados nacionales y electorales
    strategy = "max_free"  # Siempre maximizar días libres
    vac_budget = int(data.get("vacBudget", 15))  # Cupo más generoso por defecto
    vacation_calculation = data.get(
        "vacationCalculation", "traditional"
    )  # Tipo de cálculo de vacaciones
    min_win = int(data.get("minWin", 7))
    max_win = int(data.get("maxWin", 14))

    overrides = data.get("overrides") or {}  # NUEVO
    sched = build_schedule(start, end, pattern_start, pattern, overrides=overrides)
    hols = holidays_by_date(start, end, scope)

    def day_is_free(day: dict) -> bool:
        d = parse_iso(day["date"])
        is_wknd = is_weekend(d)
        is_holiday = bool(hols.get(day["date"]))

        if vacation_calculation == "traditional":
            # Tradicional: solo lunes a viernes cuentan como trabajo
            return is_wknd or is_holiday
        elif vacation_calculation == "shift-based":
            # Según turnos: usar el patrón de turnos
            return day["kind"] == "L" or is_wknd or is_holiday
        elif vacation_calculation == "all-days":
            # Todos los días: solo feriados son libres
            return is_holiday
        else:
            # Por defecto: tradicional
            return is_wknd or is_holiday

    # Sistema de IA Inteligente Avanzado para Sugerencias
    def ai_analyze_vacation_opportunities():
        """IA avanzada que analiza múltiples estrategias con algoritmos optimizados"""

        # Estrategia 1: Maximizar días libres consecutivos (Optimizada)
        def strategy_max_consecutive_free():
            results = []
            n = len(sched)

            for i in range(n):
                for length in range(min_win, max_win + 1):
                    if i + length - 1 >= n:
                        break
                    window = sched[i : i + length]
                    vac_needed = 0
                    hol_count = 0
                    irr_count = 0
                    consecutive_free = 0
                    max_consecutive = 0
                    total_free_days = 0
                    free_segments = []
                    work_days_avoided = 0
                    night_shifts_avoided = 0

                    # Analizar segmentos de días libres consecutivos
                    current_segment = 0
                    for day in window:
                        hs = hols.get(day["date"], [])
                        if not day_is_free(day):
                            vac_needed += 1
                            work_days_avoided += 1
                            if day["kind"] == "N":
                                night_shifts_avoided += 1
                            if current_segment > 0:
                                free_segments.append(current_segment)
                                current_segment = 0
                        else:
                            consecutive_free += 1
                            current_segment += 1
                            total_free_days += 1
                            max_consecutive = max(max_consecutive, consecutive_free)

                        if hs:
                            hol_count += 1
                            if any(h["irrenunciable"] for h in hs):
                                irr_count += 1

                    # Agregar el último segmento si existe
                    if current_segment > 0:
                        free_segments.append(current_segment)

                    if vac_needed <= vac_budget and vac_needed > 0:
                        # Score mejorado con múltiples factores
                        segment_bonus = sum(
                            seg * seg * seg for seg in free_segments
                        )  # Cúbico para preferir segmentos largos
                        free_ratio = total_free_days / length
                        efficiency_bonus = (
                            length - vac_needed
                        ) / length  # Eficiencia de vacaciones
                        night_shift_bonus = (
                            night_shifts_avoided * 2
                        )  # Bonus por evitar noches

                        score = (
                            (
                                length * 2
                                + segment_bonus
                                + max_consecutive * 4
                                + night_shift_bonus
                            )
                            / max(1, vac_needed)
                            * (1 + free_ratio + efficiency_bonus)
                        )

                        results.append(
                            {
                                "start": window[0]["date"],
                                "end": window[-1]["date"],
                                "len": length,
                                "used": vac_needed,
                                "holCount": hol_count,
                                "irrCount": irr_count,
                                "score": round(score, 2),
                                "strategy": "max_consecutive",
                                "ai_reason": f"Maximiza {max_consecutive} días libres consecutivos + {len(free_segments)} segmentos + evita {night_shifts_avoided} noches",
                            }
                        )

            return results

        # Estrategia 2: Optimizar alrededor de feriados (Optimizada)
        def strategy_holiday_optimization():
            results = []
            n = len(sched)

            # Encontrar feriados en el rango
            holiday_dates = set()
            for day in sched:
                if hols.get(day["date"]):
                    holiday_dates.add(day["date"])

            for holiday_date in holiday_dates:
                # Buscar ventanas que incluyan el feriado
                holiday_idx = next(
                    i for i, d in enumerate(sched) if d["date"] == holiday_date
                )

                for length in range(min_win, max_win + 1):
                    # Probar múltiples posiciones alrededor del feriado
                    for offset in range(-length // 2, length // 2 + 1):
                        start_idx = max(0, holiday_idx + offset)
                        end_idx = min(n - 1, start_idx + length - 1)

                        if end_idx - start_idx + 1 < min_win:
                            continue

                        window = sched[start_idx : end_idx + 1]
                        vac_needed = 0
                        hol_count = 0
                        irr_count = 0
                        holiday_center_bonus = 0
                        work_days_around_holiday = 0
                        night_shifts_around_holiday = 0

                        for j, day in enumerate(window):
                            hs = hols.get(day["date"], [])
                            if not day_is_free(day):
                                vac_needed += 1
                                work_days_around_holiday += 1
                                if day["kind"] == "N":
                                    night_shifts_around_holiday += 1
                            if hs:
                                hol_count += 1
                                if any(h["irrenunciable"] for h in hs):
                                    irr_count += 1
                                # Bonus extra si el feriado está en el centro de la ventana
                                if day["date"] == holiday_date:
                                    center_distance = abs(j - length // 2)
                                    holiday_center_bonus = (
                                        max(0, 5 - center_distance) * 2
                                    )

                        if vac_needed <= vac_budget and vac_needed > 0:
                            # Score mejorado con múltiples factores
                            holiday_bonus = hol_count * 3.0 + holiday_center_bonus
                            free_days = length - vac_needed
                            efficiency_bonus = (length - vac_needed) / length
                            night_shift_bonus = night_shifts_around_holiday * 2

                            score = (
                                (
                                    length * 1.5
                                    + holiday_bonus
                                    + free_days
                                    + night_shift_bonus
                                )
                                / max(1, vac_needed)
                                * (1 + efficiency_bonus)
                            )

                            results.append(
                                {
                                    "start": window[0]["date"],
                                    "end": window[-1]["date"],
                                    "len": length,
                                    "used": vac_needed,
                                    "holCount": hol_count,
                                    "irrCount": irr_count,
                                    "score": round(score, 2),
                                    "strategy": "holiday_optimization",
                                    "ai_reason": f"Optimiza {hol_count} feriados (centrado: {holiday_center_bonus:.1f}) + evita {night_shifts_around_holiday} noches",
                                }
                            )

            return results

        # Estrategia 3: Minimizar días de trabajo sacrificados (Optimizada)
        def strategy_minimize_work_loss():
            results = []
            n = len(sched)

            for i in range(n):
                for length in range(min_win, max_win + 1):
                    if i + length - 1 >= n:
                        break
                    window = sched[i : i + length]
                    vac_needed = 0
                    hol_count = 0
                    irr_count = 0
                    work_days_saved = 0
                    night_shifts_avoided = 0
                    day_shifts_avoided = 0
                    consecutive_work_penalty = 0
                    weekend_connections = 0

                    # Analizar patrones de trabajo
                    for j, day in enumerate(window):
                        hs = hols.get(day["date"], [])
                        if not day_is_free(day):
                            vac_needed += 1
                            # Bonus por evitar días de trabajo difíciles
                            if day["kind"] == "N":  # Turno de noche
                                work_days_saved += 4  # Más peso a turnos de noche
                                night_shifts_avoided += 1
                            elif day["kind"] == "D":  # Turno de día
                                work_days_saved += 1
                                day_shifts_avoided += 1

                            # Bonus por conectar con fines de semana
                            d = parse_iso(day["date"])
                            if d.weekday() in [4, 0]:  # Viernes o Lunes
                                weekend_connections += 1

                            # Penalizar secuencias largas de trabajo
                            if j > 0 and not day_is_free(window[j - 1]):
                                consecutive_work_penalty += 0.3
                        if hs:
                            hol_count += 1
                            if any(h["irrenunciable"] for h in hs):
                                irr_count += 1

                    if vac_needed <= vac_budget and vac_needed > 0:
                        # Score mejorado con análisis de patrones
                        base_score = length * 1.5 + work_days_saved
                        pattern_bonus = (
                            night_shifts_avoided * 3
                        )  # Bonus extra por evitar noches
                        weekend_bonus = weekend_connections * 2  # Bonus por puentes
                        efficiency_bonus = (length - vac_needed) / length

                        final_score = (
                            (
                                base_score
                                + pattern_bonus
                                + weekend_bonus
                                - consecutive_work_penalty
                            )
                            / max(1, vac_needed)
                            * (1 + efficiency_bonus)
                        )

                        results.append(
                            {
                                "start": window[0]["date"],
                                "end": window[-1]["date"],
                                "len": length,
                                "used": vac_needed,
                                "holCount": hol_count,
                                "irrCount": irr_count,
                                "score": round(final_score, 2),
                                "strategy": "minimize_work_loss",
                                "ai_reason": f"Evita {night_shifts_avoided} noches + {day_shifts_avoided} días + {weekend_connections} puentes",
                            }
                        )

            return results

        # Estrategia 4: Optimización de puentes (Mejorada)
        def strategy_bridge_optimization():
            results = []
            n = len(sched)

            for i in range(n):
                for length in range(min_win, max_win + 1):
                    if i + length - 1 >= n:
                        break
                    window = sched[i : i + length]
                    vac_needed = 0
                    hol_count = 0
                    irr_count = 0
                    bridge_bonus = 0
                    weekend_connections = 0

                    for j, day in enumerate(window):
                        hs = hols.get(day["date"], [])
                        d = parse_iso(day["date"])

                        if not day_is_free(day):
                            vac_needed += 1
                            # Bonus por crear puentes
                            if d.weekday() == 4:  # Viernes
                                bridge_bonus += 2.0
                                weekend_connections += 1
                            elif d.weekday() == 0:  # Lunes
                                bridge_bonus += 2.0
                                weekend_connections += 1
                            elif d.weekday() == 3:  # Jueves
                                bridge_bonus += 1.0
                            elif d.weekday() == 1:  # Martes
                                bridge_bonus += 1.0
                        if hs:
                            hol_count += 1
                            if any(h["irrenunciable"] for h in hs):
                                irr_count += 1

                    if vac_needed <= vac_budget:
                        # Score mejorado con análisis de conexiones de fin de semana
                        bridge_score = (
                            length + bridge_bonus + weekend_connections * 1.5
                        ) / max(1, vac_needed)
                        results.append(
                            {
                                "start": window[0]["date"],
                                "end": window[-1]["date"],
                                "len": length,
                                "used": vac_needed,
                                "holCount": hol_count,
                                "irrCount": irr_count,
                                "score": round(bridge_score, 2),
                                "strategy": "bridge_optimization",
                                "ai_reason": f"Crea {weekend_connections} puentes + {bridge_bonus:.1f} bonus",
                            }
                        )

            return results

        # Estrategia 5: Optimización de temporadas (Optimizada)
        def strategy_seasonal_optimization():
            results = []
            n = len(sched)

            # Definir temporadas preferidas (verano, navidad, etc.)
            def get_season_bonus(date_str):
                d = parse_iso(date_str)
                month = d.month

                # Verano (diciembre - febrero)
                if month in [12, 1, 2]:
                    return 3.0
                # Primavera (septiembre - noviembre)
                elif month in [9, 10, 11]:
                    return 2.0
                # Otoño (marzo - mayo)
                elif month in [3, 4, 5]:
                    return 1.5
                # Invierno (junio - agosto)
                else:
                    return 1.0

            for i in range(n):
                for length in range(min_win, max_win + 1):
                    if i + length - 1 >= n:
                        break
                    window = sched[i : i + length]
                    vac_needed = 0
                    hol_count = 0
                    irr_count = 0
                    seasonal_bonus = 0

                    for day in window:
                        hs = hols.get(day["date"], [])
                        if not day_is_free(day):
                            vac_needed += 1
                            seasonal_bonus += get_season_bonus(day["date"])
                        if hs:
                            hol_count += 1
                            if any(h["irrenunciable"] for h in hs):
                                irr_count += 1

                    if vac_needed <= vac_budget:
                        # Score con bonus de temporada
                        seasonal_score = (length + seasonal_bonus) / max(1, vac_needed)
                        results.append(
                            {
                                "start": window[0]["date"],
                                "end": window[-1]["date"],
                                "len": length,
                                "used": vac_needed,
                                "holCount": hol_count,
                                "irrCount": irr_count,
                                "score": round(seasonal_score, 2),
                                "strategy": "seasonal_optimization",
                                "ai_reason": f"Temporada preferida + {seasonal_bonus:.1f} bonus",
                            }
                        )

            return results

        # Estrategia 6: Análisis inteligente de patrones de turnos (Optimizada)
        def strategy_pattern_analysis():
            results = []
            n = len(sched)
            date_to_idx = {
                d["date"]: i for i, d in enumerate(sched)
            }  # NUEVO: O(1) lookup

            # Analizar el patrón de turnos para identificar oportunidades
            def analyze_shift_pattern():
                pattern_analysis = {
                    "night_clusters": [],  # Grupos de noches consecutivas
                    "day_clusters": [],  # Grupos de días consecutivos
                    "free_gaps": [],  # Espacios libres entre trabajo
                    "work_streaks": [],  # Racha de trabajo
                }

                current_cluster = {"type": None, "start": 0, "length": 0}

                for i, day in enumerate(sched):
                    if day["kind"] == "L":
                        # Si hay un cluster activo, finalizarlo
                        if current_cluster["type"]:
                            cluster_key = (
                                "night_clusters"
                                if current_cluster["type"] == "N"
                                else "day_clusters"
                            )
                            pattern_analysis[cluster_key].append(
                                {
                                    "start": current_cluster["start"],
                                    "end": i - 1,
                                    "length": current_cluster["length"],
                                }
                            )
                            current_cluster = {"type": None, "start": 0, "length": 0}
                    else:
                        # Es un día de trabajo
                        if current_cluster["type"] == day["kind"]:
                            # Continuar cluster
                            current_cluster["length"] += 1
                        else:
                            # Finalizar cluster anterior y comenzar nuevo
                            if current_cluster["type"]:
                                cluster_key = (
                                    "night_clusters"
                                    if current_cluster["type"] == "N"
                                    else "day_clusters"
                                )
                                pattern_analysis[cluster_key].append(
                                    {
                                        "start": current_cluster["start"],
                                        "end": i - 1,
                                        "length": current_cluster["length"],
                                    }
                                )
                            current_cluster = {
                                "type": day["kind"],
                                "start": i,
                                "length": 1,
                            }

                # Finalizar último cluster si existe
                if current_cluster["type"]:
                    cluster_key = (
                        "night_clusters"
                        if current_cluster["type"] == "N"
                        else "day_clusters"
                    )
                    pattern_analysis[cluster_key].append(
                        {
                            "start": current_cluster["start"],
                            "end": n - 1,
                            "length": current_cluster["length"],
                        }
                    )

                return pattern_analysis

            pattern_data = analyze_shift_pattern()

            # Buscar oportunidades basadas en el análisis de patrones
            for night_cluster in pattern_data["night_clusters"]:
                if night_cluster["length"] >= 2:  # Solo clusters de 2+ noches
                    # Buscar ventanas que incluyan este cluster
                    cluster_start = night_cluster["start"]
                    cluster_end = night_cluster["end"]

                    for length in range(min_win, max_win + 1):
                        # Probar diferentes posiciones alrededor del cluster
                        for offset in range(-length // 3, length // 3 + 1):
                            start_idx = max(0, cluster_start + offset)
                            end_idx = min(n - 1, start_idx + length - 1)

                            if end_idx - start_idx + 1 < min_win:
                                continue

                            window = sched[start_idx : end_idx + 1]
                            vac_needed = 0
                            hol_count = 0
                            irr_count = 0
                            night_shifts_in_window = 0
                            cluster_coverage = 0

                            for day in window:
                                hs = hols.get(day["date"], [])
                                if not day_is_free(day):
                                    vac_needed += 1
                                    if day["kind"] == "N":
                                        night_shifts_in_window += 1
                                        # Verificar si está en el cluster original
                                        day_idx = date_to_idx[day["date"]]  # O(1)
                                        if cluster_start <= day_idx <= cluster_end:
                                            cluster_coverage += 1
                                if hs:
                                    hol_count += 1
                                    if any(h["irrenunciable"] for h in hs):
                                        irr_count += 1

                            if (
                                vac_needed <= vac_budget
                                and vac_needed > 0
                                and cluster_coverage > 0
                            ):
                                # Score basado en cobertura del cluster y eficiencia
                                cluster_bonus = (
                                    cluster_coverage * 3
                                )  # Bonus por cubrir noches del cluster
                                efficiency_bonus = (length - vac_needed) / length
                                night_avoidance_bonus = night_shifts_in_window * 2

                                score = (
                                    (
                                        length * 1.5
                                        + cluster_bonus
                                        + night_avoidance_bonus
                                    )
                                    / max(1, vac_needed)
                                    * (1 + efficiency_bonus)
                                )

                                results.append(
                                    {
                                        "start": window[0]["date"],
                                        "end": window[-1]["date"],
                                        "len": length,
                                        "used": vac_needed,
                                        "holCount": hol_count,
                                        "irrCount": irr_count,
                                        "score": round(score, 2),
                                        "strategy": "pattern_analysis",
                                        "ai_reason": f"Analiza patrón: cubre {cluster_coverage}/{night_cluster['length']} noches del cluster",
                                    }
                                )

            return results

        # Combinar todas las estrategias
        all_results = []
        all_results.extend(strategy_max_consecutive_free())
        all_results.extend(strategy_holiday_optimization())
        all_results.extend(strategy_minimize_work_loss())
        all_results.extend(strategy_bridge_optimization())
        all_results.extend(strategy_seasonal_optimization())
        all_results.extend(strategy_pattern_analysis())

        # Eliminar duplicados y ordenar con algoritmo mejorado
        unique_results = {}
        for result in all_results:
            key = (result["start"], result["end"])
            if key not in unique_results:
                unique_results[key] = result
            else:
                # Si ya existe, mantener el de mayor score o el más diverso
                existing = unique_results[key]
                if result["score"] > existing["score"]:
                    unique_results[key] = result
                elif (
                    result["score"] == existing["score"]
                    and result["strategy"] != existing["strategy"]
                ):
                    # Si tienen el mismo score pero diferente estrategia, mantener ambos
                    unique_results[f"{key}_alt"] = result

        final_results = list(unique_results.values())

        # Ordenar por score y diversidad de estrategias
        final_results.sort(key=lambda r: (r["score"], r["len"]), reverse=True)

        # Asegurar diversidad: máximo 3 por estrategia en los primeros 15
        diverse_results = []
        strategy_counts = {}

        for result in final_results:
            strategy = result["strategy"]
            if strategy not in strategy_counts:
                strategy_counts[strategy] = 0

            if strategy_counts[strategy] < 3:
                diverse_results.append(result)
                strategy_counts[strategy] += 1

            if len(diverse_results) >= 15:
                break

        return diverse_results

    # Usar el sistema de IA
    results = ai_analyze_vacation_opportunities()

    return jsonify({"suggestions": results})


@app.post("/api/export_ics")
def api_export_ics():
    """
    Recibe JSON: { "vacationDates": ["YYYY-MM-DD", ...] }
    Devuelve un ICS con eventos all-day agrupados por rangos contiguos.
    """
    data = request.get_json(force=True)
    dates = sorted(set(data.get("vacationDates", [])))
    if not dates:
        return jsonify({"error": "No hay fechas seleccionadas"}), 400

    # Agrupar contiguos
    def iso_to_date(s: str) -> date:
        return parse_iso(s)

    chunks = []
    for k, group in itertools.groupby(
        enumerate([iso_to_date(x) for x in dates]),
        key=lambda t: t[0] - (t[1] - iso_to_date(dates[0])).days,
    ):
        g = [d for _, d in group]
        chunks.append((g[0], g[-1]))

    lines = ["BEGIN:VCALENDAR", "VERSION:2.0", "PRODID:-//Planificador Turnos CL//ES"]
    now = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")

    def next_day(d: date) -> date:
        return d + timedelta(days=1)

    for a, b in chunks:
        dt_start = a.strftime("%Y%m%d")
        dt_end = next_day(b).strftime("%Y%m%d")  # all-day end exclusive
        uid = f"vac-{dt_start}-{dt_end}@turnos-app"
        lines.extend(
            [
                "BEGIN:VEVENT",
                f"UID:{uid}",
                f"DTSTAMP:{now}",
                f"DTSTART;VALUE=DATE:{dt_start}",
                f"DTEND;VALUE=DATE:{dt_end}",
                "SUMMARY:Vacaciones",
                "END:VEVENT",
            ]
        )
    lines.append("END:VCALENDAR")

    ics_bytes = ("\r\n".join(lines)).encode("utf-8")
    resp = make_response(ics_bytes)
    resp.headers["Content-Type"] = "text/calendar; charset=utf-8"
    resp.headers["Content-Disposition"] = 'attachment; filename="vacaciones.ics"'
    return resp


@app.post("/api/export_csv")
def api_export_csv():
    """
    Recibe JSON: { "schedule": [...], "holidays": {...}, "vacations": [...] }
    Devuelve un CSV con el calendario completo para RR.HH.
    """
    data = request.get_json(force=True)
    schedule = data.get("schedule", [])
    holidays = data.get("holidays", {})
    vacations = set(data.get("vacations", []))

    if not schedule:
        return jsonify({"error": "No hay datos de calendario"}), 400

    # Crear CSV en memoria
    output = io.StringIO()
    writer = csv.writer(output)

    # Headers
    writer.writerow(
        [
            "Fecha",
            "Día Semana",
            "Tipo Turno",
            "Feriados",
            "Vacaciones",
            "Horas Trabajo",
        ]
    )

    # Mapeo de días de la semana en español
    DOW_ES = ["lunes", "martes", "miércoles", "jueves", "viernes", "sábado", "domingo"]

    # Datos
    for day in schedule:
        date_obj = parse_iso(day["date"])
        dow = DOW_ES[date_obj.weekday()]  # Nombre del día en español
        turno = {"L": "Libre", "D": "Día", "N": "Noche"}.get(day["kind"], "Libre")

        # Feriados
        day_holidays = holidays.get(day["date"], [])
        holiday_names = (
            ", ".join([h["name"] for h in day_holidays]) if day_holidays else ""
        )

        # Vacaciones
        is_vacation = day["date"] in vacations

        # Horas de trabajo
        hours = 0
        if day["kind"] == "D":
            hours = 8
        elif day["kind"] == "N":
            hours = 12

        writer.writerow(
            [
                day["date"],
                dow.capitalize(),
                turno,
                holiday_names,
                "Sí" if is_vacation else "No",
                hours,
            ]
        )

    csv_bytes = output.getvalue().encode("utf-8")
    resp = make_response(csv_bytes)
    resp.headers["Content-Type"] = "text/csv; charset=utf-8"
    resp.headers["Content-Disposition"] = 'attachment; filename="turnos_vacaciones.csv"'
    return resp


@app.get("/api/holidays/<int:year>")
def api_get_holidays(year: int):
    """Endpoint para obtener feriados de un año específico"""
    try:
        source = "local"
        holidays = get_holidays_for_year(year)
        if year >= 2027:
            api_h = get_holidays_from_api(year)
            if api_h:
                holidays = api_h
                source = "api"
            else:
                source = "local-fallback"
        return jsonify(
            {
                "year": year,
                "holidays": holidays,
                "count": len(holidays),
                "source": source,
            }
        )
    except Exception as e:
        return (
            jsonify({"error": f"Error al obtener feriados para {year}: {str(e)}"}),
            500,
        )


# ====== ENDPOINTS DE BASE DE DATOS ======


@app.post("/api/user/register")
def api_register_user():
    """Registrar nuevo usuario"""
    try:
        data = request.get_json(force=True)
        email = data.get("email")
        name = data.get("name")
        company = data.get("company", "")
        position = data.get("position", "")

        if not email or not name:
            return jsonify({"error": "Email y nombre son requeridos"}), 400

        # Verificar si el usuario ya existe
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            return jsonify({"error": "El usuario ya existe"}), 409

        # Crear nuevo usuario
        user = User(email=email, name=name, company=company, position=position)
        db.session.add(user)
        db.session.commit()

        # Crear configuración por defecto
        settings = UserSettings(user_id=user.id)
        db.session.add(settings)
        db.session.commit()

        return jsonify(
            {
                "success": True,
                "user_id": user.id,
                "message": "Usuario registrado correctamente",
            }
        )

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Error al registrar usuario: {str(e)}"}), 500


@app.post("/api/user/login")
def api_login_user():
    """Login de usuario por email"""
    try:
        data = request.get_json(force=True)
        email = data.get("email")

        if not email:
            return jsonify({"error": "Email es requerido"}), 400

        # Buscar usuario
        user = User.query.filter_by(email=email).first()
        if not user:
            return jsonify({"error": "Usuario no encontrado"}), 404

        # Actualizar último acceso
        user.last_access = datetime.utcnow()
        db.session.commit()

        return jsonify(
            {
                "success": True,
                "user": {
                    "id": user.id,
                    "email": user.email,
                    "name": user.name,
                    "company": user.company,
                    "position": user.position,
                },
            }
        )

    except Exception as e:
        return jsonify({"error": f"Error en login: {str(e)}"}), 500


@app.post("/api/pattern/save")
def api_save_pattern():
    """Guardar patrón de turnos"""
    try:
        data = request.get_json(force=True)
        user_id = data.get("user_id")
        name = data.get("name")
        pattern = data.get("pattern")
        shift_type = data.get("shift_type")
        description = data.get("description", "")

        if not all([user_id, name, pattern, shift_type]):
            return jsonify({"error": "Todos los campos son requeridos"}), 400

        # Crear nuevo patrón
        shift_pattern = ShiftPattern(
            user_id=user_id,
            name=name,
            pattern=pattern,
            shift_type=shift_type,
            description=description,
        )
        db.session.add(shift_pattern)
        db.session.commit()

        return jsonify(
            {
                "success": True,
                "pattern_id": shift_pattern.id,
                "message": "Patrón guardado correctamente",
            }
        )

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Error al guardar patrón: {str(e)}"}), 500


@app.get("/api/patterns/<int:user_id>")
def api_get_patterns(user_id):
    """Obtener patrones de un usuario"""
    try:
        patterns = ShiftPattern.query.filter_by(user_id=user_id, is_active=True).all()

        return jsonify(
            {
                "success": True,
                "patterns": [
                    {
                        "id": p.id,
                        "name": p.name,
                        "pattern": p.pattern,
                        "shift_type": p.shift_type,
                        "description": p.description,
                        "created_at": p.created_at.isoformat(),
                    }
                    for p in patterns
                ],
            }
        )

    except Exception as e:
        return jsonify({"error": f"Error al obtener patrones: {str(e)}"}), 500


@app.post("/api/vacation/save")
def api_save_vacation():
    """Guardar vacación"""
    try:
        data = request.get_json(force=True)
        user_id = data.get("user_id")
        start_date = data.get("start_date")
        end_date = data.get("end_date")
        days_used = data.get("days_used")
        calculation_type = data.get("calculation_type", "traditional")
        notes = data.get("notes", "")

        if not all([user_id, start_date, end_date, days_used]):
            return jsonify({"error": "Campos requeridos faltantes"}), 400

        # Crear nueva vacación
        vacation = Vacation(
            user_id=user_id,
            start_date=datetime.strptime(start_date, "%Y-%m-%d").date(),
            end_date=datetime.strptime(end_date, "%Y-%m-%d").date(),
            days_used=days_used,
            calculation_type=calculation_type,
            notes=notes,
        )
        db.session.add(vacation)
        db.session.commit()

        return jsonify(
            {
                "success": True,
                "vacation_id": vacation.id,
                "message": "Vacación guardada correctamente",
            }
        )

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Error al guardar vacación: {str(e)}"}), 500


@app.get("/api/vacations/<int:user_id>")
def api_get_vacations(user_id):
    """Obtener vacaciones de un usuario"""
    try:
        vacations = (
            Vacation.query.filter_by(user_id=user_id)
            .order_by(Vacation.start_date.desc())
            .all()
        )

        return jsonify(
            {
                "success": True,
                "vacations": [
                    {
                        "id": v.id,
                        "start_date": v.start_date.isoformat(),
                        "end_date": v.end_date.isoformat(),
                        "days_used": v.days_used,
                        "calculation_type": v.calculation_type,
                        "status": v.status,
                        "notes": v.notes,
                        "created_at": v.created_at.isoformat(),
                    }
                    for v in vacations
                ],
            }
        )

    except Exception as e:
        return jsonify({"error": f"Error al obtener vacaciones: {str(e)}"}), 500


if __name__ == "__main__":
    app.run(debug=True)
