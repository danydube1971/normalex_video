# normalex_video
Pour ajuster le volume d'un fichier vidéo (MKV, MP4, AVI, WEBM)


Ce script, écrit en Python, permet d'ajuster le volume de fichiers vidéo MP4, MKV, AVI et WEBM ou de normaliser leur volume à l'aide de la bibliothèque PyQt5 pour l'interface utilisateur et de FFmpeg pour le traitement vidéo. L’ajustement du volume se fait sans ré-encodage de la vidéo ce qui accélère le traitement.

![Normalex_video](https://github.com/danydube1971/normalex_video/assets/74633244/81735d4b-3947-4f9b-96ad-596af9043e60)

*Testé dans Linux Mint 21.3 sous Python3.10 et 3.11*

**Pré-requis**

    1. Python 3.10 ou supérieur doit être installé sur votre système.
    2. FFmpeg doit être installé et accessible via la ligne de commande.
    3. PyQt5 doit être installé. Vous pouvez l'installer via pip :
       pip install PyQt5
       
       
Utilisation
Lancer le Script
Pour exécuter le script, utilisez la commande suivante dans un terminal :

`python3.10 Normalex_video.py`


Interface Utilisateur

    1. Sélectionner un Fichier Vidéo : Cliquez sur le bouton "Sélectionner un fichier vidéo" pour choisir un fichier vidéo. Le chemin du fichier sélectionné sera affiché.
    2. Entrer le Nombre de Décibels : Saisissez le nombre de décibels pour ajuster le volume (entre -15 et +15).
    3. Choisir l'Action :
        ◦ Sélectionnez "Augmenter" pour augmenter le volume.
        ◦ Sélectionnez "Baisser" pour diminuer le volume.
    4. Ajuster le Volume : Cliquez sur "Ajuster le volume" pour appliquer les changements.
    5. Normaliser le Volume : Cliquez sur "Normalize" pour normaliser le volume du fichier vidéo selon les standards de diffusion.

Messages d'État

Les messages de confirmation ou d'erreur s'afficheront dans une boîte de dialogue.
