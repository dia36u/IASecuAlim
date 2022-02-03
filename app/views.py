from multiprocessing.connection import Connection
from flask import Blueprint, render_template, request
<<<<<<< HEAD
from database import Classes
=======
from flask_login import login_required, current_user
import random
from .models import Estimation
from . import db
>>>>>>> 23b15cc3a4bf46a88ab4ec38cff7494c0bef1e90

views = Blueprint('views', __name__)

@views.route('/profil')
@login_required
def profil():
    # Affiche les données personnels du current-user
    return render_template("views/user_profil.html", user=current_user)

@views.route('/etablissement')
@login_required
def etablissement():
    return render_template("views/add_etablissement.html", user=current_user)

@views.route('/historique')
@login_required
def historique():
    # Affiche l'historique des prédictions du current-user
    return render_template("views/user_historique.html", user=current_user)

@views.route('/etablissement',methods=['POST','GET'])
@login_required
def estimation():
    activites_domaines = Classes.Connection.query_table('domaine_activite')
    print(activites_domaines)
    # Affiche un formulaire de demande de prédiction
    if request.method == 'POST':
                libelle = request.form.get('libelle')
                siret = request.form.get('siret')
                libelle_activite = request.form.get('libelle_activite')
                niveau_hygiene= ['Très satisfaisant','Satisfaisant','A améliorer','A corriger de manière urgente']
                niveau_hygiene=(random.choice(niveau_hygiene))
                new_estimation = Estimation(result=(libelle+' ('+siret+') '+': '+niveau_hygiene), user_id=current_user.id)
                db.session.add(new_estimation)
                db.session.commit()
                return render_template("views/estimation.html",
<<<<<<< HEAD
                libelle=libelle,siret=siret,libelle_activite=libelle_activite,niveau_hygiene="très satisfaisant")
    return render_template("views/add_etablissement.html", domaines=activites_domaines)
=======
                libelle=libelle,siret=siret,libelle_activite=libelle_activite,niveau_hygiene=niveau_hygiene, user=current_user)
    return render_template("views/add_etablissement.html", user=current_user)
>>>>>>> 23b15cc3a4bf46a88ab4ec38cff7494c0bef1e90
