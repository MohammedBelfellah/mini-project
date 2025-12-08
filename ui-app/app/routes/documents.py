from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.db import get_db

documents_bp = Blueprint('documents', __name__, url_prefix='/documents')

@documents_bp.route('/')
def list_all_documents():
    """List all documents with search and filtering."""
    conn = get_db()
    cur = conn.cursor()
    
    # Get filter parameters
    search = request.args.get('search', '').strip()
    type_filter = request.args.get('type_doc', '')
    building_filter = request.args.get('building', '')
    
    # Base query
    query = '''
        SELECT d.id_doc, d.titre_doc, d.type_doc, d.url_fichier, 
               d.code_batiment, b.nom_batiment
        FROM DOCUMENT_MEDIA d
        JOIN BATIMENT b ON d.code_batiment = b.code_batiment
        WHERE 1=1
    '''
    params = []
    
    if search:
        query += ' AND (LOWER(d.titre_doc) LIKE LOWER(%s) OR LOWER(b.nom_batiment) LIKE LOWER(%s))'
        params.extend([f'%{search}%', f'%{search}%'])
    
    if type_filter:
        query += ' AND d.type_doc = %s'
        params.append(type_filter)
    
    if building_filter:
        query += ' AND d.code_batiment = %s'
        params.append(building_filter)
    
    query += ' ORDER BY d.id_doc DESC'
    
    cur.execute(query, params)
    documents = cur.fetchall()
    
    # Get filter dropdown data
    cur.execute('SELECT DISTINCT type_doc FROM DOCUMENT_MEDIA WHERE type_doc IS NOT NULL ORDER BY type_doc')
    types = cur.fetchall()
    
    cur.execute('SELECT code_batiment, nom_batiment FROM BATIMENT ORDER BY nom_batiment')
    buildings = cur.fetchall()
    
    cur.close()
    
    return render_template('documents/list_all.html',
                          documents=documents,
                          types=types,
                          buildings=buildings,
                          current_search=search,
                          current_type=type_filter,
                          current_building=building_filter)

@documents_bp.route('/building/<int:building_id>')
def list_documents(building_id):
    """List documents for a building."""
    conn = get_db()
    cur = conn.cursor()
    
    cur.execute('SELECT nom_batiment FROM BATIMENT WHERE code_batiment = %s', (building_id,))
    building = cur.fetchone()
    
    if not building:
        flash('Bâtiment non trouvé!', 'warning')
        return redirect(url_for('buildings.list_buildings'))
    
    cur.execute('''
        SELECT id_doc, titre_doc, type_doc, url_fichier
        FROM DOCUMENT_MEDIA WHERE code_batiment = %s ORDER BY id_doc DESC
    ''', (building_id,))
    documents = cur.fetchall()
    cur.close()
    
    return render_template('documents/list.html', 
                          documents=documents, 
                          building_id=building_id,
                          building_name=building[0])

@documents_bp.route('/add/<int:building_id>', methods=['GET', 'POST'])
def add_document(building_id):
    """Add a document to a building."""
    conn = get_db()
    cur = conn.cursor()
    
    cur.execute('SELECT nom_batiment FROM BATIMENT WHERE code_batiment = %s', (building_id,))
    building = cur.fetchone()
    
    if not building:
        flash('Bâtiment non trouvé!', 'warning')
        return redirect(url_for('buildings.list_buildings'))
    
    if request.method == 'POST':
        titre = request.form['titre_doc']
        type_doc = request.form['type_doc']
        url_fichier = request.form['url_fichier']
        
        try:
            cur.execute('''
                INSERT INTO DOCUMENT_MEDIA (titre_doc, type_doc, url_fichier, code_batiment)
                VALUES (%s, %s, %s, %s)
            ''', (titre, type_doc, url_fichier, building_id))
            conn.commit()
            cur.close()
            flash('Document ajouté!', 'success')
            return redirect(url_for('buildings.view_building', id=building_id))
        except Exception as e:
            conn.rollback()
            flash(f'Erreur: {str(e)}', 'danger')
    
    cur.close()
    types = ['Photo', 'Plan', 'PDF', 'Vidéo', 'Autre']
    return render_template('documents/add.html', 
                          building_id=building_id, 
                          building_name=building[0],
                          types=types)

@documents_bp.route('/view/<int:id>')
def view_document(id):
    """View a document."""
    conn = get_db()
    cur = conn.cursor()
    
    cur.execute('''
        SELECT d.id_doc, d.titre_doc, d.type_doc, d.url_fichier, d.code_batiment,
               b.nom_batiment
        FROM DOCUMENT_MEDIA d
        JOIN BATIMENT b ON d.code_batiment = b.code_batiment
        WHERE d.id_doc = %s
    ''', (id,))
    document = cur.fetchone()
    cur.close()
    
    if not document:
        flash('Document non trouvé!', 'warning')
        return redirect(url_for('buildings.list_buildings'))
    
    return render_template('documents/view.html', 
                          document=document,
                          building_name=document[5])

@documents_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_document(id):
    """Edit a document."""
    conn = get_db()
    cur = conn.cursor()
    
    if request.method == 'POST':
        titre = request.form['titre_doc']
        type_doc = request.form['type_doc']
        url_fichier = request.form['url_fichier']
        
        try:
            cur.execute('''
                UPDATE DOCUMENT_MEDIA 
                SET titre_doc = %s, type_doc = %s, url_fichier = %s
                WHERE id_doc = %s
            ''', (titre, type_doc, url_fichier, id))
            conn.commit()
            cur.close()
            flash('Document modifié!', 'success')
            return redirect(url_for('documents.view_document', id=id))
        except Exception as e:
            conn.rollback()
            flash(f'Erreur: {str(e)}', 'danger')
    
    cur.execute('''
        SELECT d.id_doc, d.titre_doc, d.type_doc, d.url_fichier, d.code_batiment,
               b.nom_batiment
        FROM DOCUMENT_MEDIA d
        JOIN BATIMENT b ON d.code_batiment = b.code_batiment
        WHERE d.id_doc = %s
    ''', (id,))
    document = cur.fetchone()
    cur.close()
    
    if not document:
        flash('Document non trouvé!', 'warning')
        return redirect(url_for('buildings.list_buildings'))
    
    types = ['Photo', 'Plan', 'PDF', 'Vidéo', 'Autre']
    return render_template('documents/edit.html', 
                          document=document,
                          building_name=document[5],
                          types=types)

@documents_bp.route('/delete/<int:id>', methods=['POST'])
def delete_document(id):
    """Delete a document."""
    conn = get_db()
    cur = conn.cursor()
    
    cur.execute('SELECT code_batiment FROM DOCUMENT_MEDIA WHERE id_doc = %s', (id,))
    result = cur.fetchone()
    building_id = result[0] if result else None
    
    try:
        cur.execute('DELETE FROM DOCUMENT_MEDIA WHERE id_doc = %s', (id,))
        conn.commit()
        flash('Document supprimé!', 'success')
    except Exception as e:
        conn.rollback()
        flash(f'Erreur: {str(e)}', 'danger')
    finally:
        cur.close()
    
    if building_id:
        return redirect(url_for('buildings.view_building', id=building_id))
    return redirect(url_for('buildings.list_buildings'))

@documents_bp.route('/add', methods=['POST'])
def add_document_global():
    """Add a document from the global documents page."""
    conn = get_db()
    cur = conn.cursor()
    
    building_id = request.form['code_batiment']
    titre = request.form['titre_doc']
    type_doc = request.form['type_doc']
    url_fichier = request.form['url_fichier']
    
    try:
        cur.execute('''
            INSERT INTO DOCUMENT_MEDIA (titre_doc, type_doc, url_fichier, code_batiment)
            VALUES (%s, %s, %s, %s)
            RETURNING id_doc
        ''', (titre, type_doc, url_fichier, building_id))
        new_id = cur.fetchone()[0]
        conn.commit()
        flash(f'Document "{titre}" ajouté avec succès! (ID: {new_id})', 'success')
    except Exception as e:
        conn.rollback()
        flash(f'Erreur: {str(e)}', 'danger')
    finally:
        cur.close()
    
    return redirect(url_for('documents.list_all_documents'))