# Librairies
from joblib import load
from fastapi import FastAPI, HTTPException, Request
import uvicorn
from typing import Optional
from pydantic import BaseModel
import pandas as pd
import crud
import hashlib
from jose import jwt
import sqlite3

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"

# Chargement du modèle
loaded_model = load('ridge.joblib')

# Création d'une instance FastApi
app = FastAPI()

# Classes contenu
class UserRegister(BaseModel):
    nom:str
    email:str
    mdp:str
    
class UserLogin(BaseModel):
    email:str
    mdp:str

# Définition d'un objet (une classe) pour réaliser des requêtes 
class request_body(BaseModel):
    fueltype : str
    aspiration : str
    carbody : str
    drivewheel : str
    enginelocation : str
    wheelbase : float 
    carlength : float
    carwidth : float
    carheight : float
    curbweight : float
    enginetype : str
    cylindernumber : int
    enginesize : float
    fuelsystem : str
    boreratio : float
    stroke : float
    horsepower : int
    marque : str
    cityconso : float
    highwayconso :float
    
class ajout_prix(BaseModel):
    prix_reel : float
    id_voiture : int 
    
# Fonctions utiles :
def hasher_mdp(mdp:str) -> str:
    return hashlib.sha256(mdp.encode()).hexdigest()


def decoder_token(token:str)->dict:
    return jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)

def verifier_token(req: Request):
    token = req.headers["Authorization"]
    
@app.post("/api/auth/inscription")
async def inscription(user:UserRegister):
    if len(crud.get_users_by_mail(user.email)) > 0:
        raise HTTPException(status_code=403, detail="L'email fourni possède déjà un compte")
    else:
        id_user = crud.creer_utilisateur(user.nom, user.email, hasher_mdp(user.mdp), None)
        token = jwt.encode({
            "email" : user.email,
            "mdp" : user.mdp,
            "id" : id_user
        }, SECRET_KEY, algorithm=ALGORITHM)
        crud.update_token(id_user, token)
        return {"token" : token}
    
@app.post("/api/auth/token")
async def login_token(user:UserLogin):
    resultat = crud.obtenir_jwt_depuis_email_mdp(user.email, hasher_mdp(user.mdp))
    if resultat is None:
        raise HTTPException(status_code=401, detail="Login ou mot de passe invalide")
    else:
        return {"token":resultat[0]}

# Définition du chemin du point de terminaison (API)
@app.post('/predict') # local : http://127.0.0.1:8000/predict
# Définiction de la fonction de prédiction 
def predict(data : request_body, req:Request):
    decode = decoder_token(req.headers["Authorization"])
    proprietaire_id = decode['id']
    if crud.verifier_existence_token(proprietaire_id) :
        # Nouvelles données sur lesquelles on fait la prédiction
        new_data = pd.DataFrame({'fueltype':data.fueltype, 'aspiration' : data.aspiration,'carbody': data.carbody,
                'drivewheel': data.drivewheel, 'enginelocation' : data.enginelocation, 'wheelbase':data.wheelbase, 'carlength' :data.carlength,'carwidth': data.carwidth, 'carheight':data.carheight,'curbweight':data.curbweight,'enginetype':data.enginetype,'cylindernumber':data.cylindernumber,'enginesize':data.enginesize,'fuelsystem':data.fuelsystem,'boreratio':data.boreratio,'stroke':data.stroke,'horsepower' : data.horsepower,'marque' :data.marque, 'city L/100km':data.cityconso,'highway L/100km' :data.highwayconso},index=[0])

        # Prédiction 
        prediction = loaded_model.predict(new_data)[0]
        decode = decoder_token(req.headers["Authorization"])
        proprietaire_id = decode['id']
        crud.creer_voiture(proprietaire_id,data.fueltype, data.aspiration,data.carbody,data.drivewheel,data.enginelocation, data.wheelbase, data.carlength, data.carwidth, data.carheight, data.curbweight, data.enginetype, data.cylindernumber, data.enginesize, data.fuelsystem,data.boreratio, data.stroke, data.horsepower, data.marque, data.cityconso, data.highwayconso, prediction)

        return {"prediction" : round(prediction,2)}
    else : raise HTTPException(status_code=401, detail="Vous devez être identifiés pour accéder à cet endpoint")
    


@app.get("/api/voitures")
async def mes_voitures(req: Request):
    decode = decoder_token(req.headers["Authorization"])
    proprietaire_id = decode['id']
    if crud.verifier_existence_token(proprietaire_id) :
        voitures = crud.obtenir_voiture_user(proprietaire_id)
    return voitures

@app.post("/api/ajouter_prix_voitures")
def ajouter_prix_reel(data:ajout_prix,req:Request):
    decode = decoder_token(req.headers["Authorization"])
    proprietaire_id = decode['id']
    if crud.verifier_existence_token(proprietaire_id) :
        crud.ajouter_prix_vente(data.id_voiture,data.prix_reel)
        crud.ajouter_csv(data.id_voiture)
        return ('Le prix a bien été ajouté.')
    else :
        raise HTTPException(status_code=401, detail="Vous devez être identifiés pour accéder à cet endpoint")