# ----- Import des librairies -----

from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from werkzeug.utils import secure_filename
import os 
import base64
# Import des fonctions codées dans d'autres fichiers
from app.db import get_db_connection
from app.utils import calculer_age, allowed_file
from app.models.model import predict_image

# Création du Blueprint patient
# Il permet d'organiser les routes liées à la gestion des patients
patient_bp = Blueprint('patient', __name__)

# ----- Définition des routes -----

# Route pour afficher la page avec tous les patients déjà chargés
@patient_bp.route('/patients')
def get_patients():    
    try:
        # Connexion à la BDD et récupérer les informations de tous les patients
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM Patient")
        patients = cursor.fetchall()
        conn.close()
        # Rediriger vers la page avec tous les patients chargés
        return render_template('recherche_patients.html', patients=patients)
    except Exception as e:
        print("Erreur:", e)
        return render_template('recherche_patients.html', error="Erreur de chargement des patients")

# Route pour filtrer les patients
@patient_bp.route('/filter_patients')
def filter_patients():
    try:
        # Connexion à la BDD
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        # Récupération des filtres
        nom = request.args.get('nom', '')
        prenom = request.args.get('prenom', '')
        age = request.args.get('age', '')

        # Construction de la requête SQL en fonction des filtres
        query = "SELECT * FROM Patient WHERE 1=1"
        params = []
        if nom:
            query += " AND LOWER(nom) LIKE %s"
            params.append(f"{nom.lower()}%")
        if prenom:
            query += " AND LOWER(prenom) LIKE %s"
            params.append(f"{prenom.lower()}%")
        if age:
            query += " AND age = %s"
            params.append(age)

        cursor.execute(query, tuple(params))
        patients = cursor.fetchall()
        conn.close()
        # Retourner les résultats sous forme JSON
        return jsonify(patients)
    except Exception as e:
        print("Erreur:", e)
        return jsonify({"error": "Erreur de filtrage"})

# Route pour ajouter un nouveau patient
@patient_bp.route('/nouveau_patient', methods=['GET', 'POST'])
def nouveau_patient():
    if request.method == 'POST':
        # Connexion à la BDD
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Récupération des données du formulaire
        nom = request.form['nom']
        prenom = request.form['prenom']
        date_naissance = request.form['date_naissance']
        sexe = request.form['sexe']
        mode_vie = request.form['mode_de_vie'] if request.form['mode_de_vie'] else None
        date_diagnostic = request.form['date_diagnostic'] if request.form['date_diagnostic'] else None
        forme_sep = request.form['forme_sep'] if request.form['forme_sep'] else None
        score_edss = request.form['score_edss'] if request.form['score_edss'] else None
        symptomes = request.form['symptomes'] if request.form['symptomes'] else None

        # Calcul de l'âge à partir de la date de naissance
        age = calculer_age(date_naissance)

        if sexe == "homme":
            sexe ='H'
        else:
            sexe = 'F'

        # Insertion du patient dans la table Patient
        cursor.execute("""
            INSERT INTO Patient (nom, prenom, age, sexe, mode_vie, date_diagnostic, forme_sep, score_edss, symptomes, date_de_naissance)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (nom, prenom, age, sexe, mode_vie, date_diagnostic, forme_sep, score_edss, symptomes, date_naissance))

        # Récupérer l'ID du patient qui vient d'être inséré
        patient_id = cursor.lastrowid

        # Insertion des traitements antérieurs dans la BDD si le patient en a 
        traitements = request.form.getlist('nom_traitement[]')
        frequences = request.form.getlist('frequence_traitement[]')
        infos = request.form.getlist('informations_traitement[]')
        
        for nom_traitement, frequence, info in zip(traitements, frequences, infos):
            if nom_traitement or frequence or info:
                cursor.execute("INSERT INTO Traitement (nom, frequence_dosage, informations_complementaire, actuel) VALUES (%s, %s, %s, 0)",
                            (nom_traitement, frequence, info))
                traitement_id = cursor.lastrowid
                cursor.execute("INSERT INTO Patient_traitement (patient_id, traitement_id, type_traitement) VALUES (%s, %s, 'anterieur')", 
                            (patient_id, traitement_id))
        
        # Insertion des traitements actuels dans la BDD si le patient en a 
        traitements_actuels = request.form.getlist('nom_traitement_actuel[]')
        frequences_actuels = request.form.getlist('frequence_traitement_actuel[]')
        infos_actuels = request.form.getlist('informations_traitement_actuel[]')
        
        for nom_traitement, frequence, info in zip(traitements_actuels, frequences_actuels, infos_actuels):
            if nom_traitement or frequence or info:
                cursor.execute("INSERT INTO Traitement (nom, frequence_dosage, informations_complementaire, actuel) VALUES (%s, %s, %s, 1)",
                            (nom_traitement, frequence, info))
                traitement_id = cursor.lastrowid
                cursor.execute("INSERT INTO Patient_traitement (patient_id, traitement_id, type_traitement) VALUES (%s, %s, 'actuel')", 
                            (patient_id, traitement_id))

        # Insertion des examens médicaux dans la BDD si le patient en a 
        type_analyses = request.form.getlist('type_examen[]')
        date_analyses = request.form.getlist('date_examen[]')
        resultat_analyses = request.form.getlist('resultat_examen[]')
        
        for index, (type_analyse, date_analyse, resultat) in enumerate(zip(type_analyses, date_analyses, resultat_analyses)):
            if type_analyse or date_analyse or resultat:
                # Insérer l'examen dans la table Analyse
                cursor.execute(
                    "INSERT INTO Analyse (id_patient, type_analyse, date_analyse, resultats) VALUES (%s, %s, %s, %s)",
                    (patient_id, type_analyse, date_analyse, resultat)
                )
                analyse_id = cursor.lastrowid

                # Récupérer les fichiers associés à CET examen
                files_key = f'document_scanne_{index}[]'
                files = request.files.getlist(files_key)

                # Insérer chaque image dans la table Images
                for file in files:
                    if file and file.filename != '':
                        image_data = file.read()
                        cursor.execute("INSERT INTO Images (id_analyse, document_scanne) VALUES (%s, %s)", (analyse_id, image_data))

        # Insertion des consultations dans la BDD si le patient en a        
        date_consultations = request.form.getlist('derniere_consultation[]')
        plan_soins = request.form.getlist('plan_soins[]')

        if any([date_consultations, plan_soins]):
            for date, plan in zip(date_consultations, plan_soins):
                if date or plan:
                    cursor.execute("INSERT INTO Consultation (patient_id, date_consultation, plan_soins) VALUES (%s, %s, %s)",
                                (patient_id, date, plan))

        conn.commit()
        conn.close()
        # Affichage d'un message succès et redirection vers le dashboard patient
        flash("Le patient a été ajouté avec succès !", "success")
        return redirect(url_for('patient.get_patients'))
    return render_template('nouveau_patient.html')

# Route pour supprimer un patient
@patient_bp.route('/delete_patient/<int:patient_id>', methods=['GET'])
def delete_patient(patient_id):
    # Connexion à la BDD
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        # Supprimer les associations dans la table Patient_traitement
        cursor.execute("DELETE FROM Patient_traitement WHERE patient_id = %s", (patient_id,))
        # Supprimer les traitements du patient
        cursor.execute("DELETE FROM Traitement WHERE id IN (SELECT traitement_id FROM Patient_traitement WHERE patient_id = %s)", (patient_id,))
        # Supprimer les analyses médicales du patient
        cursor.execute("DELETE FROM Analyse WHERE id_patient = %s", (patient_id,))
        # Supprimer les consultations du patient
        cursor.execute("DELETE FROM Consultation WHERE patient_id = %s", (patient_id,))
        # Supprimer le patient de la table Patient
        cursor.execute("DELETE FROM Patient WHERE id_patient = %s", (patient_id,))
        conn.commit()
        # Message de succès 
        flash("Le patient et ses informations ont été supprimés avec succès.", "success")
    # Gestion des erreurs avec message d'erreur 
    except Exception as e:
        conn.rollback()
        flash(f"Erreur lors de la suppression du patient : {str(e)}", "error")
    finally:
        conn.close()
    # Redirection
    return redirect(url_for('patient.get_patients'))  # Recharger la page avec la liste des patients

# Route pour voir la fiche d'un patient
@patient_bp.route('/view_patient/<int:patient_id>')
def view_patient(patient_id):
    # Connexion à la BDD
    conn = get_db_connection()
    cursor = conn.cursor()
    # Récupérer les informations du patient
    cursor.execute("SELECT * FROM Patient WHERE id_patient = %s", (patient_id,))
    patient = cursor.fetchone()

    # Si le patient n'existe pas 
    if not patient:
        # Redirection vers la liste des patients avec un message d'erreur
        flash('Patient non trouvé.', 'danger')
        return redirect(url_for('patient.get_patients'))

    # Récupérer les traitements antérieurs du patient
    cursor.execute("""
        SELECT *
        FROM Traitement T
        JOIN Patient_traitement PT ON T.id = PT.traitement_id
        WHERE PT.patient_id = %s AND PT.type_traitement = 'anterieur'
    """, (patient_id,))
    traitements_anterieurs = cursor.fetchall()

    # Récupérer les traitements actuels du patient
    cursor.execute("""
        SELECT *
        FROM Traitement T
        JOIN Patient_traitement PT ON T.id = PT.traitement_id
        WHERE PT.patient_id = %s AND PT.type_traitement = 'actuel'
    """, (patient_id,))

    traitements_actuels = cursor.fetchall()

    # Récupérer les analyses du patient
    cursor.execute("""
        SELECT a.id_analyse, a.type_analyse, a.date_analyse, a.resultats, i.document_scanne
        FROM Analyse a
        LEFT JOIN Images i ON a.id_analyse = i.id_analyse
        WHERE a.id_patient = %s
    """, (patient_id,))
    analyses = cursor.fetchall()
    
    # Convertir les images en Base64 et les ajouter à la liste d'analyses
    for i, analyse in enumerate(analyses):
        if analyse[4]:  
            analyses[i] = analyse[:4] + (base64.b64encode(analyse[4]).decode('utf-8'),)

    # Récupérer les consultations du patient
    cursor.execute("""
        SELECT *
        FROM Consultation C
        WHERE C.patient_id = %s
    """, (patient_id,))

    consultations = cursor.fetchall()
    conn.close()
    # Passer les informations du patient et ses détails au template
    return render_template('consulter_fiche_patient.html', patient=patient,
                           traitements_anterieurs=traitements_anterieurs,
                           traitements_actuels=traitements_actuels,
                           analyses=analyses, consultations=consultations)

# Route pour modifier la fiche d'un patient
@patient_bp.route('/edit_patient/<int:patient_id>', methods=['GET', 'POST'])
def edit_patient(patient_id):
    # Connexion à la BDD
    conn = get_db_connection()
    cursor = conn.cursor()
    # Récupérer les informations du patient
    cursor.execute("SELECT * FROM Patient WHERE id_patient = %s", (patient_id,))
    patient = cursor.fetchone()
    # Si le patient n'existe pas
    if not patient:
        # Redirection vers la liste des patients avec un message d'erreur
        flash('Patient non trouvé.', 'danger')
        return redirect(url_for('patient.get_patients'))

    # Récupérer les traitements antérieurs du patient
    cursor.execute("""
        SELECT *
        FROM Traitement T
        JOIN Patient_traitement PT ON T.id = PT.traitement_id
        WHERE PT.patient_id = %s AND PT.type_traitement = 'anterieur'
    """, (patient_id,))
    traitements_anterieurs = cursor.fetchall()

    # Récupérer les traitements actuels du patient
    cursor.execute("""
        SELECT *
        FROM Traitement T
        JOIN Patient_traitement PT ON T.id = PT.traitement_id
        WHERE PT.patient_id = %s AND PT.type_traitement = 'actuel'
    """, (patient_id,))
    traitements_actuels = cursor.fetchall()

    # Récupérer les analyses du patient
    cursor.execute("""
        SELECT *
        FROM Analyse A
        WHERE A.id_patient = %s
    """, (patient_id,))
    analyses = cursor.fetchall()

    # Récupérer les consultations du patient
    cursor.execute("""
        SELECT *
        FROM Consultation C
        WHERE C.patient_id = %s
    """, (patient_id,))
    consultations = cursor.fetchall()
    conn.close()
    # Passer les informations du patient et ses détails au template
    return render_template('modifier_patient.html', patient=patient,
                           traitements_anterieurs=traitements_anterieurs,
                           traitements_actuels=traitements_actuels,
                           analyses=analyses, consultations=consultations)

# Route pour enregistrer les modifications de la fiche d'un patient
@patient_bp.route('/modifier_patient/<int:id>', methods=['GET', 'POST'])
def modifier_patient(id):
    # Connexion à la BDD
    conn = get_db_connection()
    cursor = conn.cursor()
    
    if request.method == 'POST':
        # Récupération des données du formulaire
        nom = request.form['nom']
        prenom = request.form['prenom']
        date_naissance = request.form['date_naissance']
        sexe = request.form['sexe']
        mode_vie = request.form['mode_de_vie'] if request.form['mode_de_vie'] else None
        date_diagnostic = request.form['date_diagnostic'] if request.form['date_diagnostic'] else None
        forme_sep = request.form['forme_sep'] if request.form['forme_sep'] else None
        score_edss = request.form['score_edss'] if request.form['score_edss'] else None
        symptomes = request.form['symptomes'] if request.form['symptomes'] else None

        # Calcul de l'âge à partir de la date de naissance
        age = calculer_age(date_naissance)

        if sexe == "homme":
            sexe ='H'
        else:
            sexe = 'F'

        # Mise à jour des informations générales du patient
        cursor.execute("""
            UPDATE Patient 
            SET nom = %s, prenom = %s, age = %s, sexe = %s, mode_vie = %s, date_diagnostic = %s, forme_sep = %s, score_edss = %s, symptomes = %s, date_de_naissance = %s
            WHERE id_patient = %s
        """, (nom, prenom, age, sexe, mode_vie, date_diagnostic, forme_sep, score_edss, symptomes, date_naissance, id))

        # Traitements antérieurs
        traitements = request.form.getlist('nom_traitement[]')
        frequences = request.form.getlist('frequence_traitement[]')
        infos = request.form.getlist('informations_traitement[]')
        
        # Suppression des traitements antérieurs existants
        cursor.execute("DELETE FROM Patient_traitement WHERE patient_id = %s AND type_traitement = 'anterieur'", (id,))
        
        for nom_traitement, frequence, info in zip(traitements, frequences, infos):
            if nom_traitement or frequence or info:
                cursor.execute("INSERT INTO Traitement (nom, frequence_dosage, informations_complementaire, actuel) VALUES (%s, %s, %s, 0)",
                            (nom_traitement, frequence, info))
                traitement_id = cursor.lastrowid
                cursor.execute("INSERT INTO Patient_traitement (patient_id, traitement_id, type_traitement) VALUES (%s, %s, 'anterieur')", 
                            (id, traitement_id))

        # Traitements actuels
        traitements_actuels = request.form.getlist('nom_traitement_actuel[]')
        frequences_actuels = request.form.getlist('frequence_traitement_actuel[]')
        infos_actuels = request.form.getlist('informations_traitement_actuel[]')
        
        # Suppression des traitements actuels existants
        cursor.execute("DELETE FROM Patient_traitement WHERE patient_id = %s AND type_traitement = 'actuel'", (id,))
        
        for nom_traitement, frequence, info in zip(traitements_actuels, frequences_actuels, infos_actuels):
            if nom_traitement or frequence or info:
                cursor.execute("INSERT INTO Traitement (nom, frequence_dosage, informations_complementaire, actuel) VALUES (%s, %s, %s, 1)",
                            (nom_traitement, frequence, info))
                traitement_id = cursor.lastrowid
                cursor.execute("INSERT INTO Patient_traitement (patient_id, traitement_id, type_traitement) VALUES (%s, %s, 'actuel')", 
                            (id, traitement_id))

        # Ajout des examens médicaux
        type_analyses = request.form.getlist('type_examen[]')
        date_analyses = request.form.getlist('date_examen[]')
        resultat_analyses = request.form.getlist('resultat_examen[]')

        # Suppression des anciens examens
        cursor.execute("DELETE FROM Analyse WHERE id_patient = %s", (id,))
        
        for index, (type_analyse, date_analyse, resultat) in enumerate(zip(type_analyses, date_analyses, resultat_analyses)):
            if type_analyse or date_analyse or resultat:
                # Insérer l'examen dans la table Analyse
                cursor.execute(
                    "INSERT INTO Analyse (id_patient, type_analyse, date_analyse, resultats) VALUES (%s, %s, %s, %s)",
                    (id, type_analyse, date_analyse, resultat)
                )

                analyse_id = cursor.lastrowid

                # Récupérer les fichiers associés à cet examen
                files_key = f'document_scanne_{index}[]'
                files = request.files.getlist(files_key)

                # Insérer chaque image dans la table Images
                for file in files:
                    if file and file.filename != '':
                        image_data = file.read()
                        cursor.execute("INSERT INTO Images (id_analyse, document_scanne) VALUES (%s, %s)", (analyse_id, image_data))

        # Ajout des consultations
        date_consultations = request.form.getlist('derniere_consultation[]')
        plan_soins = request.form.getlist('plan_soins[]')

        # Suppression des anciennes consultations
        cursor.execute("DELETE FROM Consultation WHERE patient_id = %s", (id,))

        for date, plan in zip(date_consultations, plan_soins):
            if date or plan:
                cursor.execute("INSERT INTO Consultation (patient_id, date_consultation, plan_soins) VALUES (%s, %s, %s)",
                                (id, date, plan))

        conn.commit()
        conn.close()
        # Message de succès et redirection
        flash("Les informations du patient ont été mises à jour avec succès !", "success")
        return redirect(url_for('patient.get_patients'))

    # Récupérer les informations actuelles, les traitements, examens et consultations du patient
    cursor.execute("SELECT * FROM Patient WHERE id = %s", (id,))
    patient = cursor.fetchone()
    cursor.execute("SELECT * FROM Traitement JOIN Patient_traitement ON Traitement.id = Patient_traitement.traitement_id WHERE Patient_traitement.patient_id = %s", (id,))
    traitements = cursor.fetchall()
    cursor.execute("SELECT * FROM Analyse WHERE id_patient = %s", (id,))
    examens = cursor.fetchall()
    cursor.execute("SELECT * FROM Consultation WHERE patient_id = %s", (id,))
    consultations = cursor.fetchall()
    return render_template('modifier_patient.html', patient=patient, traitements=traitements, examens=examens, consultations=consultations)

# Route pour rediriger vers la page d'outil d'aide à la prise de décision
@patient_bp.route('/aidePriseDecision')
def consulter_outil():
    # Redirection
    return render_template('outil_aide_prise_decision.html')

# Route pour prédire l'état d'un patient
# SEP ou NON SEP
@patient_bp.route('/predict', methods=['POST'])
def prediction():
    if request.method == 'POST':
        # Récupérer l'image
        file = request.files['file']
        # Vérifier le format de l'image
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join('./uploads', filename)
            if not os.path.exists('./uploads'):
                os.makedirs('./uploads')
            # Sauvegarder l'image
            file.save(file_path)
            # Prédiction du label
            prediction = predict_image(file_path)
            return render_template('outil_aide_prise_decision.html', prediction=prediction)
        # Si le format n'est pas bon, message d'erreur 
        else:
            flash("Fichier refusé ! Mauvais format. Seuls les formats .jpg, .jpeg ou .png sont autorisés", "danger")
    return render_template('outil_aide_prise_decision.html')