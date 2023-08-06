# Génération-image_Gaston
## Description
Génération-image_Gaston est un package Python qui permet de générer des images à partir d'un prompt donné en utilisant le site craiyon.com. Ce package utilise Selenium pour automatiser le processus de génération et de téléchargement des images.

## Installation
Vous pouvez installer le package Génération-image_Gaston en utilisant pip :

pip install Génération-image_Gaston
Assurez-vous d'avoir les dépendances suivantes installées :

undetected_chromedriver
selenium
Elle s'installe toute seul normalement
## Utilisation
Voici un exemple d'utilisation du package :


from Generation_Image_Gaston import SelectStyle

SelectStyle("Trois Chat qui pleure...", "PHOTO")
La fonction SelectStyle prend deux paramètres :

Prompt : Le texte à utiliser comme prompt pour générer l'image.
Style : Le style d'image souhaité. Les options disponibles sont "PHOTO", "DESSIN" et "ART".
La fonction effectue les étapes suivantes :

Ouvre le site craiyon.com.
Accepte les cookies (si nécessaire).
Sélectionne le style d'image spécifié.
Saisit le prompt donné.
Génère l'image.
Télécharge l'image sur votre ordinateur.
Veuillez noter que le processus de génération peut prendre du temps. Une fois le téléchargement terminé, le message "Le téléchargement est fini" sera affiché.

Assurez-vous d'avoir Chrome installé sur votre système, car le package utilise Chrome pour interagir avec le site web.