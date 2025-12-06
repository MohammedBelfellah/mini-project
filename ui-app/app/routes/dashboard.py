from flask import Blueprint, render_template
from app.db import get_db

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/')
def index():
    """Dashboard with statistics and map."""
    conn = get_db()
    cur = conn.cursor()
    
    # Total buildings count
    cur.execute('SELECT COUNT(*) FROM BATIMENT')
    total_buildings = cur.fetchone()[0]
    
    # Buildings by zone
    cur.execute('''
        SELECT z.nom_zone, COUNT(b.code_batiment)
        FROM ZONE_URBAINE z
        LEFT JOIN BATIMENT b ON z.id_zone = b.id_zone
        GROUP BY z.id_zone, z.nom_zone
        ORDER BY COUNT(b.code_batiment) DESC
    ''')
    buildings_by_zone = cur.fetchall()
    
    # Buildings by type
    cur.execute('''
        SELECT t.libelle_type, COUNT(b.code_batiment)
        FROM TYPE_BATIMENT t
        LEFT JOIN BATIMENT b ON t.id_type = b.id_type
        GROUP BY t.id_type, t.libelle_type
        ORDER BY COUNT(b.code_batiment) DESC
    ''')
    buildings_by_type = cur.fetchall()
    
    # Buildings by conservation state (latest inspection)
    cur.execute('''
        SELECT i.etat_constate, COUNT(DISTINCT i.code_batiment)
        FROM INSPECTION i
        INNER JOIN (
            SELECT code_batiment, MAX(date_visite) as max_date
            FROM INSPECTION
            GROUP BY code_batiment
        ) latest ON i.code_batiment = latest.code_batiment 
                 AND i.date_visite = latest.max_date
        GROUP BY i.etat_constate
        ORDER BY i.etat_constate
    ''')
    buildings_by_state = cur.fetchall()
    
    # Buildings needing urgent intervention
    cur.execute('''
        SELECT b.code_batiment, b.nom_batiment, i.etat_constate, i.date_visite
        FROM BATIMENT b
        INNER JOIN INSPECTION i ON b.code_batiment = i.code_batiment
        INNER JOIN (
            SELECT code_batiment, MAX(date_visite) as max_date
            FROM INSPECTION
            GROUP BY code_batiment
        ) latest ON i.code_batiment = latest.code_batiment 
                 AND i.date_visite = latest.max_date
        WHERE i.etat_constate IN ('En ruine', 'Dégradé')
        ORDER BY 
            CASE i.etat_constate 
                WHEN 'En ruine' THEN 1 
                WHEN 'Dégradé' THEN 2 
            END,
            b.nom_batiment
    ''')
    urgent_buildings = cur.fetchall()
    
    # Total restoration cost by year
    cur.execute('''
        SELECT EXTRACT(YEAR FROM date_debut)::INTEGER as year, 
               COALESCE(SUM(cout_estime), 0) as total_cost
        FROM INTERVENTION
        WHERE date_debut IS NOT NULL
        GROUP BY EXTRACT(YEAR FROM date_debut)
        ORDER BY year DESC
    ''')
    cost_by_year = cur.fetchall()
    
    # Recent interventions count
    cur.execute('SELECT COUNT(*) FROM INTERVENTION')
    total_interventions = cur.fetchone()[0]
    
    # Recent inspections count
    cur.execute('SELECT COUNT(*) FROM INSPECTION')
    total_inspections = cur.fetchone()[0]
    
    # ========== NEW: Buildings for Map ==========
    cur.execute('''
        SELECT b.code_batiment, b.nom_batiment, b.adresse_rue, 
               b.latitude, b.longitude,
               z.nom_zone, t.libelle_type, n.niveau,
               (SELECT i.etat_constate 
                FROM INSPECTION i 
                WHERE i.code_batiment = b.code_batiment 
                ORDER BY i.date_visite DESC 
                LIMIT 1) as dernier_etat
        FROM BATIMENT b
        LEFT JOIN ZONE_URBAINE z ON b.id_zone = z.id_zone
        LEFT JOIN TYPE_BATIMENT t ON b.id_type = t.id_type
        LEFT JOIN NIV_PROTECTION n ON b.id_protection = n.id_protection
        WHERE b.latitude IS NOT NULL AND b.longitude IS NOT NULL
    ''')
    buildings_for_map = cur.fetchall()
    
    # Convert to list of dictionaries for JSON
    map_buildings = []
    for b in buildings_for_map:
        map_buildings.append({
            'code': b[0],
            'nom': b[1],
            'adresse': b[2] or 'N/A',
            'lat': float(b[3]) if b[3] else None,
            'lng': float(b[4]) if b[4] else None,
            'zone': b[5] or 'N/A',
            'type': b[6] or 'N/A',
            'protection': b[7] or 'N/A',
            'etat': b[8] or 'Non inspecté'
        })
    
    cur.close()
    
    return render_template('dashboard/index.html',
                          total_buildings=total_buildings,
                          total_interventions=total_interventions,
                          total_inspections=total_inspections,
                          buildings_by_zone=buildings_by_zone,
                          buildings_by_type=buildings_by_type,
                          buildings_by_state=buildings_by_state,
                          urgent_buildings=urgent_buildings,
                          cost_by_year=cost_by_year,
                          map_buildings=map_buildings)