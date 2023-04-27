# estimation_voiture

Ce brief est réalisé dans le cadre de la formation Développeuse en Intelligence Artificielle. 
Le sujet du brief est de réaliser une application qui utilise un modèle de régression linéaire pour prédire le prix de vente d'une voiture d'après ses caractéristiques. 

Il a pour objectif de développer les compétences suivantes : 
- Qualifier les données grâce à des outils d’analyse et de visualisation de données en vue de vérifier leur adéquation avec le projet ;
- Programmer l’import de données initiales nécessaires au projet en base de données, afin de les rendre exploitables par un tiers, dans un langage de programmation adapté et à partir de la stratégie de nettoyage des données préalablement définie ;
- Préparer les données disponibles depuis la base de données analytique en vue de leur utilisation par les algorithmes d’intelligence artificielle. 

Ainsi, le dossier contient les fichiers suivants : 
- analyse.ipynb : nettoyage et analyse du dataset de départ ; 
- modélisation : conception du modèle de machine learning ;
- model.joblib : stocke le modèle conçu pour qu'il puisse être réutilisé dans l'application ; 
- app_streamlit : application streamlit qui utilise le modèle de machine learning pour prédire le prix d'une voiture. 

En bonus, il nous a été proposé de rendre le modèle accessible via une API, sur laquelle est utilisée un système d'authentification. Il est aussi demandé de rendre possible la saisie par l'utilisateur du prix réel de vente, afin que les informations soient enregistrées dans le dataset et enrichissent les données pour l'entraînement du modèle. Cela a donc nécessité l'utilisation de FastAPI et la conception d'une base de données SQL. Les fichiers suivants poursuivent cet objectif : 
- bdd.db : base de données qui contient les utilisateurs de l'API et les voitures qu'ils enregistrent lorsqu'ils utilisent l'API ;
- creer_db.py : permet de créer la base de données contenant les utilisateurs et les voitures ; 
- crud.py : contient toutes les fonctions pour interagir avec la base de données ; 
- main.py : contient les fonctions qui ont permis la création de l'API et les interactions avec elle.

Le fichier requirements vous permet d'installer les packages nécessaires à l'exécution du projet. 