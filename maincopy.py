import requests
import csv

# Leer la lista de SMPs desde el archivo de texto
with open("smps.txt", "r") as file:
    smps_list = file.read().splitlines()

with open("datos.csv", "a", newline="") as csvfile:
    fieldnames = [
    "direccion",
    "smp",
    "seccion",
    "manzana",
    "parcela",
    "centroide",
    "srid",
    "smp_anterior",
    "smp_siguiente",
    "pdamatriz",
    "superficie_total",
    "superficie_cubierta",
    "frente",
    "fondo",
    "propiedad_horizontal",
    "pisos_bajo_rasante",
    "pisos_sobre_rasante",
    "unidades_funcionales",
    "locales",
    "vuc",
    "fuente",
    "cantidad_puertas",
    "sup_max_edificable",
    "sup_edificable_planta",
    "altura_max",
    "altura_max_plano_limite",
    "unidad_edificabilidad",
    "plusvalia_em",
    "plusvalia_pl",
    "plusvalia_sl",
    "incidencia_uva",
    "alicuota",
    "distrito_cpu",
    "fot_medianera",
    "fot_perim_libre",
    "fot_semi_libre",
    "fot_em_2",
    "fot_pl_2",
    "fot_sl_2",
    "smp_linderas",
    "aph_linderas",
    "rivolta",
    "denominacion",
    "proteccion",
    "estado",
    "ley_3056",
    "catalogacion",
    "distrito_agrupado",
    "distrito_especifico",
    "tipica",
    "riesgo_hidrico",
    "lep",
    "ensanche",
    "apertura",
    "ci_digital",
    "subzona",
    "croquis_parcela",
    "perimetro_manzana",
    "plano_indice",
    "disposicio",
    "pdf",
    "irregular",
    "superficie_parcela",
    "adps",
    "memo",
    "microcentr",
    "puertasesq",
    ]

    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    
    # Escribir los encabezados del CSV
    writer.writeheader()

    # Iterar sobre la lista de SMPs y procesar cada uno
    for smp in smps_list:
        # Generar las URLs dinámicamente para cada SMP
        url_1 = f"https://datosabiertos-catastro-apis.buenosaires.gob.ar/catastro/parcela/?smp={smp}"
        url_2 = f"https://epok.buenosaires.gob.ar/cur3d/seccion_edificabilidad/?smp={smp}"

        # Realizar solicitudes HTTP para obtener los datos JSON
        print(f"Procesando SMP: {smp}")
        
        response_1 = requests.get(url_1)
        print(f"  Estado de URL 1 ({url_1}): {response_1.status_code}")
        
        response_2 = requests.get(url_2)
        print(f"  Estado de URL 2 ({url_2}): {response_2.status_code}")

        # Convertir los datos JSON en diccionarios
        try:
            data_1 = response_1.json()
            data_2 = response_2.json()
        except requests.exceptions.JSONDecodeError:
            print(f"  No se pudo decodificar JSON para SMP {smp}")
            continue  # Salta a la siguiente iteración si hay un problema con el JSON

        # Obtener el centroide de data_1
        centroide = data_1.get("centroide", None)

        # Formatear el centroide para incluirlo en la URL
        x, y = centroide
        x_str = str(x)
        y_str = str(y)

        # Construir la nueva URL con el centroide formateado
        url_3 = f"https://epok.buenosaires.gob.ar/catastro/parcela/?callback=&x={x_str}&y={y_str}"

        # Realizar la solicitud HTTP para la nueva URL
        response_nueva = requests.get(url_3)
        print(f"  Estado de URL 3 ({url_3}): {response_nueva.status_code}")

        # Verificar si la solicitud fue exitosa antes de intentar convertir la respuesta a JSON
        if response_nueva.status_code == 200:
            # Convertir los datos JSON de la nueva solicitud en un diccionario
            data_3 = response_nueva.json()

            # Obtener la información de las puertas de data_3
            puertas_info_3 = data_3.get("puertas", [])

            # Mapear los campos, verificando la presencia de las claves en data_1 y data_2
            mapped_data = {
                "direccion": f'"{data_1.get("direccion", None)}"',  # Encerrar el valor entre comillas dobles
                "smp": data_1.get("smp", None),
                "seccion": data_1.get("seccion", None),
                "manzana": data_1.get("manzana", None),
                "parcela": data_1.get("parcela", None),
                "centroide": data_1.get("centroide", None),
                "srid": data_1.get("srid", None),
                "smp_anterior": data_1.get("smp_anterior", None),
                "smp_siguiente": data_1.get("smp_siguiente", None),
                "pdamatriz": data_1.get("pdamatriz", None),
                "superficie_total": data_1.get("superficie_total", None),
                "superficie_cubierta": data_1.get("superficie_cubierta", None),
                "frente": data_1.get("frente", None),
                "fondo": data_1.get("fondo", None),
                "propiedad_horizontal": data_1.get("propiedad_horizontal", None),
                "pisos_bajo_rasante": data_1.get("pisos_bajo_rasante", None),
                "pisos_sobre_rasante": data_1.get("pisos_sobre_rasante", None),
                "unidades_funcionales": data_1.get("unidades_funcionales", None),
                "locales": data_1.get("locales", None),
                "vuc": data_1.get("vuc", None),
                "fuente": data_1.get("fuente", None),
                "cantidad_puertas": data_1.get("cantidad_puertas", None),
                "sup_max_edificable": data_2.get("sup_max_edificable", None),
                "sup_edificable_planta": data_2.get("sup_edificable_planta", None),
                "altura_max": data_2.get("altura_max", None),
                "altura_max_plano_limite": data_2.get("altura_max_plano_limite", None),
                "unidad_edificabilidad": data_2.get("unidad_edificabilidad", None),
                "plusvalia_em": data_2.get("plusvalia_em", None),
                "plusvalia_pl": data_2.get("plusvalia_pl", None),
                "plusvalia_sl": data_2.get("plusvalia_sl", None),
                "incidencia_uva": data_2.get("incidencia_uva", None),
                "alicuota": data_2.get("alicuota", None),
                "distrito_cpu": data_2.get("distrito_cpu", None),
                "fot_medianera": data_2.get("fot_medianera", None),
                "fot_perim_libre": data_2.get("fot_perim_libre", None),
                "fot_semi_libre": data_2.get("fot_semi_libre", None),
                "fot_em_2": data_2.get("fot_em_2", None),
                "fot_pl_2": data_2.get("fot_pl_2", None),
                "fot_sl_2": data_2.get("fot_sl_2", None),   
                "smp_linderas": ", ".join(data_2.get("parcelas_linderas", {}).get("smp_linderas", [])),
                "aph_linderas": data_2.get("aph_linderas", None),
                "rivolta": data_2.get("rivolta", None),
                "denominacion": data_2.get("denominacion", None),
                "proteccion": data_2.get("proteccion", None),
                "estado": data_2.get("estado", None),
                "ley_3056": data_2.get("ley_3056", None),
                "catalogacion": data_2.get("catalogacion", None),
                "distrito_agrupado": data_2.get("distrito_agrupado", None),
                "distrito_especifico": data_2.get("distrito_especifico", None),
                "tipica": data_2.get("tipica", None),
                "riesgo_hidrico": data_2.get("riesgo_hidrico", None),
                "lep": data_2.get("lep", None),
                "ensanche": data_2.get("ensanche", None),
                "apertura": data_2.get("apertura", None),
                "ci_digital": data_2.get("ci_digital", None),
                "subzona": data_2.get("subzona", None),
                "croquis_parcela": data_2.get("croquis_parcela", None),
                "perimetro_manzana": data_2.get("perimetro_manzana", None),
                "plano_indice": data_2.get("plano_indice", None),
                "disposicio": data_2.get("disposicio", None),
                "pdf": data_2.get("pdf", None),
                "irregular": data_2.get("irregular", None),
                "superficie_parcela": data_2.get("superficie_parcela", None),
                "adps": data_2.get("adps", None),
                "memo": data_2.get("memo", None),
                "microcentr": data_2.get("microcentr", None),
                "puertasesq": ", ".join([f"{puerta['calle']} {puerta['altura']}" for puerta in puertas_info_3]),
            }   
                
            writer.writerow(mapped_data)