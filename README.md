#### PERSO
<div align="center">
  <h1>Notifications TooGoodToGo</h1> 
</div>

### > Projet en cours de développement! 👷

## Disclaimer
⚠️ Attention ! Ce projet enfreint les conditions générales de l'application. <br>
###### (6. Propriété Intellectuelle - "L’Utilisateur ne doit pas recourir à des pratiques abusives sur la Plateforme (telles que le piratage ou l’extraction de contenu)")
Je ne suis en aucun cas responsable de l'utilisation que vous allez faire de ce projet. TGTG peut bloquer totalement ou temporairement l'accès à votre compte en l'utilisant. Je vous invite à lire leurs conditions générales d'utilisation <a href=https://www.toogoodtogo.com/fr/terms-and-conditions-using-the-app><u>ici</u></a>👈<br>

De plus, je ne suis ni associé où autorisé par TGTG.

## Motivations 
Je réalise ce projet à la fin de ma 2ème année de Licence Informatique à Sorbonne Université. <br>

TooGoodToGo est une application que j'utilise régulièrement. A ce jour, celle-ci ne possède pas de **système de notifications** permettant de prévenir de l'arrivée de nouveaux paniers sur la plateforme. Je souhaite donc mettre en place un système qui permettra de répondre à ce problème.

Ce projet me permettra d'appliquer et de développer mes connaissances apprises au cours de l'année.

## Installation 
1- Installer le module tgtg
```console
pip install tgtg-python
```

2- Lancer le programme et suivre les indications du terminal
```console
python3 main.py
```

## Fonctionnalités 
###### (implémentées ou prochainement implémentées)
-   Détecter quand un nouveau panier est disponible (✔️)
  
-   Recevoir des notifications lors de l'arrivée de nouveaux paniers
-   Configurer la période de réception des notifications
-    Configurer la fréquence de raffraîchissemnt des paniers
-    Configurer une zone géographique pour les notifcations (favoris dans la zone ou non - radius autour d'un point donné)
-    Prédire quand un panier va être disponible (en se basant sur ses anciennes apparitions)

Prochaine étape :
-   Restructuration du code
-   Configuration des premiers services de notification