USE MyFiles24

SELECT TABLE_CATALOG, TABLE_NAME, ORDINAL_POSITION, TABLE_SCHEMA, COLUMN_NAME, DATA_TYPE 
FROM INFORMATION_SCHEMA.COLUMNS 
WHERE TABLE_CATALOG = 'MyFiles24'
AND TABLE_SCHEMA = 'py'
AND TABLE_NAME = 'ListArchivos'
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

SELECT COUNT(1)
FROM py.ListArchivos
Where idDupli=1
GO

Update py.ListArchivos
Set idAccion = 92, FeAccion = GETDATE()
Where idDupli=1
GO


SELECT FeCreado, Nombre, Exten, Tamano, Ruta, RutArchivo
	, FecModif, FecAccess, idHash, UsrAlta, FecAlta, idDupli
FROM py.ListArchivos
WHERE lower(Exten) IN ('.zip', '.rar', '.7z')
Order By Ruta
GO

Select count(1) FROM py.ListArchivos
WHERE lower(Exten) IN ('.zip', '.rar', '.7z')
GO
h:\llp16gb\docs_capgemini\datos\Bankia\Control Riesgo Operativo en Adeudos\Documento_Funcional\DTC