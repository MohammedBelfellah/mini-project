from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.db import get_db

proprietaires_bp = Blueprint('proprietaires', __name__, url_prefix='/proprietaires')

@proprietaires_bp.route('/')
def list_proprietaires():
    """List all proprietaires with search and filtering."""
    conn = get_db()
    cur = conn.cursor()
    
    # Get filter parameters
    search = request.args.get('search', '').strip()
    type_filter = request.args.get('type_proprio', '')
    
    # Base query with building count
    query = '''
        SELECT p.id_proprio, p.nom_complet, p.type_proprio, p.contact,
               COUNT(b.code_batiment) as nb_batiments
        FROM PROPRIETAIRE p
        LEFT JOIN BATIMENT b ON p.id_proprio = b.id_proprio
        WHERE 1=1
    '''
    
    params = []
    
    # Search
    if search:
        query += ''' AND (
            LOWER(p.nom_complet) LIKE LOWER(%s) OR 
            LOWER(p.contact) LIKE LOWER(%s)
        )'''
        search_param = f'%{search}%'
        params.extend([search_param, search_param])
    
    # Type filter
    if type_filter:
        query += ' AND p.type_proprio = %s'
        params.append(type_filter)
    
    query += ' GROUP BY p.id_proprio, p.nom_complet, p.type_proprio, p.contact'
    query += ' ORDER BY p.nom_complet'
    
    cur.execute(query, params)
    proprietaires = cur.fetchall()
    
    # Get distinct types for filter dropdown
    cur.execute('SELECT DISTINCT type_proprio FROM PROPRIETAIRE WHERE type_proprio IS NOT NULL ORDER BY type_proprio')
    types = cur.fetchall()
    
    cur.close()
    
    return render_template('proprietaires/list.html',
                          proprietaires=proprietaires,
                          types=types,
                          current_search=search,
                          current_type=type_filter)

@proprietaires_bp.route('/add', methods=['GET', 'POST'])
def add_proprietaire():
    """Add a new proprietaire."""
    conn = get_db()
    cur = conn.cursor()
    
    if request.method == 'POST':
        nom_complet = request.form['nom_complet']
        type_proprio = request.form.get('type_proprio') or None
        contact = request.form.get('contact') or None
        
        try:
            cur.execute('''
                INSERT INTO PROPRIETAIRE (nom_complet, type_proprio, contact)
                VALUES (%s, %s, %s)
                RETURNING id_proprio
            ''', (nom_complet, type_proprio, contact))
            new_id = cur.fetchone()[0]
            conn.commit()
            flash(f'Propriétaire "{nom_complet}" ajouté avec succès! (ID: {new_id})', 'success')
            return redirect(url_for('proprietaires.list_proprietaires'))
        except Exception as e:
            conn.rollback()
            flash(f'Erreur lors de l\'ajout: {str(e)}', 'danger')
        # Don't close cursor here - we need it for GET request fallback
    
    # GET: Load existing types for suggestions
    cur.execute('SELECT DISTINCT type_proprio FROM PROPRIETAIRE WHERE type_proprio IS NOT NULL ORDER BY type_proprio')
    existing_types = [t[0] for t in cur.fetchall()]
    cur.close()
    
    return render_template('proprietaires/add.html', existing_types=existing_types)

@proprietaires_bp.route('/view/<int:id>')
def view_proprietaire(id):
    """View proprietaire details with their buildings."""
    conn = get_db()
    cur = conn.cursor()
    
    # Get proprietaire details
    cur.execute('''
        SELECT id_proprio, nom_complet, type_proprio, contact
        FROM PROPRIETAIRE
        WHERE id_proprio = %s
    ''', (id,))
    proprietaire = cur.fetchone()
    
    if not proprietaire:
        flash('Propriétaire non trouvé!', 'warning')
        return redirect(url_for('proprietaires.list_proprietaires'))
    
    # Get buildings owned by this proprietaire
    cur.execute('''
        SELECT b.code_batiment, b.nom_batiment, b.adresse_rue,
               z.nom_zone, t.libelle_type
        FROM BATIMENT b
        LEFT JOIN ZONE_URBAINE z ON b.id_zone = z.id_zone
        LEFT JOIN TYPE_BATIMENT t ON b.id_type = t.id_type
        WHERE b.id_proprio = %s
        ORDER BY b.nom_batiment
    ''', (id,))
    buildings = cur.fetchall()
    
    cur.close()
    
    return render_template('proprietaires/view.html', 
                          proprietaire=proprietaire, 
                          buildings=buildings)

@proprietaires_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_proprietaire(id):
    """Edit an existing proprietaire."""
    conn = get_db()
    cur = conn.cursor()
    
    if request.method == 'POST':
        nom_complet = request.form['nom_complet']
        type_proprio = request.form.get('type_proprio') or None
        contact = request.form.get('contact') or None
        
        try:
            cur.execute('''
                UPDATE PROPRIETAIRE 
                SET nom_complet = %s, type_proprio = %s, contact = %s
                WHERE id_proprio = %s
            ''', (nom_complet, type_proprio, contact, id))
            conn.commit()
            flash('Propriétaire modifié avec succès!', 'success')
            return redirect(url_for('proprietaires.view_proprietaire', id=id))
        except Exception as e:
            conn.rollback()
            flash(f'Erreur lors de la modification: {str(e)}', 'danger')
        finally:
            cur.close()
    
    # GET: Load proprietaire data
    cur.execute('''
        SELECT id_proprio, nom_complet, type_proprio, contact
        FROM PROPRIETAIRE
        WHERE id_proprio = %s
    ''', (id,))
    proprietaire = cur.fetchone()
    
    if not proprietaire:
        flash('Propriétaire non trouvé!', 'warning')
        return redirect(url_for('proprietaires.list_proprietaires'))
    
    # Load existing types for suggestions
    cur.execute('SELECT DISTINCT type_proprio FROM PROPRIETAIRE WHERE type_proprio IS NOT NULL ORDER BY type_proprio')
    existing_types = [t[0] for t in cur.fetchall()]
    cur.close()
    
    return render_template('proprietaires/edit.html', proprietaire=proprietaire, existing_types=existing_types)

@proprietaires_bp.route('/delete/<int:id>', methods=['POST'])
def delete_proprietaire(id):
    """Delete a proprietaire."""
    conn = get_db()
    cur = conn.cursor()
    
    try:
        # Check if proprietaire has buildings
        cur.execute('SELECT COUNT(*) FROM BATIMENT WHERE id_proprio = %s', (id,))
        count = cur.fetchone()[0]
        
        if count > 0:
            flash(f'Impossible de supprimer: ce propriétaire possède {count} bâtiment(s).', 'danger')
            return redirect(url_for('proprietaires.view_proprietaire', id=id))
        
        cur.execute('DELETE FROM PROPRIETAIRE WHERE id_proprio = %s', (id,))
        conn.commit()
        flash('Propriétaire supprimé avec succès!', 'success')
    except Exception as e:
        conn.rollback()
        flash(f'Erreur: {str(e)}', 'danger')
    finally:
        cur.close()
    
    return redirect(url_for('proprietaires.list_proprietaires'))