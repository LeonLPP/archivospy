# Archivo configuracion.py

# Definir la cadena de conexión
CADENA_CONEXION_TEST = (
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=tu_servidor;"
    "DATABASE=MyFiles24;"
    "UID=tu_usuario;"
    "PWD=tu_contraseña;"
)

CADENA_CONEXION = (
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=.\SQLEXPRESS;"
    "DATABASE=MyFiles24;"
    "Trusted_Connection=Yes;"
    # "Encrypt=Yes;"
    "TrustServerCertificate=No;"
)


#  4. Opcional: Proteger la información sensible
#  Para mejorar la seguridad, puedes usar variables de entorno en lugar de almacenar credenciales directamente en el archivo. Por ejemplo:
#  
#  Instala la biblioteca python-decouple:
#  
#  pip install python-decouple
#  
#  Crea un archivo .env con tus credenciales:
#  SERVER=tu_servidor
#  DATABASE=misArchivos
#  UID=tu_usuario
#  PWD=tu_contraseña
#  
#  Modifica configuracion.py para leer estas variables:
#  python
#  from decouple import config
#  
#  CADENA_CONEXION = (
#      f"DRIVER={{ODBC Driver 17 for SQL Server}};"
#      f"SERVER={config('SERVER')};"
#      f"DATABASE={config('DATABASE')};"
#      f"UID={config('UID')};"
#      f"PWD={config('PWD')};"
#  )
#  Así puedes evitar almacenar credenciales sensibles en el código fuente directamente.