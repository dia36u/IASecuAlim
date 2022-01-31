import psycopg2 as pg
from config import DATABASE


class Connection:

    # Fonction retournant une connection à la database
    @staticmethod
    def connection_to_database():
        conn = None
        try:
            print('\nConnecting to the PostgreSQL database...')
            conn = pg.connect(host=DATABASE['host'], dbname='AlimConfiance', user=DATABASE['user'], password=DATABASE['password'], port=DATABASE['port'])
            print("Connection successful\n")
        # gestion des erreurs et exceptions
        except (Exception, pg.DatabaseError) as error:
            print("POSTGRES ERROR :")
            print(error)
        return conn

    # Fonction vérifiant l'existance de la table etablissement
    @staticmethod
    def table_exists(conn):
        results = Connection.query_all(conn, "SELECT tablename FROM pg_catalog.pg_tables WHERE schemaname != 'pg_catalog' AND schemaname != 'information_schema';")
        for result in results:
            if str(result) == "('etablissement',)":
                return True
    
    # Fonction vérifiant l'existance de donnée dans une table
    @staticmethod
    def data_exist(conn, table):
        result = Connection.query_one(conn, "SELECT * FROM %s;" %table)
        if result :
            return True
    
    # Requête retournant un tableau de select
    @staticmethod
    def query_all(conn, query):
        cursor = conn.cursor()
        try:
            cursor.execute(query)
            conn.commit()
            results = cursor.fetchall()
            cursor.close()
            print("\nQuery successful: %s \n" % query)
            return results
        except (Exception, pg.DatabaseError) as error:
            print("POSTGRES ERROR :")
            print(error)
            conn.rollback()
            cursor.close()

    # Requête retournant la première ligne d'un select
    @staticmethod
    def query_one(conn, query):
        cursor = conn.cursor()
        try:
            cursor.execute(query)
            conn.commit()
            results = cursor.fetchone()
            cursor.close()
            print("\nQuery successful: %s \n" % query)
            return results
        except (Exception, pg.DatabaseError) as error:
            print("POSTGRES ERROR :")
            print(error)
            conn.rollback()
            cursor.close()
    
    # Requête inserant des données
    @staticmethod
    def copy_from(conn, file, table):
        cursor = conn.cursor()
        with open(file, mode='r', encoding="utf-8") as line:
            next(line) # Saute la première ligne.
            try:
                # copie de la ligne
                if table == 'etablissement':
                    cursor.copy_from(line, table, columns=('id_etablissement','libelle','siret' ,'adresse','code_postal','commune','coordonnees_gps','agrement'), sep=';')
                if table == 'cible':
                    cursor.copy_from(line, table, columns=('id_etablissement','id_type_activite'), sep=';')
                if table == 'inspecte':
                    cursor.copy_from(line, table, columns=('id_etablissement','id_hygiene', 'numero_inspection', 'date_inspection'), sep=';')
                else :
                    cursor.copy_from(line, table, sep=';')
                conn.commit()
                cursor.close()
                print("\nCopy_from_file %s successful\n" %file)
            except (Exception, pg.DatabaseError) as error:
                print("POSTGRES ERROR :")
                print(error)
                conn.rollback()
                cursor.close()