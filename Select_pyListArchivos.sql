USE MyFiles24
GO

SELECT TOP 100 *
	-- COUNT(1), SUM(Tamano),  MIN(FeCreado), MAX(FeCreado) 
FROM py.ListArchivos
GO

DECLARE @filtro NVarchar(50) = '.mdb';
SELECT Exten, COUNT(1), FORMAT(SUM(Tamano)/1024^3, N'N2')
	-- ,  MIN(FeCreado), MAX(FeCreado) 
	, TRIM(CONVERT(CHAR(15), MIN(FeCreado), 107)) AS FeCraMin
	, TRIM(CONVERT(CHAR(15), MAX(FeCreado), 107)) AS FeCraMax
FROM py.ListArchivos
WHere Lower(Exten) = lower(@filtro)
Group By Exten;

SELECT Exten, COUNT(1), FORMAT(SUM([Size])/1024^3, N'N2')
	--,  MIN(Creado) AS FeCraMin, MAX(Creado) AS FeCraMax
	, TRIM(CONVERT(CHAR(15), MIN(Creado), 107)) AS FeCraMin
	, TRIM(CONVERT(CHAR(15), MAX(Creado), 107)) AS FeCraMax
FROM ListFile_Seagate_20241214
WHere Lower(Exten) = lower(@filtro)
Group By Exten;
GO


DECLARE @filtro NVarchar(50) = '.mdb';
Select lo.Exten, lo.Dupli, Borrado
	, lo.Nombre, lo.mPath, lo.Size
	, lp.Nombre, lp.Ruta, lp.Tamano
	-- , Creado, FecDupli, Exten, mHash
	, lo.UsrMod, lo.FecMod, lo.FullPath
From ListFile_Seagate_20241214 lo
Inner Join py.ListArchivos lp
ON lo.mHash = lp.idHash
WHere Lower(lo.Exten) = lower(@filtro)
	And lo.Borrado Is Null
	And lo.Dupli = 1
GO

-- RESPALDAMOS TABLA INICIAL - En el campo Nombre NO ha incluido la extencion
SELECT *
INTO py.ListArchivos_Bak
FROM py.ListArchivos
-- WHERE 1= 0 -- Estructura sin datos
;


-- DUPLICADOS 1-solo por hash y 2-hash nombre y tamaño
-- Marcamos duplicados por Hash
WITH ArDuplisHash AS (
    SELECT
        idHash,
        COUNT(*) AS TotalDuplicados,
        MIN(RutArchivo) AS ArchivoPrincipal
    FROM py.ListArchivos
    GROUP BY idHash
    HAVING COUNT(*) > 1
)
UPDATE py.ListArchivos
SET idDupli = 1
WHERE RutArchivo IN (
    SELECT l.RutArchivo
    FROM py.ListArchivos l
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
    FROM py.ListArchivos
    GROUP BY Nombre, Exten, Tamano, idHash
    HAVING COUNT(*) > 1
)
UPDATE py.ListArchivos
SET idDupli = 2
WHERE RutArchivo IN (
    SELECT l.RutArchivo
    FROM py.ListArchivos l
    INNER JOIN ArDuplis ad
    ON l.Nombre = ad.Nombre
       AND l.Exten = ad.Exten
       AND l.Tamano = ad.Tamano
       AND l.idHash = ad.idHash
    WHERE l.RutArchivo <> ad.ArchivoPrincipal
);
-- Resultado (43273 rows affected) 7segundos

SELECT idDupli, COUNT(1), FORMAT(SUM(Tamano)/1024^3, N'N2')
	-- ,  MIN(FeCreado), MAX(FeCreado) 
	, TRIM(CONVERT(CHAR(15), MIN(FeCreado), 107)) AS FeCraMin
	, TRIM(CONVERT(CHAR(15), MAX(FeCreado), 107)) AS FeCraMax
	, TRIM(CONVERT(CHAR(15), MIN(FecAccess), 107)) AS ultAccesoMin
	, TRIM(CONVERT(CHAR(15), MAX(FecAccess), 107)) AS ultAccesoMax
FROM py.ListArchivos
Group By idDupli;

DECLARE @fecini date = '2008-01-01'
DECLARE @fecfin date = '2012-01-01'
SELECT Nombre, Exten, Tamano, idHash, Ruta
	, TRIM(CONVERT(CHAR(15), FeCreado, 107)) AS FeCrea
	, TRIM(CONVERT(CHAR(15), FecAccess, 107)) AS ultAcceso
	, idDupli
	, RutArchivo
FROM py.ListArchivos
-- WHERE idDupli >0
-- WHERE FecAccess Between @fecini And @fecfin
WHERE Ruta Like 'h:\iomega\tvshow%'
ORDER BY idHash, Nombre, Ruta
;

DECLARE @miRuta NVarchar(50) = 'h:%';
SELECT SUBSTRING(Ruta, 1, LEN(@miRuta)-1) AS Grupo1
	, idDupli
	, TRIM(CONVERT(CHAR(15), MIN(FeCreado), 107)) AS FeCreaMin
	, TRIM(CONVERT(CHAR(15), MAX(FeCreado), 107)) AS FeCreaMax
	, COUNT(1) AS numArchivos
	, FORMAT(SUM(Tamano), N'N2') AS totSize
FROM py.ListArchivos
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
    FROM py.ListArchivos
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

SELECT *
INTO py.ListArchivosTest
FROM py.ListArchivos
WHERE 1=0
GO

DELETE from py.ListArchivosTest
SELECT COUNT(1)
FROM py.ListArchivosTest
-- WHERE RutArchivo In ('C:\Users\LeonPP\Documents\Eventos_1.accdb'
-- 	, 'C:\Users\LeonPP\Documents\espana\casas\villa_bonita\cetelem\certificadologaltycontratotransaccin003001000100000.zip'	)
GO
