from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.db import get_db

inspections_bp = Blueprint('inspections', __name__, url_prefix='/inspections')

@inspections_bp.route('/')
def list_inspections():
    """List all inspections with search and filtering."""
    conn = get_db()
    cur = conn.cursor()
    
    # Get filter parameters
    search = request.args.get('search', '').strip()
    etat_filter = request.args.get('etat', '')
    building_filter = request.args.get('building', '')
    date_from = request.args.get('date_from', '')
    date_to = request.args.get('date_to', '')
    
    # Base query
    query = '''
        SELECT i.id_inspect, i.date_visite, i.etat_constate, i.rapport,
               b.code_batiment, b.nom_batiment, b.adresse_rue
        FROM INSPECTION i
        JOIN BATIMENT b ON i.code_batiment = b.code_batiment
        WHERE 1=1
    '''
    
    params = []
    
    # Search
    if search:
        query += ''' AND (
            LOWER(b.nom_batiment) LIKE LOWER(%s) OR 
            LOWER(i.rapport) LIKE LOWER(%s) OR
            CAST(i.id_inspect AS TEXT) LIKE %s
        )'''
        search_param = f'%{search}%'
        params.extend([search_param, search_param, search_param])
    
    # État filter
    if etat_filter:
        query += ' AND i.etat_constate = %s'
        params.append(etat_filter)
    
    # Building filter
    if building_filter:
        query += ' AND i.code_batiment = %s'
        params.append(building_filter)
    
    # Date range
    if date_from:
        query += ' AND i.date_visite >= %s'
        params.append(date_from)
    
    if date_to:
        query += ' AND i.date_visite <= %s'
        params.append(date_to)
    
    query += ' ORDER BY i.date_visite DESC'
    
    cur.execute(query, params)
    inspections = cur.fetchall()
    
    # Get filter dropdown data
    cur.execute('SELECT DISTINCT etat_constate FROM INSPECTION WHERE etat_constate IS NOT NULL ORDER BY etat_constate')
    etats = cur.fetchall()
    
    cur.execute('SELECT code_batiment, nom_batiment FROM BATIMENT ORDER BY nom_batiment')
    buildings = cur.fetchall()
    
    cur.close()
    
    return render_template('inspections/list.html',
                          inspections=inspections,
                          etats=etats,
                          buildings=buildings,
                          current_search=search,
                          current_etat=etat_filter,
                          current_building=building_filter,
                          current_date_from=date_from,
                          current_date_to=date_to)

@inspections_bp.route('/add', methods=['GET', 'POST'])
def add_inspection():
    """Add a new inspection."""
    conn = get_db()
    cur = conn.cursor()
    
    if request.method == 'POST':
        date_visite = request.form['date_visite']
        rapport = request.form.get('rapport')
        etat_constate = request.form['etat_constate']
        code_batiment = request.form['code_batiment']
        
        try:
            cur.execute('''
                INSERT INTO INSPECTION (date_visite, rapport, etat_constate, code_batiment)
                VALUES (%s, %s, %s, %s)
            ''', (date_visite, rapport, etat_constate, code_batiment))
            conn.commit()
            flash('Inspection ajoutée avec succès!', 'success')
            return redirect(url_for('inspections.list_inspections'))
        except Exception as e:
            conn.rollback()
            flash(f'Erreur lors de l\'ajout: {str(e)}', 'danger')
        finally:
            cur.close()
    
    # GET: Load buildings for dropdown
    cur.execute('SELECT code_batiment, nom_batiment FROM BATIMENT ORDER BY nom_batiment')
    buildings = cur.fetchall()
    cur.close()
    
    etats = ['Bon', 'Moyen', 'Dégradé', 'En ruine']
    return render_template('inspections/add.html', buildings=buildings, etats=etats)

@inspections_bp.route('/view/<int:id>')
def view_inspection(id):
    """View inspection details."""
    conn = get_db()
    cur = conn.cursor()
    
    cur.execute('''
        SELECT i.*, b.nom_batiment, b.adresse_rue
        FROM INSPECTION i
        JOIN BATIMENT b ON i.code_batiment = b.code_batiment
        WHERE i.id_inspect = %s
    ''', (id,))
    inspection = cur.fetchone()
    cur.close()
    
    if not inspection:
        flash('Inspection non trouvée!', 'warning')
        return redirect(url_for('inspections.list_inspections'))
    
    return render_template('inspections/view.html', inspection=inspection)

@inspections_bp.route('/delete/<int:id>', methods=['POST'])
def delete_inspection(id):
    """Delete an inspection."""
    conn = get_db()
    cur = conn.cursor()
    
    try:
        cur.execute('DELETE FROM INSPECTION WHERE id_inspect = %s', (id,))
        conn.commit()
        flash('Inspection supprimée!', 'success')
    except Exception as e:
        conn.rollback()
        flash(f'Erreur: {str(e)}', 'danger')
    finally:
        cur.close()
    
    return redirect(url_for('inspections.list_inspections'))