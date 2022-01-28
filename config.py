# Variable globale à configurer

 # chemin du fichier csv export_alimconfiance
CSV_SOURCE_FILEPATH = 'data/csv/export_alimconfiance.csv'

# chemin du dossier de destination des nouveaux csv
CSV_DIR_FILEPATH = "data/csv/"

# configuration connection à la BDD POSTGRES
DATABASE = {
    'host':'localhost',
    'dbname':'AlimConfiance', 
    'user':'postgres', 
    'password':'mdppstg75', 
    'port':'5432'
}