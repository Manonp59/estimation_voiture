import streamlit as st
import pandas as pd 
from joblib import load

df_voitures = pd.read_csv('dataset_voitures_cleaned.csv',index_col='car_ID')

model = load('model.joblib')
    

st.title('Estimation de votre voiture')

st.write('Entrez les caractéristiques de la voiture pour obtenir une estimation de sa valeur.')

fueltype = st.radio('Carburant',('diesel','essence'))
aspiration = st.radio('Aspiration',('std','turbo'))
carbody = st.selectbox('Type de carrosserie',('convertible', 'hayon', 'berline', 'break', 'toit rigide'))
drivewheel = st.radio('Roues motrices',('propulsion', 'traction', 'quatre roues motrices'))
enginelocation = st.radio('Localisation du moteur', ('avant','arriere'))
enginetype = st.selectbox('Type de moteur',('dohc', 'ohcv', 'ohc', 'l', 'rotor', 'ohcf', 'dohcv'))
cylindernumber = st.slider('Nombre de cylindres',min_value=2,max_value=14,step=1)
fuelsystem = st.selectbox('Système carburant',('mpfi', '2bbl', 'mfi', '1bbl', 'spfi', '4bbl', 'idi', 'spdi'))
marque = st.selectbox('Marque',('alfa-romero', 'audi', 'bmw', 'chevrolet', 'dodge', 'honda',
       'isuzu', 'jaguar', 'mazda', 'buick', 'mercury', 'mitsubishi',
       'nissan', 'peugeot', 'plymouth', 'porsche', 'renault', 'saab',
       'subaru', 'toyota', 'volkswagen', 'volvo'))
wheelbase = st.slider('Empattement en cm',min_value=218.0,max_value=308.0)
carlength = st.slider('Longueur de la voiture en cm',min_value=358.0, max_value=529.0)
carwidth = st.slider('Largeur de la voiture en cm',min_value=153.0,max_value=183.0)
carheight =st.slider('Hauteur de la voiture en cm',min_value=121.0, max_value=151.0)
curbweight = st.slider('Poids à vide en kg', min_value=674.0, max_value=1844.0)
enginesize = st.slider ('Cylindrée du moteur en cm cube',min_value=0.8,max_value=5.3)
boreratio = st.slider("Taux d'alésage du moteur (diamètre du cylindre) en mm", min_value=2.0,max_value=4.0)
stroke = st.slider ("Course du piston en mm", min_value=2.0,max_value=5.0)
horsepower = st.slider('Puissance du moteur en chevaux', min_value=40,max_value=350,step=1)
cityconso = st.slider('Consommation de carburant en L/100km en conduite urbaine',min_value=4.0,max_value=20.0)
highwayconso = st.slider('Consommation de carburant en L/100km en conduite urbaine',min_value=4.0,max_value=15.0)


feature_values = pd.DataFrame({'fueltype':fueltype, 'aspiration' :aspiration,'carbody': carbody,
                   'drivewheel': drivewheel, 'enginelocation' : enginelocation, 'wheelbase':wheelbase, 'carlength' :carlength,'carwidth': carwidth, 'carheight':carheight,'curbweight':curbweight,'enginetype':enginetype,'cylindernumber':cylindernumber,'enginesize':enginesize,'fuelsystem':fuelsystem,'boreratio':boreratio,'stroke':stroke,'horsepower' : horsepower,'marque' :marque, 'city L/100km':cityconso,'highway L/100km' :highwayconso},index=[0])

X = df_voitures.drop(['price','peakrpm','modele'],axis=1)

prediction = model.predict(feature_values)

if st.button('Valider'):
    st.write(f'La valeur de la voiture est de {round(prediction[0],2)}$.')
    
