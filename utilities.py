import pandas as pd
from config import CSV_DIR_FILEPATH, CSV_SOURCE_FILEPATH
from app import copy_from_file, copy_from_file_multicolumns
import os

# Fonction créant un fichier csv de nom 'filename' important les données de la colonne 'csv_column' du csv du jeu de données et retourne le chemin du nouveau csv
def create_csv(filename, *args):
    # Creation d'un Dataframe
    original_csv_file=pd.read_csv(CSV_SOURCE_FILEPATH, sep=";")
    # Selection d'une colonne du Dataframe
    new_csv_file=original_csv_file[[*args]]
    try:
        if args.count == 1:
            # Creation d'une liste exhaustive sans redondance des valeurs de la colonne du Dataframe
            new_csv_file.drop_duplicates(subset=args, keep='first', ignore_index=True ,inplace=True)
        # Creation d'un fichier csv contenant la listes de ces valeurs et un index numérique
        new_csv_file.to_csv(path_or_buf=CSV_DIR_FILEPATH+filename+'.csv', sep=';', index=True)
        print("\nCSV creation successful\n")
    # gestion des erreurs et exceptions
    except (Exception, IOError) as error:
        print("Error: %s" % error)
    return CSV_DIR_FILEPATH+filename+'.csv'


# Fonction pour créer un CSV pour la table etablissement, avec corrections
def create_csv_etablissement(filename):
    # import du csv avec delimiteur ';'
    original_csv_file = pd.read_csv('data/csv/export_alimconfiance.csv', sep=";")
    # creation d'une variable avec les champs de la table établissement
    etabl_libs = original_csv_file[['APP_Libelle_etablissement','SIRET','Adresse_2_UA','Code_postal','Libelle_commune','geores','Agrement']]
    # correction des points-virgules des valeurs par des virgules
    etabl_libs['APP_Libelle_etablissement'] = etabl_libs['APP_Libelle_etablissement'].apply(lambda x: x.replace(';',','))
    etabl_libs['Adresse_2_UA'] = etabl_libs['Adresse_2_UA'].apply(lambda x: str(x).replace(';','.'))
    # remplacement des valeurs vides par null
    etabl_libs['Agrement'] = etabl_libs['Agrement'].fillna('null')
    try:
        # Creation d'un fichier csv contenant la listes de ces valeurs et un index numérique
        etabl_libs.to_csv(path_or_buf=CSV_DIR_FILEPATH+filename+'.csv', sep=';', index=True)
        print("\nCSV creation successful\n")
    # gestion des erreurs et exceptions
    except (Exception, IOError) as error:
        print("Error: %s" % error)
    return CSV_DIR_FILEPATH+filename+'.csv'

# Fonction pour creer un CSV puis insérer ses données dans une table
def copy_csv_to_database(table_name, csv_column=None):
    if table_name == 'etablissement':
        file = create_csv_etablissement
        copy_from_file_multicolumns(file)
    else:
        file = create_csv(table_name, csv_column)
        copy_from_file(table_name, file)