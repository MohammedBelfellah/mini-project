
-- =============================================
-- 1. TABLES DE RÉFÉRENCE (Listes déroulantes)
-- =============================================

CREATE TABLE ZONE_URBAINE (
   id_zone      SERIAL PRIMARY KEY,
   nom_zone     VARCHAR(100) NOT NULL,
   type_zone    VARCHAR(50)  -- Ex: Quartier, Secteur
);

CREATE TABLE TYPE_BATIMENT (
   id_type      SERIAL PRIMARY KEY,
   libelle_type VARCHAR(100) NOT NULL -- Ex: Religieux, Civil
);



CREATE TABLE NIV_PROTECTION (
   id_protection SERIAL PRIMARY KEY,
   niveau        VARCHAR(50) NOT NULL -- Ex: Classé, Inscrit
);

CREATE TABLE PROPRIETAIRE (
   id_proprio   SERIAL PRIMARY KEY,
   nom_complet  VARCHAR(150) NOT NULL,
   type_proprio VARCHAR(50), -- Public, Privé
   contact      VARCHAR(100)
);

CREATE TABLE PRESTATAIRE (
   id_prestataire SERIAL PRIMARY KEY,
   nom_entreprise VARCHAR(150) NOT NULL,
   role_prest     VARCHAR(100) -- Architecte, Entreprise BTP
);

-- =============================================
-- 2. TABLE CENTRALE : BATIMENT
-- =============================================

CREATE TABLE BATIMENT (
   code_batiment     SERIAL PRIMARY KEY,
   nom_batiment      VARCHAR(150),
   adresse_rue       VARCHAR(255),
   latitude          DECIMAL(9,6),
   longitude         DECIMAL(9,6),
   date_construction DATE,
   note_historique   TEXT,
   
   -- Clés étrangères (Relations 1,1)
   id_zone       INT REFERENCES ZONE_URBAINE(id_zone),
   id_type       INT REFERENCES TYPE_BATIMENT(id_type),
   id_protection INT REFERENCES NIV_PROTECTION(id_protection),
   id_proprio    INT REFERENCES PROPRIETAIRE(id_proprio)
);

-- =============================================
-- 3. TABLES ÉVÉNEMENTS (Historique)
-- =============================================

CREATE TABLE INSPECTION (
   id_inspect    SERIAL PRIMARY KEY,
   date_visite   DATE NOT NULL,
   rapport       TEXT,
   etat_constate VARCHAR(50), -- Bon, Moyen, Dégradé...
   code_batiment INT NOT NULL REFERENCES BATIMENT(code_batiment)
);

CREATE TABLE INTERVENTION (
   id_interv    SERIAL PRIMARY KEY,
   date_debut   DATE,
   date_fin     DATE,
   type_travaux VARCHAR(255),
   cout_estime  DECIMAL(12,2),
   est_validee  BOOLEAN DEFAULT FALSE,
   
   code_batiment  INT NOT NULL REFERENCES BATIMENT(code_batiment),
   id_prestataire INT NOT NULL REFERENCES PRESTATAIRE(id_prestataire)
);

-- =============================================
-- 4. TABLE DOCUMENTS (Spec 10 : Photos/Docs)
-- =============================================

CREATE TABLE DOCUMENT_MEDIA (
   id_doc        SERIAL PRIMARY KEY,
   titre_doc     VARCHAR(150),
   type_doc      VARCHAR(50), -- Photo, Plan, PDF
   url_fichier   VARCHAR(255),
   code_batiment INT NOT NULL REFERENCES BATIMENT(code_batiment)
);
   