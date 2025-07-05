import requests

def get_coords(ciudad, pais):
    """
    Obtiene las coordenadas (latitud, longitud) de una ciudad en un país específico.
    """
    # Tu API key personal de Graphhopper
    api_key = "ef84eead-ab9f-4513-ae36-43854ea9b0b0"
    url = "https://graphhopper.com/api/1/geocode"
    params = {
        "q": f"{ciudad}, {pais}",
        "locale": "es",
        "limit": 1,
        "key": api_key
    }
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        if "hits" in data and len(data["hits"]) > 0:
            lat = data["hits"][0]["point"]["lat"]
            lon = data["hits"][0]["point"]["lng"]
            return f"{lat},{lon}"
        else:
            print(f"Error: No se pudieron encontrar las coordenadas para {ciudad} en {pais}.")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error de conexión al obtener coordenadas: {e}")
        return None

def main():
    """
    Función principal para calcular y mostrar la ruta entre una ciudad de Chile y una de Argentina.
    """
    transportes = {
        "auto": "car",
        "bici": "bike",
        "caminando": "foot"
    }
    # Tu API key personal de Graphhopper
    api_key = "ef84eead-ab9f-4513-ae36-43854ea9b0b0"

    while True:
        print("\n" + "="*50)
        print("CÁLCULO DE RUTA ENTRE CIUDADES DE CHILE Y ARGENTINA")
        print("="*50)
        
        # Requerimiento: Solicitar "Ciudad de Origen" y "Ciudad de Destino".
        origen = input("Ingrese la Ciudad de Origen en Chile (o 's' para salir): ").strip()
        # Requerimiento: Permitir salir con la letra 's'.
        if origen.lower() == 's':
            break

        destino = input("Ingrese la Ciudad de Destino en Argentina (o 's' para salir): ").strip()
        if destino.lower() == 's':
            break
        
        # Requerimiento: Permitir elegir tipo de medio de transporte.
        medio_transporte_usuario = input("Medio de transporte (auto, bici, caminando): ").strip().lower()
        if medio_transporte_usuario not in transportes:
            print("Transporte no válido. Por favor, elija entre 'auto', 'bici' o 'caminando'.")
            continue

        # Requerimiento: Medir la distancia entre una ciudad de Chile y una de Argentina.
        coord_origen = get_coords(origen, "Chile")
        coord_destino = get_coords(destino, "Argentina")

        if not coord_origen or not coord_destino:
            continue

        url_ruta = "https://graphhopper.com/api/1/route"
        params_ruta = {
            "point": [coord_origen, coord_destino],
            "vehicle": transportes[medio_transporte_usuario],
            "locale": "es",
            "instructions": "true",
            "key": api_key
        }

        try:
            response = requests.get(url_ruta, params=params_ruta)
            response.raise_for_status()
            data_ruta = response.json()

            if "paths" in data_ruta and len(data_ruta["paths"]) > 0:
                path = data_ruta["paths"][0]
                distancia_km = path["distance"] / 1000
                distancia_mi = distancia_km * 0.621371
                duracion_seg = path["time"] / 1000
                
                horas = int(duracion_seg // 3600)
                minutos = int((duracion_seg % 3600) // 60)
                
                print("\n--- RESULTADOS DEL VIAJE ---")
                # Requerimiento: Mostrar duración en millas, kilómetros y tiempo.
                print(f"→ Distancia: {distancia_km:.2f} km / {distancia_mi:.2f} millas")
                print(f"→ Duración estimada: {horas} horas y {minutos} minutos")
                
                # Requerimiento: Mostrar la narrativa del viaje.
                print("\n→ Narrativa del viaje:")
                for instruccion in path["instructions"]:
                    print(f"- {instruccion['text']} ({instruccion['distance']/1000:.1f} km)")
                print("--------------------------")

            else:
                print("No se pudo encontrar una ruta válida entre las ciudades especificadas.")

        except requests.exceptions.RequestException as e:
            print(f"Error al consultar la ruta: {e}")

        continuar = input("\n¿Desea realizar otra consulta? (Presione 's' para salir o cualquier otra tecla para continuar): ").strip().lower()
        if continuar == 's':
            break

if __name__ == "__main__":
    main()
