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
    @idArchivo INT,
    @idResult INT
AS
BEGIN
    SET NOCOUNT ON;

    -- Actualiza la tabla py.ListArchivos con los valores recibidos y calcula UsrResult y FecResult
    UPDATE py.ListArchivos
    SET idResult = @idResult
        , FecResult = GETDATE()
        , UsrResult = SUSER_SNAME()
    WHERE idArchivo = @idArchivo;

    -- Verificar si la actualización afectó alguna fila
    IF @@ROWCOUNT = 0
    BEGIN
        -- Si no se encuentra el idArchivo, devolver un mensaje informativo
        RAISERROR ('El idArchivo especificado no existe en la tabla py.ListArchivos.', 16, 1);
    END
END;
GO
