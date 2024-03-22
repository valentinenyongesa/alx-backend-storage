-- 3-glam_rock.sql
-- Task: List all bands with Glam rock as their main style, ranked by their longevity

SELECT band_name, 
       (CASE 
            WHEN formed IS NULL OR formed = 0 THEN NULL
            WHEN split IS NULL THEN 2022 - formed
            ELSE split - formed
        END) AS lifespan
FROM metal_bands
WHERE style = 'Glam rock'
ORDER BY lifespan DESC;
