USE MyFiles24
GO


SELECT TABLE_CATALOG, TABLE_NAME, TABLE_SCHEMA, COLUMN_NAME, DATA_TYPE 
FROM INFORMATION_SCHEMA.COLUMNS 
WHERE TABLE_CATALOG = 'MyFiles24'
AND TABLE_SCHEMA = 'py'
ORDER BY TABLE_NAME, ORDINAL_POSITION
GO

DROP PROCEDURE IF EXISTS py.sp_procesArchivos
GO

CREATE PROCEDURE py.sp_procesArchivos    
    @idAccion INT
AS
BEGIN
    SET NOCOUNT ON;
	Select idArchivo, Nombre, RutArchivo, Tamano
	From py.ListArchivos
	Where idAccion = @idAccion;
END;
GO


EXEC py.sp_procesArchivos 92;
