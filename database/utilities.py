import numpy as np
import pandas as pd
from Classes import Connection

# chemin du dossier de destination des nouveaux csv
SAVE_CSV_FILEPATH = "database/data/"

def frame_data(df_source, filename, columns):
   
    print(df_source)
    new_csv_file = df_source[columns]
    print('colonnes : %s' %columns)

    if filename == 'etablissement':
        print('etablissement')
        # correction des points-virgules des valeurs par des virgules
        new_csv_file['APP_Libelle_etablissement'] = new_csv_file['APP_Libelle_etablissement'].apply(lambda x: str(x).replace(';',','))
        new_csv_file['Adresse_2_UA'] = new_csv_file['Adresse_2_UA'].apply(lambda x: str(x).replace(';','.'))
        # remplacement des valeurs vides par null
        #new_csv_file['Agrement'] = new_csv_file['Agrement'].fillna('null')
    # TODO
    if filename == 'cible':
        print('cible')
        conn = Connection.connection_to_database()
        types = pd.DataFrame(Connection.query_all(conn,'select * from %s;' %filename))
        print(types)
        etablissements = pd.DataFrame(Connection.query_all(conn,'select id_etablissement, siret from etablissement;'))
        print(etablissements)
        for key, value in types.items():
            new_csv_file.replace(to_replace=[], value=[])
    return new_csv_file

# Fonction créant un fichier csv de nom 'filename' important les données de la colonne 'csv_column' du csv du jeu de données et retourne le chemin du nouveau csv
def create_csv(csv_source, filename, columns):
    # Creation d'un Dataframe
    original_csv_file=pd.read_csv(csv_source, sep=";")
    try:     
        if isinstance(columns, str):
            print(1)
            new_csv_file = original_csv_file[[columns]]
            # Creation d'une liste exhaustive sans redondance des valeurs de la colonne du Dataframe
            new_csv_file.drop_duplicates(subset=columns, keep='first', ignore_index=True ,inplace=True)
        else :
            print(2)
            new_csv_file = frame_data(original_csv_file, filename, columns)

        # Creation d'un fichier csv contenant la listes de ces valeurs et un index numérique
        new_csv_file.to_csv(path_or_buf=SAVE_CSV_FILEPATH+filename+'.csv', sep=';', index=True)
        print("\n %s CSV created\n" %filename)

    # gestion des erreurs et exceptions
    except (Exception, IOError) as error:
        print("IOERROR :")
        print(error,'\n')







