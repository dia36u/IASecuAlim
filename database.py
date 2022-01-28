import pandas as pd
import numpy as np
import psycopg2 as pg
from config import DATABASE

class Connection(object) :

    def __init__(self) -> None:
        pass

    # Fonction retournant une connection à la database
    @staticmethod
    def connection_to_database(self):
        conn = None
        try:
            print('\nConnecting to the PostgreSQL database...')
            conn = pg.connect(host=DATABASE['host'], dbname=DATABASE['dbname'], user=DATABASE['user'], password=DATABASE['password'], port=DATABASE['port'])
            print("Connection successful\n")
        # gestion des erreurs et exceptions
        except (Exception, pg.DatabaseError) as error:
            print("Error: %s" % error)
        self.conn = conn
        return conn

    @staticmethod
    def execute_query(self, query):
        cursor = self.con.cursor()
        try:
            cursor.execute(query)
            self.conn.commit()
            cursor.close()
            print("\nQuery successful\n")
        except (Exception, pg.DatabaseError) as error:
            print("Error: %s" % error)
            self.con.rollback()
            cursor.close()
            

# Fonction exécutant un script à partir d'un fichier SQL
def execute_SQL_script(script_filepath):
# Connection à la base de données
    connection = Connection.connection_to_database()
    # Récupération du pointeur mémoire
    cursor = connection.cursor()
    # Lecture du fichier ligne par ligne
    try:
        cursor.execute(open(script_filepath, mode='r').read())
        connection.commit()
        cursor.close()
        print("\nQuery successful\n")
    except (Exception, pg.DatabaseError) as error:
        print("Error: %s" % error)
        connection.rollback()
        cursor.close()

# Fonction executant une requête retournant une liste
def request_all(sql_statement):
    # Connection à la base de données
    connection = Connection.connection_to_database()
    # Récupération du pointeur mémoire
    cursor = connection.cursor()
    # Lecture du fichier ligne par ligne
    try:
        cursor.execute(sql_statement)
        results = cursor.fetchall()
        connection.commit()
        cursor.close()
        print("\nQuery successful\n")
        return results
    except (Exception, pg.DatabaseError) as error:
        print("Error: %s" % error)
        connection.rollback()
        cursor.close()

# Requête POSTGRES pour afficher la liste des databases
def show_databases():
    connection = Connection.connection_to_database()
    cursor = connection.cursor()
    sql_statement = 'SELECT datname FROM pg_database;'
    cursor.execute(sql_statement)
    results = cursor.fetchall()
    connection.commit()
    cursor.close()
    return results

# Fonction inserant des données dans la 'table' depuis un fichier csv ressource 'file'
def copy_from_file(table, file):
     # Connection à la base de données
    connection = Connection.connection_to_database()
    # Récupération du pointeur mémoire
    cursor = connection.cursor()
    # Lecture du fichier ligne par ligne
    with open(file, mode='r', encoding="utf-8") as line:
        next(line) # Saute la première ligne.
        try:
            # copie de la ligne
            cursor.copy_from(line, table,sep=';')
            connection.commit()
            cursor.close()
            print("\nCopy_from_file() successful\n")
        except (Exception, pg.DatabaseError) as error:
            print("Error: %s" % error)
            connection.rollback()
            cursor.close()

# Fonction pour insérer les données d'un CSV dans la table etablissement
def copy_from_file_multicolumns(file):
     # Connection à la base de données
    connection = Connection.connection_to_database()
    # Récupération du pointeur mémoire
    cursor = connection.cursor()
    # Lecture du fichier ligne par ligne
    with open(file, mode='r', encoding="utf-8") as line:
        next(line) # Saute la première ligne.
        try:
            # copie de la ligne
            cursor.copy_from(line, 'etablissement', columns=('id_etablissement','libelle','siret' ,'adresse','code_postal','commune','coordonnees_gps','agrement'), sep=';')
            connection.commit()
            cursor.close()
            print("\nCopy_from_file() successful\n")
        except (Exception, pg.DatabaseError) as error:
            print("Error: %s" % error)
            connection.rollback()
            cursor.close()

