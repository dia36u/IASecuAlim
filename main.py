from database import create_database
from app import create_app
from modele import processus_ETL

database = create_database()
app = create_app()
processus_ETL.launchETL()

# Lancement de l'application
if __name__ == "__main__":
    app.run()

