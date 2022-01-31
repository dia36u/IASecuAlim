from Classes import Connection
from utilities import create_csv
import os

 # chemins relatifs vers les fichiers de scripts, vers les fichiers de données
PATH_TO_SCRIPTS = "database/scripts/"
PATH_TO_CSV = "database/data/"

# dictionnaire "{table : colonnes csv}"
database_tables = {
    'niveau_hygiene':'Synthese_eval_sanit',
    'etablissement': ['APP_Libelle_etablissement','SIRET','Adresse_2_UA','Code_postal','Libelle_commune','geores','Agrement'],
    'domaine_activite':'APP_Libelle_activite_etablissement',
    'type_activite':'ods_type_activite',
    'cible':['SIRET', 'ods_type_activite'],
    'inspecte':['SIRET', 'Numero_inspection', 'Date_inspection','Synthese_eval_sanit'],
    'concerne':['SIRET', 'APP_Libelle_activite_etablissement'],
}

def create_database():
    """ Cette fonction execute les étapes de création de la base de données POSTGRES :
            1. Ouverture d'une connection au serveur en renseignant les paramètres du fichier "config.py":
                - la database par défaut est 'AlimConfiance';
            2. Exécution du script de création des tables 'create_tables.sql' après vérification de leur absence de la database;
            3. Création de fichiers au format CSV en sélectionnant les colonnes du CSV 'export_alimconfiance.csv', aussi:
                - vérification si le fichier csv n'est pas déjà crée dans le dossier data/
                - un fichier csv = une table en base de données (listée dans la variable 'database_tables'),
                - les tables de liaisons 'cible', 'concerne' et 'inspecte' ont été traitées avec la fonction 'clean_dataframe' qui remplace les valeurs par des id,
            4. Exécution des requêtes d'insertion des données dans les tables
    """
    # 1. Connexion à la base de donnée
    db = Connection.connection_to_database()

    # 2. Execution du script sql de création des tables si elles n'existent pas
    if Connection.table_exists(db) != True :
        for line in open(PATH_TO_SCRIPTS+'create_tables.sql'):
            db.cursor().execute(line)
            db.cursor().close()
    
    # 3. Création des fichiers CSV pour chaque table si le fichier n'existe pas
    for key, value in database_tables.items() :
        if value and not os.path.isfile(PATH_TO_CSV+key+'.csv'):
            create_csv(PATH_TO_CSV+'export_alimconfiance.csv', key, value, db)
    
    # 4. Insertion des données dans les tables si la table est vide
    for key in database_tables.keys():
        file = PATH_TO_CSV+key+'.csv'
        print("check tables content\n")
        if os.path.isfile(file) and not Connection.data_exist(db, key):
            Connection.copy_from(db, file, key)

create_database()
