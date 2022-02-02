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

        if isinstance(columns, str) and filename != 'domaine_activite':
            new_csv_file = original_csv_file[[columns]]
            # Creation d'une liste exhaustive sans redondance des valeurs de la colonne du Dataframe
            new_csv_file.drop_duplicates(subset=columns, keep='first', ignore_index=True ,inplace=True)
            # Creation d'un fichier csv contenant la listes de ces valeurs et un index numérique
            new_csv_file.to_csv(path_or_buf=SAVE_CSV_FILEPATH+filename+'.csv', sep=';', index=True)
            print("\nFile '%s.csv' created\n" %filename)

        else :
            new_csv_file = original_csv_file[columns]
            print(new_csv_file)

            if filename == 'etablissement':
                print('Creating dataframe etablissement...')
                # correction des points-virgules des valeurs par des virgules
                new_csv_file['APP_Libelle_etablissement'] = new_csv_file['APP_Libelle_etablissement'].apply(lambda x: str(x).replace(';',','))
                new_csv_file['Adresse_2_UA'] = new_csv_file['Adresse_2_UA'].apply(lambda x: str(x).replace(';','.'))
                # suppression des doublons
                new_csv_file.drop_duplicates(subset='SIRET', keep='first', ignore_index=True ,inplace=True)
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
                delimiter = '|'
                df = pd.DataFrame(data=None, columns=['SIRET', 'APP_Libelle_activite_etablissement'])
                for i in new_csv_file.index :
                    # on stocke la valeur App_libelle_activite de la ligne
                    list_activities = new_csv_file['APP_Libelle_activite_etablissement'][i]
                    # si cette valeur contient le caractère |
                    if delimiter in list_activities:
                        # on crée une liste qui va contenir les activités résultant du split
                        activities = []
                        activity = list_activities.split(delimiter)
                        activities += activity
                        # on boucle sur la liste des activités qu'on réaffecte au Siret dans un dataframe qu'on concatene dans le df
                        for a in activities :
                            df_activity = pd.DataFrame(data=[[ new_csv_file['SIRET'][i] , a ]], columns=['SIRET', 'APP_Libelle_activite_etablissement'])
                            df = pd.concat([df, df_activity], ignore_index=True)
                        # on supprime la ligne concernée du dataframe source
                        new_csv_file.drop(index=i)
                new_csv_file = pd.concat([new_csv_file, df], ignore_index=True)         
                new_csv_file.drop_duplicates(subset=['SIRET','APP_Libelle_activite_etablissement'], keep='last', ignore_index=True ,inplace=True)
                file_temp = SAVE_CSV_FILEPATH+filename+'_temp.csv'
                new_csv_file.to_csv(path_or_buf=file_temp, sep=';', index=True)
                print("\nFile '%s_temp.csv' created\n" %filename)
                create_csv_concerne(file_temp, db_connect)
            
            if filename == 'domaine_activite':
                print('Creating dataframe domaine_activite...')
                delimiter = '|'
                df_length = len(new_csv_file)
                s = []
                for i in range(0, df_length):
                    row = new_csv_file.iloc[i]
                    lib_activite = row.split(delimiter)
                    s = s + lib_activite
                d = {'APP_Libelle_activite_etablissement': s}
                df = pd.DataFrame(data=d)
                df.drop_duplicates(subset=['APP_Libelle_activite_etablissement'], keep='first', ignore_index=True ,inplace=True)
                print('Dataframe cible created!')
                df.to_csv(path_or_buf=SAVE_CSV_FILEPATH + filename + '.csv', sep=';', index=True)
                print("\nFile '%s.csv' created\n" % filename)

    # gestion des erreurs et exceptions
    except (Exception, IOError) as error:
        print("IOERROR :", error,'\n')


def create_csv_cible(file_temp, db_connect):

    df_source = pd.read_csv(file_temp, sep=";", index_col=0)

    # récupération des données types activites en BDD
    etablissements = pd.DataFrame(Classes.Connection.query_all(db_connect,'select id_etablissement, siret from etablissement;'), columns=['id','siret'])
    etablissements.set_index('siret', inplace=True)
    types = pd.DataFrame(Classes.Connection.query_all(db_connect,'select * from type_activite;'), columns=['id','type'])
    types.set_index('type', inplace=True)

    # Creation d'un df_target pour générer un csv avec de la table de liaison avec id
    df_target = pd.DataFrame(data=None,columns=['id_etablissement','id_type_activite'])
    for index in range(0, len(df_source)):
        siret = df_source['SIRET'][index]
        activite = df_source['ods_type_activite'][index]
        df_new_row = pd.DataFrame({'id_etablissement': [etablissements.loc[siret,'id']],'id_type_activite': types.loc[activite,'id']})
        df_target = pd.concat([df_target,df_new_row], ignore_index=True)

    # Creation d'un fichier csv contenant la listes de ces valeurs et un index numérique
    df_target.to_csv(path_or_buf='database/data/cible.csv', sep=';', index=False)
    print("\nFile 'cible.csv' final created\n")


def create_csv_inspecte(file_temp, db_connect):

    df_source = pd.read_csv(file_temp, sep=";", index_col=0)

    # récupération des données types activites en BDD
    etablissements = pd.DataFrame(Classes.Connection.query_all(db_connect,'select id_etablissement, siret from etablissement;'), columns=['id','siret'])
    etablissements.set_index('siret', inplace=True)
    niveau_hygiene = pd.DataFrame(Classes.Connection.query_all(db_connect,'select * from niveau_hygiene;'), columns=['id', 'niveau'])
    niveau_hygiene.set_index('niveau', inplace=True)
    
    # Creation d'un df_target pour générer un csv avec de la table de liaison avec id
    df_target = pd.DataFrame(data=None,columns=['id_etablissement','id_hygiene','numero_inspection','date_inspection'])
    for index in range(0, len(df_source)):
        siret = df_source['SIRET'][index]
        hygiene = df_source['Synthese_eval_sanit'][index]
        df_new_row = pd.DataFrame({'id_etablissement': [etablissements.loc[siret,'id']],'id_hygiene': [niveau_hygiene.loc[hygiene,'id']],'numero_inspection': [df_source['Numero_inspection'][index]],'date_inspection': [df_source['Date_inspection'][index]]})
        df_target = pd.concat([df_target,df_new_row], ignore_index=True)

    # Creation d'un fichier csv contenant la listes de ces valeurs et un index numérique
    df_target.to_csv(path_or_buf='database/data/inspecte.csv', sep=';', index=False)
    print("\nFile 'inspecte.csv' final created\n")

# CRéation table de relation concerne : id_etablissement et id_domaine_activite
def create_csv_concerne(file_temp, db_connect):

    df_source = pd.read_csv(file_temp, sep=";", index_col=0)

    # récupération des données types activites en BDD
    etablissements = pd.DataFrame(Classes.Connection.query_all(db_connect,'select id_etablissement, siret from etablissement;'), columns=['id','siret'])
    etablissements.set_index('siret', inplace=True)
    domaine = pd.DataFrame(Classes.Connection.query_all(db_connect,'select * from domaine_activite;'), columns=['id', 'domaine'])
    domaine.set_index('domaine', inplace=True)
    
    # Creation d'un df_target pour générer un csv avec de la table de liaison avec id
    df_target = pd.DataFrame(data=None,columns=['id_etablissement','id_activite'])
    for index in range(0, len(df_source)):
        # on stocke la valeur siret et app_libelle du csv source
        siret = df_source['SIRET'][index]
        activite = df_source['APP_Libelle_activite_etablissement'][index]
        # si il y a plusieurs activites dans la variable 'activite' on split
        delimiter = '|'
        if delimiter in activite :
            activities = []
            activity = activite.split(delimiter)
            activities += activity
            for a in activities:
                df_new_row = pd.DataFrame(data=[[ etablissements.loc[siret,'id'] , domaine.loc[a,'id'] ]], columns=['id_etablissement', 'id_activite'])
                df_target = pd.concat([df_target, df_new_row], ignore_index=True)
        else:
            df_new_row = pd.DataFrame(data=[[ etablissements.loc[siret,'id'] , domaine.loc[activite,'id'] ]], columns=['id_etablissement', 'id_activite'])
            df_target = pd.concat([df_target, df_new_row], ignore_index=True)
    
    # Suppression des doublons
    df_target.drop_duplicates(subset=['id_etablissement','id_activite'], keep='last', ignore_index=True ,inplace=True)            
    # Creation d'un fichier csv contenant la liste de ces valeurs et un index numérique
    df_target.to_csv(path_or_buf='database/data/concerne.csv', sep=';', index=False)
    print("\nFile 'concerne.csv' final created\n")




