from multiprocessing.connection import Connection
from flask import Blueprint, render_template, request
from database import Classes

views = Blueprint('views', __name__)

@views.route('/profil')
def profil():
    # Affiche les données personnels du current-user
    return render_template("views/user_profil.html")

@views.route('/historique')
def historique():
    # Affiche l'historique des prédictions du current-user
    return render_template("views/user_historique.html")

@views.route('/etablissement',methods=['POST','GET'])
def estimation():
    activites_domaines = Classes.Connection.query_table('domaine_activite')
    print(activites_domaines)
    # Affiche un formulaire de demande de prédiction
    if request.method == 'POST':
                libelle = request.form.get('libelle')
                siret = request.form.get('siret')
                libelle_activite = request.form.get('libelle_activite')
                return render_template("views/estimation.html",
                libelle=libelle,siret=siret,libelle_activite=libelle_activite,niveau_hygiene="très satisfaisant")
    return render_template("views/add_etablissement.html", domaines=activites_domaines)