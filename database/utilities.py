import numpy as np
import pandas as pd
import os
from . import Classes

# chemin du dossier de destination des nouveaux csv
SAVE_CSV_FILEPATH = "database/data/"

# Fonction créant un fichier csv de nom 'filename' important les données de la colonne 'csv_column' du csv du jeu de données et retourne le chemin du nouveau csv
def create_csv(csv_source, filename, columns, db_connect=None):
    # Creation d'un Dataframe
    original_csv_file=pd.read_csv(csv_source, sep=";")
    try:     
        if isinstance(columns, str):
            new_csv_file = original_csv_file[[columns]]
            # Creation d'une liste exhaustive sans redondance des valeurs de la colonne du Dataframe
            new_csv_file.drop_duplicates(subset=columns, keep='first', ignore_index=True ,inplace=True)
            # Creation d'un fichier csv contenant la listes de ces valeurs et un index numérique
            new_csv_file.to_csv(path_or_buf=SAVE_CSV_FILEPATH+filename+'.csv', sep=';', index=True)
            print("\nFile '%s.csv' created\n" %filename)
        else :
            #new_csv_file = frame_data(original_csv_file, filename, columns)
            new_csv_file = original_csv_file[columns]

            if filename == 'etablissement':
                print('Creating dataframe etablissement...')
                # correction des points-virgules des valeurs par des virgules
                new_csv_file['APP_Libelle_etablissement'] = new_csv_file['APP_Libelle_etablissement'].apply(lambda x: str(x).replace(';',','))
                new_csv_file['Adresse_2_UA'] = new_csv_file['Adresse_2_UA'].apply(lambda x: str(x).replace(';','.'))
                # suppression des doublons
                new_csv_file.drop_duplicates(subset='SIRET', keep='first', ignore_index=True ,inplace=True)
                # remplacement des valeurs vides par null
                #new_csv_file['Agrement'] = new_csv_file['Agrement'].fillna('null')
                print('Dataframe cible created!')
                new_csv_file.to_csv(path_or_buf=SAVE_CSV_FILEPATH+filename+'.csv', sep=';', index=True)
                print("\nFile '%s.csv' created\n" %filename)

            if filename == 'cible':
                print('Creating dataframe cible...')
                new_csv_file.drop_duplicates(subset=['SIRET','ods_type_activite'], keep='first', ignore_index=True ,inplace=True)
                file_temp = SAVE_CSV_FILEPATH+filename+'_temp.csv'
                new_csv_file.to_csv(path_or_buf=file_temp, sep=';', index=True)
                print("\nFile '%s_temp.csv' created\n" %filename)
                create_csv_cible(file_temp, db_connect)

            if filename == 'inspecte':
                print('Creating dataframe inspecte...')
                file_temp = SAVE_CSV_FILEPATH+filename+'_temp.csv'
                new_csv_file.to_csv(path_or_buf=file_temp, sep=';', index=True)
                print("\nFile '%s_temp.csv' created\n" %filename)
                create_csv_inspecte(file_temp, db_connect)
            
            if filename == 'concerne':
                print('Creating dataframe concerne...')
                new_csv_file.drop_duplicates(subset=['SIRET','APP_Libelle_activite_etablissement'], keep='first', ignore_index=True ,inplace=True)
                file_temp = SAVE_CSV_FILEPATH+filename+'_temp.csv'
                new_csv_file.to_csv(path_or_buf=file_temp, sep=';', index=True)
                print("\nFile '%s_temp.csv' created\n" %filename)
                create_csv_concerne(file_temp, db_connect)

    # gestion des erreurs et exceptions
    except (Exception, IOError) as error:
        print("IOERROR :", error,'\n')



def create_csv_cible(file_temp, db_connect):

    df_source = pd.read_csv(file_temp, sep=";", index_col=0)
    print(df_source.head(5))
    # récupération des données types activites en BDD
    etablissements = pd.DataFrame(Connection.query_all(db_connect,'select id_etablissement, siret from etablissement;'), columns=['id','siret'])
    etablissements.set_index('siret', inplace=True)
    print(etablissements.head(5))
    types = pd.DataFrame(Connection.query_all(db_connect,'select * from type_activite;'), columns=['id','type'])
    types.set_index('type', inplace=True)
    print(types.head(5))

    df_target = pd.DataFrame(data=None,columns=['id_etablissement','id_type_activite'])
    for index in range(0, len(df_source)):
        siret = df_source['SIRET'][index]
        activite = df_source['ods_type_activite'][index]
        df_new_row = pd.DataFrame({'id_etablissement': [etablissements.loc[siret,'id']],'id_type_activite': types.loc[activite,'id']})
        df_target = pd.concat([df_target,df_new_row], ignore_index=True)
    print(df_target.head())
    # Creation d'un fichier csv contenant la listes de ces valeurs et un index numérique
    df_target.to_csv(path_or_buf='database/data/cible.csv', sep=';', index=False)

    print("\nFile 'cible.csv' final created\n")


def create_csv_inspecte(file_temp, db_connect):

    df_source = pd.read_csv(file_temp, sep=";", index_col=0)

    # récupération des données types activites en BDD
    etablissements = pd.DataFrame(Connection.query_all(db_connect,'select id_etablissement, siret from etablissement;'), columns=['id','siret'])
    etablissements.set_index('siret', inplace=True)
    niveau_hygiene = pd.DataFrame(Connection.query_all(db_connect,'select * from niveau_hygiene;'), columns=['id', 'niveau'])
    niveau_hygiene.set_index('niveau', inplace=True)
    
    df_target = pd.DataFrame(data=None,columns=['id_etablissement','id_hygiene','numero_inspection','date_inspection'])
    for index in range(0, len(df_source)):
        siret = df_source['SIRET'][index]
        hygiene = df_source['Synthese_eval_sanit'][index]
        df_new_row = pd.DataFrame({'id_etablissement': [etablissements.loc[siret,'id']],'id_hygiene': [niveau_hygiene.loc[hygiene,'id']],'numero_inspection': [df_source['Numero_inspection'][index]],'date_inspection': [df_source['Date_inspection'][index]]})
        df_target = pd.concat([df_target,df_new_row], ignore_index=True)
    print(df_target.head())
    # Creation d'un fichier csv contenant la listes de ces valeurs et un index numérique
    df_target.to_csv(path_or_buf='database/data/inspecte.csv', sep=';', index=False)

    print("\nFile 'inspecte.csv' final created\n")


def create_csv_concerne(file_temp, db_connect):

    df_source = pd.read_csv(file_temp, sep=";", index_col=0)

    # récupération des données types activites en BDD
    etablissements = pd.DataFrame(Connection.query_all(db_connect,'select id_etablissement, siret from etablissement;'), columns=['id','siret'])
    etablissements.set_index('siret', inplace=True)
    domaine = pd.DataFrame(Connection.query_all(db_connect,'select * from domaine_activite;'), columns=['id', 'domaine'])
    domaine.set_index('domaine', inplace=True)
    
    df_target = pd.DataFrame(data=None,columns=['id_etablissement','id_activite'])
    for index in range(0, len(df_source)):
        siret = df_source['SIRET'][index]
        activite = df_source['APP_Libelle_activite_etablissement'][index]
        df_new_row = pd.DataFrame({'id_etablissement': [etablissements.loc[siret,'id']],'id_activite': [domaine.loc[activite,'id']]})
        df_target = pd.concat([df_target,df_new_row], ignore_index=True)
    print(df_target.head())
    # Creation d'un fichier csv contenant la listes de ces valeurs et un index numérique
    df_target.to_csv(path_or_buf='database/data/concerne.csv', sep=';', index=False)

    print("\nFile 'inspecte.csv' final created\n")

