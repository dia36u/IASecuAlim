from Classes import Connection
from utilities import create_csv
import os

 # chemins relatifs
PATH_TO_SCRIPTS = "database/scripts/"
PATH_TO_CSV = "database/data/"

# dictionnaire "table : colonnes csv"
database_tables = {
    'niveau_hygiene':'Synthese_eval_sanit',
    'etablissement': ['APP_Libelle_etablissement','SIRET','Adresse_2_UA','Code_postal','Libelle_commune','geores','Agrement'],
    'concerne':['SIRET', 'APP_Libelle_activite_etablissement'],
    'domaine_activite':'APP_Libelle_activite_etablissement',
    'cible':['SIRET', 'ods_type_activite'],
    'type_activite':'ods_type_activite',
    'inspecte':['SIRET', 'Numero_inspection', 'Date_inspection','Synthese_eval_sanit'],
}

def create_database():
    
    # Connexion à la base de donnée
    db = Connection.connection_to_database()

    # Execution du script sql de création des tables si elles n'existent pas
    if Connection.table_exists(db) != True :
        for line in open(PATH_TO_SCRIPTS+'create_tables.sql'):
            db.cursor().execute(line)
            db.cursor().close()
    
    # Création des fichiers CSV pour chaque table si le fichier n'existe pas
    for key, value in database_tables.items() :
        if value and not os.path.isfile(PATH_TO_CSV+key+'.csv'):
            create_csv(PATH_TO_CSV+'export_alimconfiance.csv', key, value)
    
    # Insertion des données dans les tables si la table est vide
    for key in database_tables.keys():
        file = PATH_TO_CSV+key+'.csv'
        if os.path.isfile(file) and not Connection.data_exist(db, key):
            Connection.copy_from(db, file, key)

create_database()
