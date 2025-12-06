from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.db import get_db

zones_bp = Blueprint('zones', __name__, url_prefix='/zones')

@zones_bp.route('/')
def list_zones():
    """List all zones with search and filtering."""
    conn = get_db()
    cur = conn.cursor()
    
    # Get filter parameters
    search = request.args.get('search', '').strip()
    type_filter = request.args.get('type_zone', '')
    
    # Base query with building count
    query = '''
        SELECT z.id_zone, z.nom_zone, z.type_zone,
               COUNT(b.code_batiment) as nb_batiments
        FROM ZONE_URBAINE z
        LEFT JOIN BATIMENT b ON z.id_zone = b.id_zone
        WHERE 1=1
    '''
    
    params = []
    
    # Search
    if search:
        query += ''' AND (
            LOWER(z.nom_zone) LIKE LOWER(%s) OR 
            LOWER(z.type_zone) LIKE LOWER(%s)
        )'''
        search_param = f'%{search}%'
        params.extend([search_param, search_param])
    
    # Type filter
    if type_filter:
        query += ' AND z.type_zone = %s'
        params.append(type_filter)
    
    query += ' GROUP BY z.id_zone, z.nom_zone, z.type_zone'
    query += ' ORDER BY z.nom_zone'
    
    cur.execute(query, params)
    zones = cur.fetchall()
    
    # Get distinct types for filter dropdown
    cur.execute('SELECT DISTINCT type_zone FROM ZONE_URBAINE WHERE type_zone IS NOT NULL ORDER BY type_zone')
    types = cur.fetchall()
    
    cur.close()
    
    return render_template('zones/list.html',
                          zones=zones,
                          types=types,
                          current_search=search,
                          current_type=type_filter)

@zones_bp.route('/add', methods=['GET', 'POST'])
def add_zone():
    """Add a new zone."""
    conn = get_db()
    cur = conn.cursor()
    
    if request.method == 'POST':
        nom_zone = request.form['nom_zone']
        type_zone = request.form.get('type_zone') or None
        
        try:
            cur.execute('''
                INSERT INTO ZONE_URBAINE (nom_zone, type_zone)
                VALUES (%s, %s)
                RETURNING id_zone
            ''', (nom_zone, type_zone))
            new_id = cur.fetchone()[0]
            conn.commit()
            cur.close()
            flash(f'Zone "{nom_zone}" ajoutée avec succès! (ID: {new_id})', 'success')
            return redirect(url_for('zones.list_zones'))
        except Exception as e:
            conn.rollback()
            flash(f'Erreur lors de l\'ajout: {str(e)}', 'danger')
            # Don't close cursor here - we need it for the form below
    
    # GET or POST with error: Load existing types for suggestions
    cur.execute('SELECT DISTINCT type_zone FROM ZONE_URBAINE WHERE type_zone IS NOT NULL ORDER BY type_zone')
    existing_types = [t[0] for t in cur.fetchall()]
    cur.close()
    
    return render_template('zones/add.html', existing_types=existing_types)

@zones_bp.route('/view/<int:id>')
def view_zone(id):
    """View zone details with its buildings."""
    conn = get_db()
    cur = conn.cursor()
    
    # Get zone details
    cur.execute('''
        SELECT id_zone, nom_zone, type_zone
        FROM ZONE_URBAINE
        WHERE id_zone = %s
    ''', (id,))
    zone = cur.fetchone()
    
    if not zone:
        flash('Zone non trouvée!', 'warning')
        return redirect(url_for('zones.list_zones'))
    
    # Get buildings in this zone
    cur.execute('''
        SELECT b.code_batiment, b.nom_batiment, b.adresse_rue,
               t.libelle_type, n.niveau,
               (SELECT i.etat_constate FROM INSPECTION i 
                WHERE i.code_batiment = b.code_batiment 
                ORDER BY i.date_visite DESC LIMIT 1) as dernier_etat
        FROM BATIMENT b
        LEFT JOIN TYPE_BATIMENT t ON b.id_type = t.id_type
        LEFT JOIN NIV_PROTECTION n ON b.id_protection = n.id_protection
        WHERE b.id_zone = %s
        ORDER BY b.nom_batiment
    ''', (id,))
    buildings = cur.fetchall()
    
    # Get statistics for this zone
    cur.execute('''
        SELECT 
            COUNT(*) as total,
            COUNT(CASE WHEN (SELECT i.etat_constate FROM INSPECTION i 
                            WHERE i.code_batiment = b.code_batiment 
                            ORDER BY i.date_visite DESC LIMIT 1) = 'Bon' THEN 1 END) as bon,
            COUNT(CASE WHEN (SELECT i.etat_constate FROM INSPECTION i 
                            WHERE i.code_batiment = b.code_batiment 
                            ORDER BY i.date_visite DESC LIMIT 1) = 'Moyen' THEN 1 END) as moyen,
            COUNT(CASE WHEN (SELECT i.etat_constate FROM INSPECTION i 
                            WHERE i.code_batiment = b.code_batiment 
                            ORDER BY i.date_visite DESC LIMIT 1) IN ('Dégradé', 'En ruine') THEN 1 END) as urgent
        FROM BATIMENT b
        WHERE b.id_zone = %s
    ''', (id,))
    stats = cur.fetchone()
    
    cur.close()
    
    return render_template('zones/view.html', 
                          zone=zone, 
                          buildings=buildings,
                          stats=stats)

@zones_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_zone(id):
    """Edit an existing zone."""
    conn = get_db()
    cur = conn.cursor()
    
    if request.method == 'POST':
        nom_zone = request.form['nom_zone']
        type_zone = request.form.get('type_zone') or None
        
        try:
            cur.execute('''
                UPDATE ZONE_URBAINE 
                SET nom_zone = %s, type_zone = %s
                WHERE id_zone = %s
            ''', (nom_zone, type_zone, id))
            conn.commit()
            cur.close()
            flash('Zone modifiée avec succès!', 'success')
            return redirect(url_for('zones.view_zone', id=id))
        except Exception as e:
            conn.rollback()
            flash(f'Erreur lors de la modification: {str(e)}', 'danger')
            # Don't close cursor here - we need it for the form below
    
    # GET or POST with error: Load zone data
    cur.execute('''
        SELECT id_zone, nom_zone, type_zone
        FROM ZONE_URBAINE
        WHERE id_zone = %s
    ''', (id,))
    zone = cur.fetchone()
    
    if not zone:
        cur.close()
        flash('Zone non trouvée!', 'warning')
        return redirect(url_for('zones.list_zones'))
    
    # Load existing types for suggestions
    cur.execute('SELECT DISTINCT type_zone FROM ZONE_URBAINE WHERE type_zone IS NOT NULL ORDER BY type_zone')
    existing_types = [t[0] for t in cur.fetchall()]
    cur.close()
    
    return render_template('zones/edit.html', zone=zone, existing_types=existing_types)

@zones_bp.route('/delete/<int:id>', methods=['POST'])
def delete_zone(id):
    """Delete a zone."""
    conn = get_db()
    cur = conn.cursor()
    
    try:
        # Check if zone has buildings
        cur.execute('SELECT COUNT(*) FROM BATIMENT WHERE id_zone = %s', (id,))
        count = cur.fetchone()[0]
        
        if count > 0:
            flash(f'Impossible de supprimer: cette zone contient {count} bâtiment(s).', 'danger')
            return redirect(url_for('zones.view_zone', id=id))
        
        cur.execute('DELETE FROM ZONE_URBAINE WHERE id_zone = %s', (id,))
        conn.commit()
        flash('Zone supprimée avec succès!', 'success')
    except Exception as e:
        conn.rollback()
        flash(f'Erreur: {str(e)}', 'danger')
    finally:
        cur.close()
    
    return redirect(url_for('zones.list_zones'))