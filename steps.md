# Étapes reproduites

## Étape 1 : Téléchargement des dossiers de patients

Il y a 150 dossiers patients en tout à télécharger, dans le dossier, on trouve des fichiers `.cab` et des dossiers déjà
décompressés. On a donc besoin de décompresser les fichiers `.cab` une fois téléchargés.

## Étape 2 : Trier les fichiers DICOM par patient et par scan

 > :warning: **Warning:** À noter qu'avant d'exécuter le script [`organize_dicom_files.py`](organize_dicom_files.py), il **faut faire une copie**
des dossiers patients dans un autre dossier. Parce que le script ne copie pas les fichiers dicom pour les organiser,
mais il les déplace. Donc, si on veut garder les dossiers patients originaux, il faut faire une copie avant d'exécuter.
En sachant qu'il faut avoir une copie du dossier original pour l'étape 3.


Le script [`organize_dicom_files.py`](organize_dicom_files.py) permet de trier les fichiers DICOM par patient et par
scan.
Il lit tous les fichiers dans tous les dossiers et les classe par patient et par scan.

## Étape 3 : Analyse du résultat d'organisation

Le script [`analyse_results.py`](analyse_results.py) permet d'avoir une idée de ce qu'on a comme résultat après avoir
exécuté le script [`organize_dicom_files.py`](organize_dicom_files.py). Il affiche le nombre de dossiers patients
avec des fichiers DICOM corrects, le nombre de scan par patient, le nombre de fichiers DICOM par scan.

## Étape 4 : Analyse des images

Le script [`rotation_script.py`](rotation_script_1.py) permet d'analyser les images. Il enlève les fichiers
ne contenant la métadonnée `Modality` et la métadonnée `SliceLocation`. On ne peut pas détecter les sténoses
carotidiennes avec ce script automatiquement, mais on peut toutefois les voir sur les images dans les deux carotides
avec la fonctionnalité de rotation que le script fournit.