from flask import Blueprint, render_template

views = Blueprint('views', __name__)

@views.route('/etablissement')
def etablissement():
    # Affiche un formulaire de demande de prédiction
    return render_template("views/add_etablissement.html")

@views.route('/profil')
def profil():
    # Affiche les données personnels du current-user
    return render_template("views/user_profil.html")

@views.route('/historique')
def historique():
    # Affiche l'historique des prédictions du current-user
    return render_template("views/user_historique.html")