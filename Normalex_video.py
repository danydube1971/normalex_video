#!/usr/bin/env python3.10


import os
import subprocess
from PyQt5 import QtWidgets, QtCore, QtGui

class VolumeAdjusterApp(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()
    
    def initUI(self):
        self.setWindowTitle('Normalex_video (MP4, MKV, AVI, WEBM)')
        
        # Définir la taille de la fenêtre principale
        self.resize(600, 400)
        
        # Layout principal
        layout = QtWidgets.QVBoxLayout()

        # Bouton pour sélectionner un fichier vidéo
        self.fileButton = QtWidgets.QPushButton('Sélectionner un fichier vidéo', self)
        self.fileButton.clicked.connect(self.selectFile)
        layout.addWidget(self.fileButton)

        # Label pour afficher le fichier sélectionné
        self.fileLabel = QtWidgets.QLabel('Aucun fichier sélectionné', self)
        layout.addWidget(self.fileLabel)

        # Champ pour entrer le nombre de décibels
        self.dbLabel = QtWidgets.QLabel('Nombre de décibels à ajuster:', self)
        layout.addWidget(self.dbLabel)
        
        self.dbInput = QtWidgets.QLineEdit(self)
        layout.addWidget(self.dbInput)

        # Radio buttons pour choisir augmenter ou baisser le volume
        self.radioGroup = QtWidgets.QGroupBox('Action')
        self.radioLayout = QtWidgets.QHBoxLayout()

        self.increaseRadio = QtWidgets.QRadioButton('Augmenter', self)
        self.increaseRadio.setChecked(True)
        self.radioLayout.addWidget(self.increaseRadio)

        self.decreaseRadio = QtWidgets.QRadioButton('Baisser', self)
        self.radioLayout.addWidget(self.decreaseRadio)

        self.radioGroup.setLayout(self.radioLayout)
        layout.addWidget(self.radioGroup)

        # Bouton pour lancer l'ajustement du volume
        self.adjustButton = QtWidgets.QPushButton('Ajuster le volume', self)
        self.adjustButton.clicked.connect(self.adjustVolume)
        layout.addWidget(self.adjustButton)

        # Bouton pour normaliser le volume
        self.normalizeButton = QtWidgets.QPushButton('Normalize', self)
        self.normalizeButton.clicked.connect(self.normalizeVolume)
        layout.addWidget(self.normalizeButton)

        # Label pour afficher les messages d'état
        self.statusLabel = QtWidgets.QLabel('', self)
        layout.addWidget(self.statusLabel)

        self.setLayout(layout)

    def selectFile(self):
        options = QtWidgets.QFileDialog.Options()
        fileName, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Sélectionner un fichier vidéo", "", "Fichiers Vidéo (*.mkv *.mp4 *.avi *.webm)", options=options)
        if fileName:
            self.fileLabel.setText(fileName)
            self.fileName = fileName

    def adjustVolume(self):
        try:
            fichier_video = self.fileLabel.text()
            db = self.dbInput.text()
            
            if not db:
                self.showMessage("Vous devez entrer un nombre compris entre -15 et +15.")
                return
            
            try:
                db_value = float(db)
            except ValueError:
                self.showMessage("Vous devez entrer un nombre valide.")
                return

            if db_value < -15 or db_value > 15:
                self.showMessage("Vous devez entrer un nombre compris entre -15 et +15.")
                return

            if self.increaseRadio.isChecked():
                db_suffix = f"_+{db}dB"
                db_value = f"{db}dB"
            else:
                db_suffix = f"_-{db}dB"
                db_value = f"-{db}dB"

            # Déterminer le conteneur de sortie en fonction de l'extension du fichier vidéo
            base_name, extension = os.path.splitext(fichier_video)
            extension = extension.lower()

            if extension == '.webm':
                codec_audio = 'libvorbis'
            else:
                if extension in ['.mkv', '.mp4', '.avi']:
                    codec_audio = 'aac'
                else:
                    self.statusLabel.setText("Format de fichier non supporté.")
                    return

            # Construire le nom de fichier de sortie avec le suffixe de dB
            output_file = base_name + db_suffix + extension

            # Échapper les caractères spéciaux dans les chemins de fichiers
            fichier_video_escaped = fichier_video.replace("'", "'\\''")
            output_file_escaped = output_file.replace("'", "'\\''")

            # Commande FFmpeg pour ajuster le volume
            commande = f"ffmpeg -i '{fichier_video_escaped}' -c:v copy -af 'volume={db_value}' -c:a {codec_audio} '{output_file_escaped}'"
            
            # Exécuter la commande FFmpeg pour ajuster le volume
            subprocess.run(commande, shell=True, check=True)
            
            # Afficher un message de confirmation dans une boîte de dialogue
            self.showMessage(f"Le fichier vidéo '{fichier_video}' a été ajusté de {db_value}. Fichier de sortie : '{output_file}'.")
        except Exception as e:
            self.showMessage(f"Erreur : {e}")

    def normalizeVolume(self):
        try:
            fichier_video = self.fileLabel.text()
            
            # Déterminer le conteneur de sortie en fonction de l'extension du fichier vidéo
            base_name, extension = os.path.splitext(fichier_video)
            extension = extension.lower()

            if extension == '.webm':
                codec_audio = 'libvorbis'
            else:
                if extension in ['.mkv', '.mp4', '.avi']:
                    codec_audio = 'aac'
                else:
                    self.statusLabel.setText("Format de fichier non supporté.")
                    return

            # Construire le nom de fichier de sortie avec le suffixe de normalisation
            output_file = base_name + "_normalized" + extension

            # Échapper les caractères spéciaux dans les chemins de fichiers
            fichier_video_escaped = fichier_video.replace("'", "'\\''")
            output_file_escaped = output_file.replace("'", "'\\''")

            # Commande FFmpeg pour normaliser le volume
            commande = f"ffmpeg -i '{fichier_video_escaped}' -c:v copy -af loudnorm=I=-23:TP=-2:LRA=11 -c:a {codec_audio} '{output_file_escaped}'"
            
            # Exécuter la commande FFmpeg pour normaliser le volume
            subprocess.run(commande, shell=True, check=True)
            
            # Afficher un message de confirmation dans une boîte de dialogue
            self.showMessage(f"Le fichier vidéo '{fichier_video}' a été normalisé. Fichier de sortie : '{output_file}'.")
        except Exception as e:
            self.showMessage(f"Erreur : {e}")

    def showMessage(self, message):
        msgBox = QtWidgets.QMessageBox()
        msgBox.setIcon(QtWidgets.QMessageBox.Information)
        msgBox.setText(message)
        msgBox.setWindowTitle("Confirmation")
        msgBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
        msgBox.exec()

if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ex = VolumeAdjusterApp()
    ex.show()
    sys.exit(app.exec_())

