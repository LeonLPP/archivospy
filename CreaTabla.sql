USE MyFiles24
GO

DROP TABLE IF EXISTS py.ListArchivos;
CREATE TABLE py.ListArchivos (
    idArchivo INT IDENTITY(1, 1) NOT NULL
	, FeCreado DATETIME
    , Nombre NVARCHAR(MAX)
    , Exten NVARCHAR(50)
    , Tamano BIGINT
    , Ruta NVARCHAR(MAX)
    , RutArchivo NVARCHAR(MAX)
    , FecModif DATETIME
    , FecAccess DATETIME
    , idHash NVARCHAR(100),
	PRIMARY KEY CLUSTERED 
(
	[idArchivo] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO

-- Agregar columna UsrAlta con un valor predeterminado del usuario actual
ALTER TABLE py.ListArchivos
	ADD UsrAlta NVARCHAR(255) DEFAULT SYSTEM_USER
	, FecAlta DATETIME DEFAULT GETDATE()
	, idDupli INT DEFAULT 0
	, idAccion INT DEFAULT NULL
	, FeAccion DATETIME DEFAULT Null
	, idResult INT
	, FecResult DATETIME
	, UsrResult NVARCHAR(255)
GO


/*1 = Borrado, 2 = No se ha podido borrar, 3 = No encontrado para borrar, 
  4 = Error al intentar borrar, 5 = Conservar, 6 = Comprimir
*/
-- Crear la tabla ddAccion
DROP TABLE IF EXISTS ddAccion;
CREATE TABLE ddAccion (
    idAccion INT PRIMARY KEY,          -- Clave primaria
    DescripS NVARCHAR(50) NOT NULL,   -- Descripción corta
    DescripL NVARCHAR(255) NOT NULL   -- Descripción larga
);

ALTER TABLE ddAccion
	ADD UsrAlta NVARCHAR(255) DEFAULT SYSTEM_USER,
	FecAlta DATETIME DEFAULT GETDATE();


-- Insertar los valores iniciales
INSERT INTO ddAccion (idAccion, DescripS, DescripL)
VALUES (99, 'Borrado', 'Archivo eliminado correctamente'),
	(90, 'Para Borrar', 'Archivo seleccionado para borrar'),
	(91, 'No encontrado', 'Archivo no encontrado para borrar'),
	(92, 'Simula Borrar', 'Simula el borrado, No elimina el archivo'),
	(93, 'No borrado', 'No se ha podido borrar el archivo'),
	(94, 'Error borrar', 'Error al intentar borrar el archivo'),
	(0, 'Conservar', 'Archivo marcado para conservar'),
	(1, 'Comprimir', 'Archivo marcado para compresión');
GO
Select * From ddAccion
GO

Select COUNT(1), MIN(FecAlta), MAX(FecAlta) From py.ListArchivos
GO