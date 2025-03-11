import os
import re
import datetime

def validRespaldo(backup_folder):
    """
    Valida los respaldos en la carpeta indicada.
    - Verifica si los archivos están comprimidos en .zip o .7z.
    - Se queda con los últimos 7 respaldos diarios.
    - Se queda con los respaldos más recientes mes a mes durante los últimos 24 meses.
    """
    # Lista de archivos en la carpeta
    archivos = [archivo for archivo in os.listdir(backup_folder) if os.path.isfile(os.path.join(backup_folder, archivo))]

    # Filtrar archivos que terminan con _aaaammdd
    patron_respaldo = re.compile(r".*_\d{8}\.(zip|7z)$")
    respaldos_validos = [archivo for archivo in archivos if patron_respaldo.match(archivo)]

    # Verificar si hay archivos que no están comprimidos
    no_comprimidos = [archivo for archivo in archivos if re.match(r".*_\d{8}$", archivo) and archivo not in respaldos_validos]

    if no_comprimidos:
        print("Los siguientes archivos no están comprimidos. Por favor, comprímelos en formato .zip o .7z:")
        for archivo in no_comprimidos:
            print(f"- {archivo}")
        return  # Salir si hay archivos no comprimidos

    print("Todos los archivos están comprimidos. Procesando respaldos...")

    # Ordenar los respaldos por fecha (extraída del nombre del archivo)
    respaldos_validos.sort(key=lambda x: datetime.datetime.strptime(x.split('_')[-1].split('.')[0], "%Y%m%d"))

    # Mantener los últimos 7 respaldos diarios
    ultimos_diarios = respaldos_validos[-7:]

    # Seleccionar un respaldo por mes de los últimos 24 meses
    respaldos_mensuales = {}
    ahora = datetime.datetime.now()
    for respaldo in reversed(respaldos_validos):  # Iterar del más reciente al más antiguo
        fecha_respaldo = datetime.datetime.strptime(respaldo.split('_')[-1].split('.')[0], "%Y%m%d")
        meses_diferencia = (ahora.year - fecha_respaldo.year) * 12 + ahora.month - fecha_respaldo.month
        if 0 <= meses_diferencia < 24:
            mes_clave = fecha_respaldo.strftime("%Y-%m")  # Usar el año-mes como clave
            if mes_clave not in respaldos_mensuales:
                respaldos_mensuales[mes_clave] = respaldo

    # Combinar los respaldos diarios y mensuales
    respaldos_finales = set(ultimos_diarios + list(respaldos_mensuales.values()))

    print("Los respaldos que se mantendrán son:")
    for respaldo in respaldos_finales:
        print(f"- {respaldo}")

    # Eliminar respaldos que no están en la lista final
    for respaldo in respaldos_validos:
        if respaldo not in respaldos_finales:
            ruta_respaldo = os.path.join(backup_folder, respaldo)
            print(f"Eliminando respaldo antiguo: {ruta_respaldo}")
            os.remove(ruta_respaldo)
