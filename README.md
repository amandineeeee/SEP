# Les jumeaux numériques appliqués à la sclérose en plaques (SEP)

## Sommaire

- [Présentation générale](#application-daide-à-la-gestion-des-patients-atteints-de-sep)
- [Machine Learning](#création-du-modèle-de-machine-learning-model_trainingpy)
- [Jumeau numérique](#lébauche-dun-jumeau-numérique)
- [Installation et mise en place](#installation-et-mise-en-place)
- [Lancement de l'application](#lancement-de-lapplication)

## Application d'aide à la gestion des patients atteints de SEP

**Auteur: HENRY Amandine**

Cette application permet la gestion numérique des dossiers patients (ajout, modification et suppression de fiches patients).  

Elle intègre également un outil d’aide à la prise de décision qui, à partir d’Imageries par Résonance Magnétique, tente de prédire la présence ou non de SEP chez un patient.  

**Limitation** : 
Le modèle a été entraîné sur un nombre limité de données et **ne doit pas être utilisé en situation réelle**. Il illustre simplement la logique d’application sur un jeu de données médicales plus conséquent.

Par ailleurs, cette application intègre une ébauche de jumeau numérique en illustrant de manière très simplifiée la transmission des signaux d'un neurone à un autre.

**Limitation** : 
En l'absence d'une équipe composée de neurologue, il est très compliqué de créer virtuellement le système nerveux. 
De plus, ayant été confrontée à un manque de données, il n'était pas possible d'alimenter un réel jumeau numérique.

L’interface utilisateur est gérée via Flask, les données sont stockées dans une base MySQL.

## Création du modèle de Machine Learning (model_training.py)

Étant donné que je ne possédais que très peu de données, j’ai choisi d’utiliser un CNN peu
profond afin d’éviter le surapprentissage.
Le modèle que j’ai implémenté a la structure suivante :
- Une couche d’entrée ;
- Une couche de convolution comprenant 32 filtres de taille 3 × 3, utilisant la fonction
d’activation ReLU, qui permet de détecter les motifs dans l’image ;
- Une couche de pooling MaxPooling 2×2 pour réduire la taille des cartes de caractéristiques
et éviter le surapprentissage ;
- Une couche de Flatten pour transformer les matrices en un vecteur unidimensionnel ;
- Une couche dense composée de 64 neurones et utilisant la fonction d’activation ReLU
pour extraire des caractéristiques ;
- Une couche de sortie utilisant la fonction d’activation sigmoïde pour réaliser une classification binaire (SEP ou non).

J’ai utilisé l’optimiseur Adam et l’accuracy comme métrique d’évaluation.
Pour éviter le surapprentissage, j’ai ajouté un callback EarlyStopping qui arrête l’entraînement
si l’accuracy de validation n’augmente plus après 10 epochs.
J’ai également utilisé ReduceLROnPlateau, qui diminue automatiquement le taux d’apprentis-
sage lorsque la perte de validation cesse de s’améliorer, permettant ainsi une convergence plus
stable.
Pour ce qui est des hyperparamètres, j’ai fixé un maximum d’epochs à 20 et un batch size de 3.
Ce choix a été contraint par la quantité limitée de données en ma possession.
J’obtiens une perte à 2.09 et une accuracy à 75%. Ces résultats montrent que le modèle fonctionne
à un niveau acceptable, mais en ce qui concerne la perte, un nette amélioration est possible. Cela s’explique par le fait que le modèle n’a pas suffisamment de données pour apprendre correc-
tement. En effet, le manque de données peut limiter la capacité du modèle à généraliser et à
capturer la variabilité des images.
J’ai aussi tenté d’intégrer des techniques d’augmentation de données afin d’augmenter artificiellement la taille du jeu de données et de diversifier les exemples d’entraînement. Cependant lorsque j’ai voulu l’intégrer à mon application Flask, cela a posé problème.
Afin de rendre mon modèle fiable, il me faudrait beaucoup plus de données.
Si cela était possible, j’aimerais tester divers modèles tels que Random Forest ou encore de
nombreux modèles de réseaux de neurones tels que ResNet.

Pour compiler le fichier correspondant, lancez la commande suivante : 
```
python3 model_training.py
```

## L'ébauche d'un jumeau numérique

Ce projet est une esquisse simplifiée d’un jumeau numérique appliqué à la SEP, une maladie neurodégénérative. L’objectif était de modéliser l’impact de la démyélinisation sur le comportement des neurones.

Pour ce faire, je me suis appuyée sur un modèle de neurone de type Integrate and Fire. En l’absence de données cliniques et de l’expertise d’un neurologue, j’ai opté pour une approche modulaire.
Mon modèle simule :
- Un neurone sain : conduction rapide et efficace.
- Un neurone partiellement démyélinisé : conduction ralentie.
- Un neurone sévèrement démyélinisé : absence de conduction.

Le projet repose sur deux classes Python :
- Neurone, qui simule un neurone simple soumis à un courant constant et génère un potentiel d'action lorsqu’un seuil est atteint.
- NeuroneSEP, qui hérite de Neurone et modifie son comportement selon le degré de démyélinisation, grâce à une constante de temps tau ajustable (20 pour sain, 50 pour endommagé, 100 pour sévère).

Des courbes de potentiel membranaire et un histogramme de spikes illustrent comment la dégradation de la myéline affecte la transmission du signal nerveux et réduit progressivement l'activité neuronale.

Pour compiler le fichier correspondant, lancez la commande suivante : 
```
python3 ebauche_jumeauNumerique.py
```

## Installation et mise en place

### Pré-requis

Avant de commencer, assurez-vous d'avoir installé :  
- **Python 3.8**  
- **Conda**  
- **MySQL**


### Création de la base de données 

- Se connecter à MySQL

```
mysql -u root -p
```

<u>Attention:</u>
Si vous rencontrez l'erreur "ERROR 2002 (HY000): Can't connect to local MySQL server through socket '/tmp/mysql.sock'", cela signifie que le client MySQL utilise un mauvais chemin de socket et vous devez exécuter la conmmande suivante: 

```
mysql -u root -p --socket=/var/run/mysqld/mysqld.sock
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

### Création et activation de l'environnement de travail 

- Créer l'environnement

```
conda env create -f environment.yml
```

- Activer l'environnement 

```
conda activate nom_de_ton_env
```

### Lancement de l'application

```
python3 run.py
```

Pour vous connecter créez votre compte. 