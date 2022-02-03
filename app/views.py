from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
import random
from .models import Estimation
from . import db
import pandas as pd
from modele.RandomForest import predict
from database.Classes import Connection

views = Blueprint('views', __name__)

@views.route('/profil')
@login_required
def profil():
    # Affiche les données personnels du current-user
    return render_template("views/user_profil.html", user=current_user)

# @views.route('/etablissement')
# @login_required
# def etablissement():
#     return render_template("views/add_etablissement.html", user=current_user)

@views.route('/historique')
@login_required
def historique():
    # Affiche l'historique des prédictions du current-user
    return render_template("views/user_historique.html", user=current_user)

@views.route('/etablissement',methods=['POST','GET'])
@login_required
def estimation():
    # Affiche un formulaire de demande de prédiction
    requete_id='SELECT * FROM domaine_activite'
    db = Connection.connection_to_database()
    activites = Connection.query_all(db, requete_id)
    requete_id='SELECT * FROM type_activite'
    types=Connection.query_all(db, requete_id)

    if request.method == 'POST':
        libelle = request.form.get('libelle')
        siret = request.form.get('siret')
        libelle_activite = request.form.get('libelle_activite')
        code_postal = request.form.get('code_postal')
        type_activite = request.form.get('type_activite')
        # niveau_hygiene= ['Très satisfaisant','Satisfaisant','A améliorer','A corriger de manière urgente']
        # niveau_hygiene=(random.choice(niveau_hygiene))
        # new_estimation = Estimation(result=(libelle+' ('+siret+') '+': '+niveau_hygiene), user_id=current_user.id)
        new_estimation = pd.DataFrame({"id_activite": [libelle_activite], "id_type_activite": [type_activite], "code_postal":[code_postal]})
        # db.session.add(new_estimation)
        # db.session.commit()
        # get prediction for new input
        new_output = predict.cls.predict(new_estimation)
        niveau_hygiene = Connection.query_all(db, 'SELECT * FROM niveau_hygiene')
        for niveau in niveau_hygiene:
            if new_output==niveau[0]:
                niveau_textuel=niveau[1]
        # summarize input and output
        # print(new_input, new_output)
        return render_template("views/estimation.html",libelle=libelle,siret=siret,libelle_activite=libelle_activite,niveau_hygiene=niveau_textuel, user=current_user)
    return render_template("views/add_etablissement.html", user=current_user, activites=activites, types=types)