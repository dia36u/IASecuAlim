from database import create_database
from app import create_app

database = create_database()
app = create_app()

# Lancement de l'application
if __name__ == "__main__":
    app.run()

