SELECT TABLE_CATALOG, TABLE_NAME, ORDINAL_POSITION, TABLE_SCHEMA, COLUMN_NAME, DATA_TYPE 
FROM INFORMATION_SCHEMA.COLUMNS 
WHERE TABLE_CATALOG = 'MyFiles24'
AND TABLE_SCHEMA = 'py'
ORDER BY TABLE_NAME, ORDINAL_POSITION
GO

INSERT INTO py.ListArchivos (
	FeCreado, Nombre, Exten, Tamano, Ruta, RutArchivo
	, FecModif, FecAccess, idHash, UsrAlta, FecAlta, idDupli
)
SELECT FeCreado, Nombre, Exten, Tamano, Ruta, RutArchivo
	, FecModif, FecAccess, idHash, UsrAlta, FecAlta, idDupli
FROM py.ListArchivos_SDD1
WHERE Ruta Like 'H:\llp16gb%'
GO

SELECT TOP 100 *
FROM py.ListArchivos
GO