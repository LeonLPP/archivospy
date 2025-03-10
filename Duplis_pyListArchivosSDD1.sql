-- + - - - - -
-- + Marcar Duplicados
-- + - - - - -

USE MyFiles24
GO

SELECT * 
INTO py.ListArchivos_SDD1
FROM py.ListArchivos_Bak
GO


SELECT -- TOP 100 *
	idDupli, FORMAT(COUNT(1), N'N0') AS totArchivos
	, FORMAT(SUM(Tamano), N'N0') AS totSize
	, FORMAT(SUM(Tamano)/(1024^2), N'N2') AS totSizeMb
	-- , MIN(FeCreado) AS MinCreado
	, CONVERT(nvarchar(15), MAX(FeCreado), 107) AS FeCreaMax
	, CONVERT(nvarchar(15), MAX(FecModif), 106) AS FecModMax
	, CONVERT(nvarchar(15), MAX(FecAccess), 107) AS FecAccMax
FROM py.ListArchivos_SDD1
GROUP BY idDupli
GO

-- DUPLICADOS 1-solo por hash y 2-hash nombre y tamaño
-- Marcamos duplicados por Hash
WITH ArDuplisHash AS (
    SELECT
        idHash,
        COUNT(*) AS TotalDuplicados,
        MIN(RutArchivo) AS ArchivoPrincipal
    FROM py.ListArchivos_SDD1
    GROUP BY idHash
    HAVING COUNT(*) > 1
)
UPDATE py.ListArchivos_SDD1
SET idDupli = 1
WHERE RutArchivo IN (
    SELECT l.RutArchivo
    FROM py.ListArchivos_SDD1 l
    INNER JOIN ArDuplisHash ad
    ON l.idHash = ad.idHash
    WHERE l.RutArchivo <> ad.ArchivoPrincipal
);
-- Resultado (47816 rows affected) 10segundos

-- Marcamos duplicados por nombre y tamaño
WITH ArDuplis AS (
    SELECT Nombre, Exten, Tamano, idHash,
        COUNT(*) AS TotalDuplicados,
        MIN(RutArchivo) AS ArchivoPrincipal
    FROM py.ListArchivos_SDD1
    GROUP BY Nombre, Exten, Tamano, idHash
    HAVING COUNT(*) > 1
)
UPDATE py.ListArchivos_SDD1
SET idDupli = 2
WHERE RutArchivo IN (
    SELECT l.RutArchivo
    FROM py.ListArchivos_SDD1 l
    INNER JOIN ArDuplis ad
    ON l.Nombre = ad.Nombre
       AND l.Exten = ad.Exten
       AND l.Tamano = ad.Tamano
       AND l.idHash = ad.idHash
    WHERE l.RutArchivo <> ad.ArchivoPrincipal
);
-- Resultado (43273 rows affected) 7segundos


DECLARE @fecini date = '2000-01-01'
DECLARE @fecfin date = '2012-01-01'
SELECT Nombre, Exten, Tamano, idHash, Ruta
	, TRIM(CONVERT(CHAR(15), FeCreado, 107)) AS FeCrea
	, TRIM(CONVERT(CHAR(15), FecAccess, 107)) AS ultAcceso
	, idDupli
	, RutArchivo
FROM py.ListArchivos_SDD1
-- WHERE idDupli >0
-- WHERE FecAccess Between @fecini And @fecfin
WHERE Ruta Like 'h:\iomega\tvshow%'
ORDER BY idHash, Nombre, Ruta
;

DECLARE @miRuta NVarchar(50) = 'h:\iomega%';
SELECT SUBSTRING(Ruta, 1, LEN(@miRuta)-1) AS Grupo1
	, idDupli
	, TRIM(CONVERT(CHAR(15), MIN(FeCreado), 107)) AS FeCreaMin
	, TRIM(CONVERT(CHAR(15), MAX(FeCreado), 107)) AS FeCreaMax
	, FORMAT(COUNT(1), N'N0') AS numArchivos
	, FORMAT(SUM(Tamano), N'N2') AS totSize
FROM py.ListArchivos_SDD1
WHERE Ruta Like @miRuta
Group By SUBSTRING(Ruta, 1, LEN(@miRuta)-1)
	, idDupli
Order By SUBSTRING(Ruta, 1, LEN(@miRuta)-1)
	, idDupli
GO


WITH RutAgrupada AS (
    SELECT 
        CASE 
            WHEN CHARINDEX('\', Ruta, CHARINDEX('\', Ruta, 1) + 1) = 0 THEN Ruta
            ELSE SUBSTRING(Ruta, 1, CHARINDEX('\', Ruta, CHARINDEX('\', Ruta, 1) + 1) - 1)
        END AS grpRuta,
        idDupli, Tamano, FeCreado, FecModif ,FecAccess
    FROM py.ListArchivos_SDD1
)
SELECT grpRuta, idDupli
    , TRIM(CONVERT(CHAR(15), MIN(FeCreado), 107)) AS FeCreaMax
    , TRIM(CONVERT(CHAR(15), MAX(FecModif), 107)) AS FeModifMax
	, TRIM(CONVERT(CHAR(15), MAX(FecAccess), 107)) AS ultAcceso
    , COUNT(*) AS numArchivos
    , FORMAT(SUM(Tamano), N'N2') AS totSize
FROM RutAgrupada
GROUP BY grpRuta, idDupli
ORDER BY grpRuta, idDupli
GO
