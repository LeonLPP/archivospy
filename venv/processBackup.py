import os
import re
import datetime

def validRespaldo(backFolder):
    """
    Valida los respaldos.
    - Verifica si todos los archivos están comprimidos en .zip o .7z.
    - Se queda con los últimos 7 respaldos diarios.
    - Se queda con los respaldos más recientes mes a mes durante los últimos 24 meses.
    """
    # Lista de archivos
    archivos = [archivo for archivo in os.listdir(backFolder) if os.path.isfile(os.path.join(backFolder, archivo))]

    # Filtrar archivos que terminan con _aaaammdd
    arFmtFecha = re.compile(r".*_\d{8}\.(zip|7z)$")
    arValidos = [archivo for archivo in archivos if arFmtFecha.match(archivo)]

    # Verificar si hay archivos que no están comprimidos
    arNoComprimidos = [archivo for archivo in archivos if re.match(r".*_\d{8}$", archivo) and archivo not in arValidos]

    if arNoComprimidos:        
        for archivo in arNoComprimidos:
            print(f"Debe comprimir- {archivo}")
        return  # Finaliza, todos deben estar comprimidos

    print("Todos los archivos están comprimidos. Procesando respaldos...")

    # Ordenar los respaldos por fecha del nombre del archivo
    arValidos.sort(key=lambda x: datetime.datetime.strptime(x.split('_')[-1].split('.')[0], "%Y%m%d"))

    # Mantener los últimos 7 respaldos diarios
    ultDiarios = arValidos[-7:]

    # Seleccionar un respaldo por mes de los últimos 24 meses
    arMensuales = {}
    ahora = datetime.datetime.now()
    for respaldo in reversed(arValidos):  # Iterar del más reciente al más antiguo
        fecRespaldo = datetime.datetime.strptime(respaldo.split('_')[-1].split('.')[0], "%Y%m%d")
        mesesDiff = (ahora.year - fecRespaldo.year) * 12 + ahora.month - fecRespaldo.month
        if 0 <= mesesDiff < 24:
            mesRespaldo = fecRespaldo.strftime("%Y-%m")  # Usar el año-mes como clave
            if mesRespaldo not in arMensuales:
                arMensuales[mesRespaldo] = respaldo

    # Combinar los respaldos diarios y mensuales
    respadoSelect = set(ultDiarios + list(arMensuales.values()))

    # print("Los respaldos que se mantendrán son:")
    for respaldo in respadoSelect:
        print(f"- Mantener {respaldo}")

    # Eliminar respaldos
    for respaldo in arValidos:
        if respaldo not in respadoSelect:
            ruta_respaldo = os.path.join(backFolder, respaldo)
            print(f"Eliminar respaldo: {ruta_respaldo}")
            # os.remove(ruta_respaldo)
