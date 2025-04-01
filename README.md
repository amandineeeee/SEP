# Application d'aide à la gestion des patients atteints de SEP

**Auteur: HENRY Amandine**

Cette application permet la gestion numérique des dossiers patients (ajout, modification et suppression de fiches patients).  

Elle intègre également un outil d’aide à la prise de décision qui, à partir d’Imageries par Résonance Magnétique, tente de prédire la présence ou non de SEP chez un patient.  

**Limitation** : 
Le modèle a été entraîné sur un nombre limité de données et **ne doit pas être utilisé en situation réelle**. Il illustre simplement la logique d’application sur un jeu de données médicales plus conséquent

# Installation et mise en place

## Pré-requis

Avant de commencer, assurez-vous d'avoir installé :  
- **Python 3.8**  
- **Conda**  
- **MySQL**


## Création de la base de données 

- Se connecter à MySQL

```
mysql -u root -p
```

- Créer une base de données 

```
CREATE DATABASE dossier_medical;
```

- Quitter MySQL et importer le fichier SQL 

```
mysql -u root -p dossier_medical < dossier_medical.sql
```

Une fois cela fait, vous devez changer vos informations de connexion dans le fichier db.py.

## Création et activation de l'environnement de travail 

- Créer l'environnement

```
conda env create -f environment.yml
```

- Activer l'environnement 

```
conda activate nom_de_ton_env
```

## Lancement de l'application

```
python3 run.py
```