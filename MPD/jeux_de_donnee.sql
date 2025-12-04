-- =============================================
-- JEU DE DONNÉES (DML) - CONTEXTE MAROC
-- =============================================

-- 1. INSERTION ZONES URBAINES
INSERT INTO ZONE_URBAINE (id_zone, nom_zone, type_zone) VALUES
(1, 'Médina de Fès el-Bali', 'Secteur Sauvegardé'),
(2, 'Centre-Ville Casablanca', 'Architecture XXème'),
(3, 'Kasbah des Oudayas (Rabat)', 'Quartier Historique'),
(4, 'Palmeraie de Skoura', 'Zone Oasienne');

-- 2. INSERTION TYPES DE BÂTIMENT
INSERT INTO TYPE_BATIMENT (id_type, libelle_type) VALUES
(1, 'Medersa (École Coranique)'),
(2, 'Riad / Dar'),
(3, 'Immeuble Art Déco'),
(4, 'Kasbah (Architecture de terre)');

-- 3. INSERTION NIVEAUX DE PROTECTION
INSERT INTO NIV_PROTECTION (id_protection, niveau) VALUES
(1, 'Patrimoine Mondial UNESCO'),
(2, 'Classé Monument National (Dahir)'),
(3, 'Inventaire Régional'),
(4, 'En cours de classement');

-- 4. INSERTION PROPRIÉTAIRES
INSERT INTO PROPRIETAIRE (id_proprio, nom_complet, type_proprio, contact) VALUES
(1, 'Ministère des Habous et Affaires Islamiques', 'Public', '+212 5 37 76 00 00'),
(2, 'Fondation Nationale des Musées', 'Semi-Public', 'contact@fnm.ma'),
(3, 'Héritiers Famille El Glaoui', 'Privé', 'Notaire Maître Bennani'),
(4, 'Wilaya du Grand Casablanca', 'Public', 'service.patrimoine@casablanca.ma');

-- 5. INSERTION PRESTATAIRES
INSERT INTO PRESTATAIRE (id_prestataire, nom_entreprise, role_prest) VALUES
(1, 'Atelier du Zellige Fassi', 'Artisanat d''Art'),
(2, 'Société de Restauration des Kasbahs (SRK)', 'Spécialiste Pisé/Terre'),
(3, 'Bureau d''Études Structure & Beton', 'Bureau d''Études'),
(4, 'Ent. Générale de Bâtiment Maroc', 'Gros Oeuvre');

-- =============================================
-- 6. INSERTION BÂTIMENTS (Table Centrale)
-- =============================================

-- Réinitialisation de la séquence pour être sûr (Optionnel)
-- ALTER SEQUENCE batiment_code_batiment_seq RESTART WITH 1;

INSERT INTO BATIMENT (code_batiment, nom_batiment, adresse_rue, latitude, longitude, date_construction, note_historique, id_zone, id_type, id_protection, id_proprio) VALUES
(100, 'Medersa Bou Inania', 'Rue Talaa Kebira, Fès', 34.062450, -4.982780, '1350-01-01', 'Chef-d''oeuvre de l''architecture mérinide, construite par le sultan Abou Inan Faris. Dispose d''une horloge hydraulique unique.', 1, 1, 1, 1),

(101, 'Immeuble Liberté (Le 17e étage)', 'Bd de la Liberté, Casablanca', 33.590120, -7.612340, '1951-06-15', 'Premier gratte-ciel d''Afrique du Nord à sa construction. Architecture moderne emblématique de Casa.', 2, 3, 3, 3),

(102, 'Kasbah Amridil', 'Oasis de Skoura', 31.047800, -6.567000, '1680-01-01', 'Forteresse familiale emblématique figurant sur les anciens billets de 50 Dirhams. Architecture en pisé très fragile.', 4, 4, 2, 3),

(103, 'Musée des Oudayas', 'Kasbah des Oudayas, Rabat', 34.031500, -6.836500, '1672-01-01', 'Ancienne résidence princière de Moulay Ismaïl, transformée en musée des parures.', 3, 2, 1, 2);


-- =============================================
-- 7. INSERTION INSPECTIONS (Historique)
-- =============================================

INSERT INTO INSPECTION (date_visite, rapport, etat_constate, code_batiment) VALUES
('2023-11-10', 'Fissures observées sur les murs porteurs suite au séisme. Zelliges intacts.', 'Moyen', 100), -- Medersa
('2024-01-15', 'Infiltrations d''eau en toiture terrasse. Façade noircie par la pollution.', 'Dégradé', 101), -- Immeuble Casa
('2024-02-20', 'État exceptionnel de conservation. Quelques reprises de pisé nécessaires au sud.', 'Bon', 102);    -- Kasbah


-- =============================================
-- 8. INSERTION INTERVENTIONS
-- =============================================

INSERT INTO INTERVENTION (date_debut, date_fin, type_travaux, cout_estime, est_validee, code_batiment, id_prestataire) VALUES
('2024-03-01', '2024-06-30', 'Restauration des plâtres sculptés et bois de cèdre', 150000.00, TRUE, 100, 1), -- Sur Medersa par Atelier Zellige
('2024-09-01', NULL, 'Renforcement structurel et étanchéité', 450000.00, FALSE, 101, 3); -- Sur Immeuble (Pas encore validé)


-- =============================================
-- 9. INSERTION DOCUMENTS / MEDIA
-- =============================================

INSERT INTO DOCUMENT_MEDIA (titre_doc, type_doc, url_fichier, code_batiment) VALUES
('Plan Cadastral 1950', 'Plan PDF', '/docs/casa/plan_liberte_1950.pdf', 101),
('Photo Cour Intérieure', 'Photo JPG', '/img/fes/bouinania_cour.jpg', 100),
('Rapport Expertise Pisé', 'Rapport PDF', '/docs/skoura/expert_terre.pdf', 102);