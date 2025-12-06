from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.db import get_db

prestataires_bp = Blueprint('prestataires', __name__, url_prefix='/prestataires')

@prestataires_bp.route('/')
def list_prestataires():
    """List all prestataires with search and filtering."""
    conn = get_db()
    cur = conn.cursor()
    
    # Get filter parameters
    search = request.args.get('search', '').strip()
    role_filter = request.args.get('role', '')
    
    # Base query
    query = '''
        SELECT p.id_prestataire, p.nom_entreprise, p.role_prest,
               COUNT(i.id_interv) as nb_interventions,
               COALESCE(SUM(i.cout_estime), 0) as total_cout
        FROM PRESTATAIRE p
        LEFT JOIN INTERVENTION i ON p.id_prestataire = i.id_prestataire
        WHERE 1=1
    '''
    
    params = []
    
    # Search
    if search:
        query += ''' AND (
            LOWER(p.nom_entreprise) LIKE LOWER(%s) OR 
            LOWER(p.role_prest) LIKE LOWER(%s)
        )'''
        search_param = f'%{search}%'
        params.extend([search_param, search_param])
    
    # Role filter
    if role_filter:
        query += ' AND p.role_prest = %s'
        params.append(role_filter)
    
    query += ' GROUP BY p.id_prestataire, p.nom_entreprise, p.role_prest'
    query += ' ORDER BY p.nom_entreprise'
    
    cur.execute(query, params)
    prestataires = cur.fetchall()
    
    # Get distinct roles for filter dropdown
    cur.execute('SELECT DISTINCT role_prest FROM PRESTATAIRE WHERE role_prest IS NOT NULL ORDER BY role_prest')
    roles = cur.fetchall()
    
    cur.close()
    
    return render_template('prestataires/list.html',
                          prestataires=prestataires,
                          roles=roles,
                          current_search=search,
                          current_role=role_filter)

@prestataires_bp.route('/add', methods=['GET', 'POST'])
def add_prestataire():
    """Add a new prestataire."""
    conn = get_db()
    cur = conn.cursor()
    
    if request.method == 'POST':
        nom_entreprise = request.form['nom_entreprise']
        role_prest = request.form.get('role_prest') or None
        
        try:
            # Let PostgreSQL auto-generate the ID (don't specify id_prestataire)
            cur.execute('''
                INSERT INTO PRESTATAIRE (nom_entreprise, role_prest)
                VALUES (%s, %s)
                RETURNING id_prestataire
            ''', (nom_entreprise, role_prest))
            new_id = cur.fetchone()[0]
            conn.commit()
            flash(f'Prestataire ajouté avec succès! (ID: {new_id})', 'success')
            return redirect(url_for('prestataires.list_prestataires'))
        except Exception as e:
            conn.rollback()
            flash(f'Erreur lors de l\'ajout: {str(e)}', 'danger')
        finally:
            cur.close()
    
    # GET: Load existing roles from database for suggestions
    cur.execute('SELECT DISTINCT role_prest FROM PRESTATAIRE WHERE role_prest IS NOT NULL ORDER BY role_prest')
    existing_roles = [r[0] for r in cur.fetchall()]
    cur.close()
    
    return render_template('prestataires/add.html', existing_roles=existing_roles)

@prestataires_bp.route('/view/<int:id>')
def view_prestataire(id):
    """View prestataire details with their interventions."""
    conn = get_db()
    cur = conn.cursor()
    
    # Get prestataire details
    cur.execute('''
        SELECT id_prestataire, nom_entreprise, role_prest
        FROM PRESTATAIRE
        WHERE id_prestataire = %s
    ''', (id,))
    prestataire = cur.fetchone()
    
    if not prestataire:
        flash('Prestataire non trouvé!', 'warning')
        return redirect(url_for('prestataires.list_prestataires'))
    
    # Get interventions by this prestataire
    cur.execute('''
        SELECT i.id_interv, i.date_debut, i.date_fin, i.type_travaux,
               i.cout_estime, i.est_validee, i.statut_travaux,
               b.code_batiment, b.nom_batiment
        FROM INTERVENTION i
        JOIN BATIMENT b ON i.code_batiment = b.code_batiment
        WHERE i.id_prestataire = %s
        ORDER BY i.date_debut DESC
    ''', (id,))
    interventions = cur.fetchall()
    
    # Get statistics
    cur.execute('''
        SELECT 
            COUNT(*) as total,
            COUNT(CASE WHEN est_validee = TRUE THEN 1 END) as validated,
            COUNT(CASE WHEN statut_travaux = 'En cours' THEN 1 END) as en_cours,
            COUNT(CASE WHEN statut_travaux = 'Terminé' THEN 1 END) as termines,
            COALESCE(SUM(cout_estime), 0) as total_cout
        FROM INTERVENTION
        WHERE id_prestataire = %s
    ''', (id,))
    stats = cur.fetchone()
    
    cur.close()
    
    return render_template('prestataires/view.html', 
                          prestataire=prestataire, 
                          interventions=interventions,
                          stats=stats)

@prestataires_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_prestataire(id):
    """Edit an existing prestataire."""
    conn = get_db()
    cur = conn.cursor()
    
    if request.method == 'POST':
        nom_entreprise = request.form['nom_entreprise']
        role_prest = request.form.get('role_prest') or None
        
        try:
            cur.execute('''
                UPDATE PRESTATAIRE 
                SET nom_entreprise = %s, role_prest = %s
                WHERE id_prestataire = %s
            ''', (nom_entreprise, role_prest, id))
            conn.commit()
            flash('Prestataire modifié avec succès!', 'success')
            return redirect(url_for('prestataires.view_prestataire', id=id))
        except Exception as e:
            conn.rollback()
            flash(f'Erreur lors de la modification: {str(e)}', 'danger')
        finally:
            cur.close()
    
    # GET: Load prestataire data
    cur.execute('''
        SELECT id_prestataire, nom_entreprise, role_prest
        FROM PRESTATAIRE
        WHERE id_prestataire = %s
    ''', (id,))
    prestataire = cur.fetchone()
    
    if not prestataire:
        flash('Prestataire non trouvé!', 'warning')
        return redirect(url_for('prestataires.list_prestataires'))
    
    # Load existing roles for suggestions
    cur.execute('SELECT DISTINCT role_prest FROM PRESTATAIRE WHERE role_prest IS NOT NULL ORDER BY role_prest')
    existing_roles = [r[0] for r in cur.fetchall()]
    cur.close()
    
    return render_template('prestataires/edit.html', prestataire=prestataire, existing_roles=existing_roles)

@prestataires_bp.route('/delete/<int:id>', methods=['POST'])
def delete_prestataire(id):
    """Delete a prestataire."""
    conn = get_db()
    cur = conn.cursor()
    
    try:
        # Check if prestataire has interventions
        cur.execute('SELECT COUNT(*) FROM INTERVENTION WHERE id_prestataire = %s', (id,))
        count = cur.fetchone()[0]
        
        if count > 0:
            flash(f'Impossible de supprimer: ce prestataire a {count} intervention(s) associée(s).', 'danger')
            return redirect(url_for('prestataires.view_prestataire', id=id))
        
        cur.execute('DELETE FROM PRESTATAIRE WHERE id_prestataire = %s', (id,))
        conn.commit()
        flash('Prestataire supprimé avec succès!', 'success')
    except Exception as e:
        conn.rollback()
        flash(f'Erreur: {str(e)}', 'danger')
    finally:
        cur.close()
    
    return redirect(url_for('prestataires.list_prestataires'))