-- List Glam rock bands ranked by longevity
SELECT band_name, (2022 - formed) AS lifespan
FROM metal_bands
WHERE split LIKE '%Glam rock%'
ORDER BY lifespan DESC;
