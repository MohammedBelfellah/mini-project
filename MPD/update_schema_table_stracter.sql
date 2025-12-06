-- 1. Enable PostGIS extension (if not already done)
CREATE EXTENSION IF NOT EXISTS postgis;

-- 2. Add the geometry column
ALTER TABLE BATIMENT 
ADD COLUMN geom GEOMETRY(POINT, 4326);

-- 3. (Optional) Auto-fill geometry from your existing lat/lon columns
UPDATE BATIMENT 
SET geom = ST_SetSRID(ST_MakePoint(longitude, latitude), 4326)
WHERE longitude IS NOT NULL AND latitude IS NOT NULL;




ALTER TABLE INTERVENTION 
ADD COLUMN date_validation DATE,
ADD COLUMN commentaire_validation TEXT; -- For notes from the municipality




ALTER TABLE INTERVENTION 
ADD COLUMN statut_travaux VARCHAR(50) DEFAULT 'Planifié';
-- Example values: 'Planifié', 'En cours', 'Terminé', 'Annulé'


-- Add a constraint to ensure only valid states are entered
ALTER TABLE INSPECTION 
ADD CONSTRAINT chk_etat_constate 
CHECK (etat_constate IN ('Bon', 'Moyen', 'Dégradé', 'En ruine'));






