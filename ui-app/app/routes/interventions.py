from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.db import get_db

interventions_bp = Blueprint('interventions', __name__, url_prefix='/interventions')

@interventions_bp.route('/')
def list_interventions():
    """List all interventions."""
    conn = get_db()
    cur = conn.cursor()
    cur.execute('''
        SELECT i.id_interv, i.date_debut, i.date_fin, i.type_travaux, 
               i.cout_estime, i.est_validee, i.statut_travaux,
               b.nom_batiment, b.code_batiment,
               p.nom_entreprise
        FROM INTERVENTION i
        JOIN BATIMENT b ON i.code_batiment = b.code_batiment
        JOIN PRESTATAIRE p ON i.id_prestataire = p.id_prestataire
        ORDER BY i.date_debut DESC
    ''')
    interventions = cur.fetchall()
    cur.close()
    return render_template('interventions/list.html', interventions=interventions)

@interventions_bp.route('/add', methods=['GET', 'POST'])
def add_intervention():
    """Add a new intervention."""
    conn = get_db()
    cur = conn.cursor()
    
    if request.method == 'POST':
        date_debut = request.form.get('date_debut') or None
        date_fin = request.form.get('date_fin') or None
        type_travaux = request.form.get('type_travaux')
        cout_estime = request.form.get('cout_estime') or None
        code_batiment = request.form['code_batiment']
        id_prestataire = request.form['id_prestataire']
        statut_travaux = request.form.get('statut_travaux', 'Planifié')
        
        try:
            cur.execute('''
                INSERT INTO INTERVENTION (date_debut, date_fin, type_travaux, 
                                          cout_estime, code_batiment, id_prestataire, statut_travaux)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            ''', (date_debut, date_fin, type_travaux, cout_estime, 
                  code_batiment, id_prestataire, statut_travaux))
            conn.commit()
            flash('Intervention ajoutée avec succès!', 'success')
            return redirect(url_for('interventions.list_interventions'))
        except Exception as e:
            conn.rollback()
            flash(f'Erreur: {str(e)}', 'danger')
        finally:
            cur.close()
    
    # GET: Load dropdowns
    cur.execute('SELECT code_batiment, nom_batiment FROM BATIMENT ORDER BY nom_batiment')
    buildings = cur.fetchall()
    cur.execute('SELECT id_prestataire, nom_entreprise, role_prest FROM PRESTATAIRE ORDER BY nom_entreprise')
    prestataires = cur.fetchall()
    cur.close()
    
    statuts = ['Planifié', 'En cours', 'Terminé', 'Annulé']
    return render_template('interventions/add.html', 
                          buildings=buildings, 
                          prestataires=prestataires, 
                          statuts=statuts)

@interventions_bp.route('/view/<int:id>')
def view_intervention(id):
    """View intervention details."""
    conn = get_db()
    cur = conn.cursor()
    
    cur.execute('''
        SELECT i.id_interv, i.date_debut, i.date_fin, i.type_travaux, 
               i.cout_estime, i.est_validee, i.statut_travaux,
               i.code_batiment, i.id_prestataire, i.date_validation,
               i.commentaire_validation,
               b.nom_batiment, b.adresse_rue,
               p.nom_entreprise, p.role_prest
        FROM INTERVENTION i
        JOIN BATIMENT b ON i.code_batiment = b.code_batiment
        JOIN PRESTATAIRE p ON i.id_prestataire = p.id_prestataire
        WHERE i.id_interv = %s
    ''', (id,))
    intervention = cur.fetchone()
    cur.close()
    
    if not intervention:
        flash('Intervention non trouvée!', 'warning')
        return redirect(url_for('interventions.list_interventions'))
    
    return render_template('interventions/view.html', intervention=intervention)

@interventions_bp.route('/validate/<int:id>', methods=['POST'])
def validate_intervention(id):
    """Validate an intervention (municipal service approval)."""
    conn = get_db()
    cur = conn.cursor()
    
    commentaire = request.form.get('commentaire_validation', '')
    
    try:
        cur.execute('''
            UPDATE INTERVENTION 
            SET est_validee = TRUE, 
                date_validation = CURRENT_DATE,
                commentaire_validation = %s
            WHERE id_interv = %s
        ''', (commentaire, id))
        conn.commit()
        flash('Intervention validée avec succès!', 'success')
    except Exception as e:
        conn.rollback()
        flash(f'Erreur: {str(e)}', 'danger')
    finally:
        cur.close()
    
    return redirect(url_for('interventions.view_intervention', id=id))

@interventions_bp.route('/delete/<int:id>', methods=['POST'])
def delete_intervention(id):
    """Delete an intervention."""
    conn = get_db()
    cur = conn.cursor()
    
    try:
        cur.execute('DELETE FROM INTERVENTION WHERE id_interv = %s', (id,))
        conn.commit()
        flash('Intervention supprimée!', 'success')
    except Exception as e:
        conn.rollback()
        flash(f'Erreur: {str(e)}', 'danger')
    finally:
        cur.close()
    
    return redirect(url_for('interventions.list_interventions'))