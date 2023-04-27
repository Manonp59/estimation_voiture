import sqlite3
import csv

# Ajouter un élément dans la BDD 

def creer_utilisateur(nom:str,email:str,mdp:str,jwt:str) -> int:
    connexion = sqlite3.connect('bdd.db')
    curseur = connexion.cursor()
    curseur.execute("""
                    INSERT INTO utilisateur VALUES (NULL, ?, ?, ?,?)
                    """,(nom, email, mdp, jwt))
    id_user = curseur.lastrowid
    connexion.commit()
    connexion.close()
    return id_user

def creer_voiture(proprietaire_id,fueltyp:str,aspiration:str,carbody:str, drivewheel:str, enginelocation:str, wheelbase:float,carlength:float, carwidth:float, carheight:float, curbweight:float, enginetype:str,cylindernumer:int, enginesize:float, fuelsystem:str,boreratio:float,stroke:float,horsepower:int,marque:str,cityconso:float,highwayconso:float,prix_estimation:float):
    connexion = sqlite3.connect('bdd.db')
    curseur = connexion.cursor()
    curseur.execute("""
                    INSERT INTO voiture VALUES (NULL,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,NULL)
                    """,(proprietaire_id,fueltyp,aspiration,carbody, drivewheel, enginelocation, wheelbase,carlength, carwidth, carheight, curbweight, enginetype,cylindernumer, enginesize, fuelsystem,boreratio,stroke,horsepower,marque,cityconso,highwayconso,prix_estimation))
    connexion.commit()
    connexion.close()
    
# Auth utilisateur : 

def obtenir_jwt_depuis_email_mdp(email:str, mdp:str):
    connexion = sqlite3.connect("bdd.db")
    curseur = connexion.cursor()
    curseur.execute("""
                    SELECT jwt FROM utilisateur WHERE email=? AND mdp=?
                    """, (email, mdp))
    resultat = curseur.fetchone()
    connexion.close()
    return resultat
    
def get_users_by_mail(mail:str):
    connexion = sqlite3.connect("bdd.db")
    curseur = connexion.cursor()
    curseur.execute("""
                    SELECT * FROM utilisateur WHERE email=?
                    """, (mail,))
    resultat = curseur.fetchall()
    connexion.close()
    return resultat

def get_id_user_by_email(email:str):
    connexion = sqlite3.connect("bdd.db")
    curseur = connexion.cursor()
    curseur.execute("""
                    SELECT id FROM utilisateur WHERE email=?
                    """, (email,))
    resultat = curseur.fetchone()
    connexion.close()
    return resultat

# UPDATE 

def update_token(id, token:str)->None:
    connexion = sqlite3.connect("bdd.db")
    curseur = connexion.cursor()
    curseur.execute("""
                    UPDATE utilisateur
                        SET jwt = ?
                        WHERE id=?
                    """,(token, id))
    connexion.commit()
    connexion.close()
    
def ajouter_prix_vente(id, prix_reel:float)->None:
    connexion = sqlite3.connect("bdd.db")
    curseur = connexion.cursor()
    curseur.execute("""
                    UPDATE voiture
                        SET prix_reel = ?
                        WHERE id=?
                    """,(prix_reel, id))
    connexion.commit()
    connexion.close()

def ajouter_csv(id):
    connexion = sqlite3.connect("bdd.db")
    curseur = connexion.cursor()
    curseur.execute("""
                    SELECT * FROM voiture WHERE id = ?
                    """, (id,))
    resultat = curseur.fetchall()[0]
    print(resultat[0])
    connexion.close()
    [(3, 2, 'essence', 'std', 'convertible', 'propulsion', 'avant', 225.04, 428.75, 162.81, 123.95, 1155.75, 'dohc', 4, 2.13, 'mpfi', 3.47, 2.68, 111, 'alfa-romero', 11.0, 8.0, 15265.233128846092, 16000)]
    with open('dataset_voitures_cleaned.csv', mode='a',newline='') as f:
        fieldnames = ['car_id',
                      'symboling',
                    'fueltype',
                    'aspiration',
                    'doornumber',
                    'carbody',
                    'drivewheel',
                    'enginelocation',
                    'wheelbase',
                    'carlength',
                    'carwidth',
                    'carheight',
                    'curbweight',
                    'enginetype',
                    'cylindernumber',
                    'enginesize',
                    'fuelsystem',
                    'boreratio',
                    'stroke',
                    'compressionratio',
                    'horsepower',
                    'peakrpm',
                    'price',
                    'marque',
                    'modele',
                    'cityconso',
                    'highwayconso'
                    ]
        writer = csv.DictWriter(f,fieldnames=fieldnames)
        writer.writerow({'car_id':0,
                      'symboling':0,'fueltype':resultat[2], 'aspiration' : resultat[3],
                      'doornumber':0,
                      'carbody': resultat[4],
                'drivewheel': resultat[5], 'enginelocation' : resultat[6], 'wheelbase':resultat[7], 'carlength' :resultat[8],'carwidth': resultat[9], 'carheight':resultat[10],'curbweight':resultat[11],'enginetype':resultat[12],'cylindernumber':resultat[13],'enginesize':resultat[14],'fuelsystem':resultat[15],'boreratio':resultat[16],'stroke':resultat[16],
                'compressionratio':0,
                'horsepower' :resultat[18],
                'peakrpm':0,
                'price':resultat[23],
                'marque' :resultat[19], 'modele':0,'cityconso':resultat[20],'highwayconso' :resultat[21]})
    
    
    

# Obtenir voitures d'un utilisateur : 

def obtenir_voiture_user(user_id:int) -> list:
    print(user_id)
    connexion = sqlite3.connect("bdd.db")
    curseur = connexion.cursor()
    curseur.execute("""
                    SELECT * FROM voiture WHERE proprietaire_id = ?
                    """, (user_id,))
    resultat = curseur.fetchall()
    connexion.close()
    return resultat

def verifier_existence_token(proprietaire_id:int)-> bool:
    connexion = sqlite3.connect("bdd.db")
    curseur = connexion.cursor()
    curseur.execute("""
                    SELECT * FROM utilisateur WHERE id = ?
                    """, (proprietaire_id,))
    resultat = curseur.fetchall()
    connexion.close()
    if resultat is None : 
        return False
    else : 
        return True

