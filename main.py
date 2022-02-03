from database import create_database
from app import create_app

# Création de la database Postgres et récup d'un objet connection
database = create_database()

# Création de l'app Flask
app = create_app()

# Lancement de l'application
if __name__ == "__main__":
    app.run()

# Modele Regression Logistique
#exec(open("modele/logisticRegression.py",'r').read())
