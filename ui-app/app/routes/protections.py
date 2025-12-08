from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.db import get_db

protections_bp = Blueprint('protections', __name__, url_prefix='/protections')

@protections_bp.route('/')
def list_protections():
    """List all protection levels with building count."""
    conn = get_db()
    cur = conn.cursor()
    
    # Get filter parameters
    search = request.args.get('search', '').strip()
    
    # Base query with building count
    query = '''
        SELECT n.id_protection, n.niveau,
               COUNT(b.code_batiment) as nb_batiments
        FROM NIV_PROTECTION n
        LEFT JOIN BATIMENT b ON n.id_protection = b.id_protection
        WHERE 1=1
    '''
    
    params = []
    
    if search:
        query += ' AND LOWER(n.niveau) LIKE LOWER(%s)'
        params.append(f'%{search}%')
    
    query += ' GROUP BY n.id_protection, n.niveau'
    query += ' ORDER BY n.niveau'
    
    cur.execute(query, params)
    protections = cur.fetchall()
    cur.close()
    
    return render_template('protections/list.html',
                          protections=protections,
                          current_search=search)

@protections_bp.route('/add', methods=['GET', 'POST'])
def add_protection():
    """Add a new protection level."""
    conn = get_db()
    cur = conn.cursor()
    
    if request.method == 'POST':
        niveau = request.form['niveau']
        
        try:
            cur.execute('''
                INSERT INTO NIV_PROTECTION (niveau)
                VALUES (%s)
                RETURNING id_protection
            ''', (niveau,))
            new_id = cur.fetchone()[0]
            conn.commit()
            flash(f'Niveau de protection "{niveau}" ajouté avec succès! (ID: {new_id})', 'success')
            return redirect(url_for('protections.list_protections'))
        except Exception as e:
            conn.rollback()
            flash(f'Erreur lors de l\'ajout: {str(e)}', 'danger')
        finally:
            cur.close()
    
    return render_template('protections/add.html')

@protections_bp.route('/view/<int:id>')
def view_protection(id):
    """View protection level details with its buildings."""
    conn = get_db()
    cur = conn.cursor()
    
    # Get protection details
    cur.execute('''
        SELECT id_protection, niveau
        FROM NIV_PROTECTION
        WHERE id_protection = %s
    ''', (id,))
    protection = cur.fetchone()
    
    if not protection:
        flash('Niveau de protection non trouvé!', 'warning')
        return redirect(url_for('protections.list_protections'))
    
    # Get buildings with this protection level
    cur.execute('''
        SELECT b.code_batiment, b.nom_batiment, b.adresse_rue,
               z.nom_zone, t.libelle_type,
               (SELECT i.etat_constate FROM INSPECTION i 
                WHERE i.code_batiment = b.code_batiment 
                ORDER BY i.date_visite DESC LIMIT 1) as dernier_etat
        FROM BATIMENT b
        LEFT JOIN ZONE_URBAINE z ON b.id_zone = z.id_zone
        LEFT JOIN TYPE_BATIMENT t ON b.id_type = t.id_type
        WHERE b.id_protection = %s
        ORDER BY b.nom_batiment
    ''', (id,))
    buildings = cur.fetchall()
    
    cur.close()
    
    return render_template('protections/view.html', 
                          protection=protection, 
                          buildings=buildings)

@protections_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_protection(id):
    """Edit an existing protection level."""
    conn = get_db()
    cur = conn.cursor()
    
    if request.method == 'POST':
        niveau = request.form['niveau']
        
        try:
            cur.execute('''
                UPDATE NIV_PROTECTION 
                SET niveau = %s
                WHERE id_protection = %s
            ''', (niveau, id))
            conn.commit()
            flash('Niveau de protection modifié avec succès!', 'success')
            return redirect(url_for('protections.view_protection', id=id))
        except Exception as e:
            conn.rollback()
            flash(f'Erreur lors de la modification: {str(e)}', 'danger')
        finally:
            cur.close()
    
    # GET: Load protection data
    cur.execute('''
        SELECT id_protection, niveau
        FROM NIV_PROTECTION
        WHERE id_protection = %s
    ''', (id,))
    protection = cur.fetchone()
    
    if not protection:
        flash('Niveau de protection non trouvé!', 'warning')
        return redirect(url_for('protections.list_protections'))
    
    cur.close()
    
    return render_template('protections/edit.html', protection=protection)

@protections_bp.route('/delete/<int:id>', methods=['POST'])
def delete_protection(id):
    """Delete a protection level."""
    conn = get_db()
    cur = conn.cursor()
    
    try:
        # Check if protection level has buildings
        cur.execute('SELECT COUNT(*) FROM BATIMENT WHERE id_protection = %s', (id,))
        count = cur.fetchone()[0]
        
        if count > 0:
            flash(f'Impossible de supprimer: ce niveau de protection est utilisé par {count} bâtiment(s).', 'danger')
            return redirect(url_for('protections.view_protection', id=id))
        
        cur.execute('DELETE FROM NIV_PROTECTION WHERE id_protection = %s', (id,))
        conn.commit()
        flash('Niveau de protection supprimé avec succès!', 'success')
    except Exception as e:
        conn.rollback()
        flash(f'Erreur: {str(e)}', 'danger')
    finally:
        cur.close()
    
    return redirect(url_for('protections.list_protections'))