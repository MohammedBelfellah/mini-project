from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.db import get_db

inspections_bp = Blueprint('inspections', __name__, url_prefix='/inspections')

@inspections_bp.route('/')
def list_inspections():
    """List all inspections."""
    conn = get_db()
    cur = conn.cursor()
    cur.execute('''
        SELECT i.id_inspect, i.date_visite, i.etat_constate, 
               b.nom_batiment, b.code_batiment,
               SUBSTRING(i.rapport, 1, 100) as rapport_preview
        FROM INSPECTION i
        JOIN BATIMENT b ON i.code_batiment = b.code_batiment
        ORDER BY i.date_visite DESC
    ''')
    inspections = cur.fetchall()
    cur.close()
    return render_template('inspections/list.html', inspections=inspections)

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