import sqlite3

connexion = sqlite3.connect('bdd.db')

curseur = connexion.cursor()

curseur.execute("""
                CREATE TABLE IF NOT EXISTS utilisateur(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nom TEXT NOT NULL,
                    email TEXT NOT NULL UNIQUE, 
                    mdp TEXT NOT NULL, 
                    jwt TEXT
                )
                """)

curseur.execute("""
                CREATE TABLE IF NOT EXISTS voiture(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    proprietaire_id INTEGER,
                    fueltype TEXT NOT NULL,
                    aspiration TEXT NOT NULL,
                    carbody TEXT NOT NULL,
                    drivewheel TEXT NOT NULL,
                    enginelocation TEXT NOT NULL,
                    wheelbase REAL NOT NULL,
                    carlength REAL NOT NULL,
                    carwidth REAL NOT NULL,
                    carheight REAL NOT NULL,
                    curbweight REAL NOT NULL,
                    enginetype TEXT NOT NULL,
                    cylindernumber INTEGER NOT NULL,
                    enginesize REAL NOT NULL,
                    fuelsystem TEXT NOT NULL,
                    boreratio REAL NOT NULL,
                    stroke REAL NOT NULL,
                    horsepower INTEGER NOT NULL,
                    marque TEXT NOT NULL,
                    cityconso REAL NOT NULL,
                    highwayconso REAL NOT NULL,
                    prix_estimation REAL NOT NULL, 
                    prix_reel INTEGER,
                    FOREIGN KEY (proprietaire_id) REFERENCES utilisateur(id) ON DELETE CASCADE
                )
                """)

connexion.commit()

connexion.close()