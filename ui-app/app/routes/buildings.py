from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.db import get_db

buildings_bp = Blueprint('buildings', __name__, url_prefix='/buildings')

@buildings_bp.route('/')
def list_buildings():
    """List all buildings with their details."""
    conn = get_db()
    cur = conn.cursor()
    cur.execute('''
        SELECT b.code_batiment, b.nom_batiment, b.adresse_rue, 
               z.nom_zone, t.libelle_type, n.niveau, p.nom_complet,
               b.latitude, b.longitude
        FROM BATIMENT b
        LEFT JOIN ZONE_URBAINE z ON b.id_zone = z.id_zone
        LEFT JOIN TYPE_BATIMENT t ON b.id_type = t.id_type
        LEFT JOIN NIV_PROTECTION n ON b.id_protection = n.id_protection
        LEFT JOIN PROPRIETAIRE p ON b.id_proprio = p.id_proprio
        ORDER BY b.code_batiment DESC
    ''')
    buildings = cur.fetchall()
    cur.close()
    return render_template('buildings/list.html', buildings=buildings)

@buildings_bp.route('/add', methods=['GET', 'POST'])
def add_building():
    """Add a new building."""
    conn = get_db()
    cur = conn.cursor()
    
    if request.method == 'POST':
        # Get form data
        nom = request.form['nom_batiment']
        adresse = request.form['adresse_rue']
        latitude = request.form.get('latitude') or None
        longitude = request.form.get('longitude') or None
        date_construction = request.form.get('date_construction') or None
        note = request.form.get('note_historique')
        id_zone = request.form.get('id_zone') or None
        id_type = request.form.get('id_type') or None
        id_protection = request.form.get('id_protection') or None
        id_proprio = request.form.get('id_proprio') or None
        
        try:
            cur.execute('''
                INSERT INTO BATIMENT (nom_batiment, adresse_rue, latitude, longitude, 
                                      date_construction, note_historique, id_zone, 
                                      id_type, id_protection, id_proprio)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ''', (nom, adresse, latitude, longitude, date_construction, note,
                  id_zone, id_type, id_protection, id_proprio))
            
            # Update geometry if coordinates provided
            if latitude and longitude:
                cur.execute('''
                    UPDATE BATIMENT 
                    SET geom = ST_SetSRID(ST_MakePoint(%s, %s), 4326)
                    WHERE code_batiment = (SELECT MAX(code_batiment) FROM BATIMENT)
                ''', (longitude, latitude))
            
            conn.commit()
            flash('Bâtiment ajouté avec succès!', 'success')
            return redirect(url_for('buildings.list_buildings'))
        except Exception as e:
            conn.rollback()
            flash(f'Erreur lors de l\'ajout: {str(e)}', 'danger')
        finally:
            cur.close()
    
    # GET: Load dropdown data
    cur.execute('SELECT id_zone, nom_zone FROM ZONE_URBAINE ORDER BY nom_zone')
    zones = cur.fetchall()
    cur.execute('SELECT id_type, libelle_type FROM TYPE_BATIMENT ORDER BY libelle_type')
    types = cur.fetchall()
    cur.execute('SELECT id_protection, niveau FROM NIV_PROTECTION ORDER BY niveau')
    protections = cur.fetchall()
    cur.execute('SELECT id_proprio, nom_complet FROM PROPRIETAIRE ORDER BY nom_complet')
    proprietaires = cur.fetchall()
    cur.close()
    
    return render_template('buildings/add.html', zones=zones, types=types, 
                          protections=protections, proprietaires=proprietaires)

@buildings_bp.route('/view/<int:id>')
def view_building(id):
    """View a single building with all details."""
    conn = get_db()
    cur = conn.cursor()
    
    # Get building details
    cur.execute('''
        SELECT b.code_batiment, b.nom_batiment, b.adresse_rue, 
               b.latitude, b.longitude, b.date_construction, b.note_historique,
               z.nom_zone, t.libelle_type, n.niveau, p.nom_complet, p.type_proprio
        FROM BATIMENT b
        LEFT JOIN ZONE_URBAINE z ON b.id_zone = z.id_zone
        LEFT JOIN TYPE_BATIMENT t ON b.id_type = t.id_type
        LEFT JOIN NIV_PROTECTION n ON b.id_protection = n.id_protection
        LEFT JOIN PROPRIETAIRE p ON b.id_proprio = p.id_proprio
        WHERE b.code_batiment = %s
    ''', (id,))
    building = cur.fetchone()
    
    if not building:
        flash('Bâtiment non trouvé!', 'warning')
        return redirect(url_for('buildings.list_buildings'))
    
    # Get inspections for this building
    cur.execute('''
        SELECT id_inspect, date_visite, etat_constate, rapport
        FROM INSPECTION 
        WHERE code_batiment = %s 
        ORDER BY date_visite DESC
    ''', (id,))
    inspections = cur.fetchall()
    
    # Get interventions for this building
    cur.execute('''
        SELECT i.id_interv, i.date_debut, i.date_fin, i.type_travaux, 
               i.cout_estime, i.est_validee, i.statut_travaux,
               p.nom_entreprise, p.role_prest
        FROM INTERVENTION i
        LEFT JOIN PRESTATAIRE p ON i.id_prestataire = p.id_prestataire
        WHERE i.code_batiment = %s 
        ORDER BY i.date_debut DESC
    ''', (id,))
    interventions = cur.fetchall()
    
    # Get documents/media for this building
    cur.execute('''
        SELECT id_doc, titre_doc, type_doc, url_fichier
        FROM DOCUMENT_MEDIA
        WHERE code_batiment = %s
        ORDER BY id_doc DESC
    ''', (id,))
    documents = cur.fetchall()
    
    cur.close()
    return render_template('buildings/view.html', 
                          building=building, 
                          inspections=inspections, 
                          interventions=interventions,
                          documents=documents)

@buildings_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_building(id):
    """Edit an existing building."""
    conn = get_db()
    cur = conn.cursor()
    
    if request.method == 'POST':
        nom = request.form['nom_batiment']
        adresse = request.form['adresse_rue']
        latitude = request.form.get('latitude') or None
        longitude = request.form.get('longitude') or None
        date_construction = request.form.get('date_construction') or None
        note = request.form.get('note_historique')
        id_zone = request.form.get('id_zone') or None
        id_type = request.form.get('id_type') or None
        id_protection = request.form.get('id_protection') or None
        id_proprio = request.form.get('id_proprio') or None
        
        try:
            cur.execute('''
                UPDATE BATIMENT 
                SET nom_batiment = %s, adresse_rue = %s, latitude = %s, 
                    longitude = %s, date_construction = %s, note_historique = %s,
                    id_zone = %s, id_type = %s, id_protection = %s, id_proprio = %s
                WHERE code_batiment = %s
            ''', (nom, adresse, latitude, longitude, date_construction, note,
                  id_zone, id_type, id_protection, id_proprio, id))
            
            # Update geometry if coordinates changed
            if latitude and longitude:
                cur.execute('''
                    UPDATE BATIMENT 
                    SET geom = ST_SetSRID(ST_MakePoint(%s, %s), 4326)
                    WHERE code_batiment = %s
                ''', (longitude, latitude, id))
            
            conn.commit()
            flash('Bâtiment modifié avec succès!', 'success')
            return redirect(url_for('buildings.view_building', id=id))
        except Exception as e:
            conn.rollback()
            flash(f'Erreur lors de la modification: {str(e)}', 'danger')
        finally:
            cur.close()
    
    # GET: Load building data and dropdown options
    cur.execute('''
        SELECT b.*, z.id_zone, t.id_type, n.id_protection, p.id_proprio
        FROM BATIMENT b
        LEFT JOIN ZONE_URBAINE z ON b.id_zone = z.id_zone
        LEFT JOIN TYPE_BATIMENT t ON b.id_type = t.id_type
        LEFT JOIN NIV_PROTECTION n ON b.id_protection = n.id_protection
        LEFT JOIN PROPRIETAIRE p ON b.id_proprio = p.id_proprio
        WHERE b.code_batiment = %s
    ''', (id,))
    building = cur.fetchone()
    
    if not building:
        flash('Bâtiment non trouvé!', 'warning')
        return redirect(url_for('buildings.list_buildings'))
    
    cur.execute('SELECT id_zone, nom_zone FROM ZONE_URBAINE ORDER BY nom_zone')
    zones = cur.fetchall()
    cur.execute('SELECT id_type, libelle_type FROM TYPE_BATIMENT ORDER BY libelle_type')
    types = cur.fetchall()
    cur.execute('SELECT id_protection, niveau FROM NIV_PROTECTION ORDER BY niveau')
    protections = cur.fetchall()
    cur.execute('SELECT id_proprio, nom_complet FROM PROPRIETAIRE ORDER BY nom_complet')
    proprietaires = cur.fetchall()
    cur.close()
    
    return render_template('buildings/edit.html', 
                          building=building,
                          zones=zones, 
                          types=types, 
                          protections=protections, 
                          proprietaires=proprietaires)

@buildings_bp.route('/delete/<int:id>', methods=['POST'])
def delete_building(id):
    """Delete a building."""
    conn = get_db()
    cur = conn.cursor()
    
    try:
        # Delete related records first (due to foreign keys)
        cur.execute('DELETE FROM DOCUMENT_MEDIA WHERE code_batiment = %s', (id,))
        cur.execute('DELETE FROM INTERVENTION WHERE code_batiment = %s', (id,))
        cur.execute('DELETE FROM INSPECTION WHERE code_batiment = %s', (id,))
        cur.execute('DELETE FROM BATIMENT WHERE code_batiment = %s', (id,))
        conn.commit()
        flash('Bâtiment supprimé avec succès!', 'success')
    except Exception as e:
        conn.rollback()
        flash(f'Erreur lors de la suppression: {str(e)}', 'danger')
    finally:
        cur.close()
    
    return redirect(url_for('buildings.list_buildings'))