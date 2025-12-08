from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.db import get_db

types_bp = Blueprint('types', __name__, url_prefix='/types')

@types_bp.route('/')
def list_types():
    """List all building types."""
    conn = get_db()
    cur = conn.cursor()
    
    search = request.args.get('search', '').strip()
    
    query = '''
        SELECT t.id_type, t.libelle_type,
               COUNT(b.code_batiment) as nb_batiments
        FROM TYPE_BATIMENT t
        LEFT JOIN BATIMENT b ON t.id_type = b.id_type
        WHERE 1=1
    '''
    params = []
    
    if search:
        query += ' AND LOWER(t.libelle_type) LIKE LOWER(%s)'
        params.append(f'%{search}%')
    
    query += ' GROUP BY t.id_type, t.libelle_type ORDER BY t.libelle_type'
    
    cur.execute(query, params)
    types = cur.fetchall()
    cur.close()
    
    return render_template('types/list.html', types=types, current_search=search)

@types_bp.route('/add', methods=['GET', 'POST'])
def add_type():
    """Add a new building type."""
    conn = get_db()
    cur = conn.cursor()
    
    if request.method == 'POST':
        libelle_type = request.form['libelle_type']
        
        try:
            cur.execute('''
                INSERT INTO TYPE_BATIMENT (libelle_type)
                VALUES (%s)
                RETURNING id_type
            ''', (libelle_type,))
            new_id = cur.fetchone()[0]
            conn.commit()
            cur.close()
            flash(f'Type "{libelle_type}" ajouté avec succès! (ID: {new_id})', 'success')
            return redirect(url_for('types.list_types'))
        except Exception as e:
            conn.rollback()
            flash(f'Erreur: {str(e)}', 'danger')
    
    cur.close()
    return render_template('types/add.html')

@types_bp.route('/view/<int:id>')
def view_type(id):
    """View building type details with its buildings."""
    conn = get_db()
    cur = conn.cursor()
    
    # Get type details
    cur.execute('''
        SELECT id_type, libelle_type
        FROM TYPE_BATIMENT
        WHERE id_type = %s
    ''', (id,))
    type_bat = cur.fetchone()
    
    if not type_bat:
        flash('Type non trouvé!', 'warning')
        return redirect(url_for('types.list_types'))
    
    # Get buildings with this type
    cur.execute('''
        SELECT b.code_batiment, b.nom_batiment, b.adresse_rue,
               z.nom_zone, n.niveau,
               (SELECT i.etat_constate FROM INSPECTION i 
                WHERE i.code_batiment = b.code_batiment 
                ORDER BY i.date_visite DESC LIMIT 1) as dernier_etat
        FROM BATIMENT b
        LEFT JOIN ZONE_URBAINE z ON b.id_zone = z.id_zone
        LEFT JOIN NIV_PROTECTION n ON b.id_protection = n.id_protection
        WHERE b.id_type = %s
        ORDER BY b.nom_batiment
    ''', (id,))
    buildings = cur.fetchall()
    
    # Get statistics
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
        WHERE b.id_type = %s
    ''', (id,))
    stats = cur.fetchone()
    
    cur.close()
    
    return render_template('types/view.html', 
                          type_bat=type_bat, 
                          buildings=buildings,
                          stats=stats)

@types_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_type(id):
    """Edit a building type."""
    conn = get_db()
    cur = conn.cursor()
    
    if request.method == 'POST':
        libelle_type = request.form['libelle_type']
        
        try:
            cur.execute('UPDATE TYPE_BATIMENT SET libelle_type = %s WHERE id_type = %s', 
                       (libelle_type, id))
            conn.commit()
            cur.close()
            flash('Type modifié avec succès!', 'success')
            return redirect(url_for('types.view_type', id=id))
        except Exception as e:
            conn.rollback()
            flash(f'Erreur: {str(e)}', 'danger')
    
    cur.execute('SELECT id_type, libelle_type FROM TYPE_BATIMENT WHERE id_type = %s', (id,))
    type_bat = cur.fetchone()
    cur.close()
    
    if not type_bat:
        flash('Type non trouvé!', 'warning')
        return redirect(url_for('types.list_types'))
    
    return render_template('types/edit.html', type_bat=type_bat)

@types_bp.route('/delete/<int:id>', methods=['POST'])
def delete_type(id):
    """Delete a building type."""
    conn = get_db()
    cur = conn.cursor()
    
    try:
        cur.execute('SELECT COUNT(*) FROM BATIMENT WHERE id_type = %s', (id,))
        count = cur.fetchone()[0]
        
        if count > 0:
            flash(f'Impossible: ce type est utilisé par {count} bâtiment(s).', 'danger')
            return redirect(url_for('types.view_type', id=id))
        
        cur.execute('DELETE FROM TYPE_BATIMENT WHERE id_type = %s', (id,))
        conn.commit()
        flash('Type supprimé!', 'success')
    except Exception as e:
        conn.rollback()
        flash(f'Erreur: {str(e)}', 'danger')
    finally:
        cur.close()
    
    return redirect(url_for('types.list_types'))