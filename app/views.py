from flask import Blueprint, render_template, request
from flask_login import login_required, current_user

views = Blueprint('views', __name__)

@views.route('/')
@login_required
def profil():
    # Affiche les données personnels du current-user
    return render_template("views/user_profil.html")

@views.route('/etablissement')
def etablissement():
    return render_template("views/add_etablissement.html")

@views.route('/historique')
def historique():
    # Affiche l'historique des prédictions du current-user
    return render_template("views/user_historique.html")

@views.route('/etablissement',methods=['POST','GET'])
def estimation():
    # Affiche un formulaire de demande de prédiction
    if request.method == 'POST':
                libelle = request.form.get('libelle')
                siret = request.form.get('siret')
                libelle_activite = request.form.get('libelle_activite')
                return render_template("views/estimation.html",
                libelle=libelle,siret=siret,libelle_activite=libelle_activite,niveau_hygiene="très satisfaisant")
    return render_template("views/add_etablissement.html")