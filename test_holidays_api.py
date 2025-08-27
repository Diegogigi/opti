#!/usr/bin/env python3
"""
Script para probar la API de feriados de Chile
"""

import requests
import json
from datetime import datetime


def test_holidays_api():
    """Prueba la API de feriados"""
    base_url = "http://127.0.0.1:5000"

    # Años a probar
    years_to_test = [2025, 2026, 2027, 2028]

    print("=== PRUEBA DE API DE FERIADOS ===")
    print()

    for year in years_to_test:
        print(f"Probando año {year}...")

        try:
            response = requests.get(f"{base_url}/api/holidays/{year}")

            if response.status_code == 200:
                data = response.json()
                print(
                    f"✅ Éxito: {data['count']} feriados obtenidos desde {data['source']}"
                )

                # Mostrar algunos feriados como ejemplo
                if data["holidays"]:
                    print("   Ejemplos de feriados:")
                    for holiday in data["holidays"][:3]:  # Solo los primeros 3
                        print(f"   - {holiday['date']}: {holiday['name']}")
                    if len(data["holidays"]) > 3:
                        print(f"   ... y {len(data['holidays']) - 3} más")
                print()
            else:
                print(f"❌ Error HTTP: {response.status_code}")
                print(f"   Respuesta: {response.text}")
                print()

        except requests.exceptions.ConnectionError:
            print(f"❌ Error: No se pudo conectar al servidor en {base_url}")
            print("   Asegúrate de que el servidor Flask esté ejecutándose")
            print()
            break
        except Exception as e:
            print(f"❌ Error inesperado: {e}")
            print()


def test_external_api():
    """Prueba la API externa de feriados de Chile"""
    print("=== PRUEBA DE API EXTERNA DE FERIADOS ===")
    print()

    try:
        # Probar con la API externa
        url = "https://apis.digital.gob.cl/fl/feriados/2027"
        response = requests.get(url, timeout=10)

        if response.status_code == 200:
            data = response.json()
            print(f"✅ API externa funcionando: {len(data)} feriados obtenidos")
            print("   Ejemplos:")
            for holiday in data[:3]:
                print(
                    f"   - {holiday.get('fecha', 'N/A')}: {holiday.get('nombre', 'N/A')}"
                )
            print()
        else:
            print(f"❌ API externa no disponible: {response.status_code}")
            print()

    except Exception as e:
        print(f"❌ Error al conectar con API externa: {e}")
        print()


if __name__ == "__main__":
    print("Iniciando pruebas de API de feriados...")
    print()

    # Probar API externa primero
    test_external_api()

    # Probar API local
    test_holidays_api()

    print("Pruebas completadas.")
