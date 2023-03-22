# Deep-Bridge

Le projet "Deep Bridge" vise à développer un programme basé sur l'intelligence artificielle pour détecter les sténoses
carotidiennes, qui pourraient être invisibles à l'œil nu lors d'une première lecture des scanners.

## Contexte

M. Galli nous a fourni un ensemble de dossiers patients (150) contenant des fichiers DICOM et un script
[`rotation_script.py`](rotation_script.py). Ce script permet de lire un ensemble de fichiers DICOM pour un patient
donné, d'analyser les images et d'afficher le résultat dans une fenêtre Tkinter. Notre objectif initial était
de comprendre ce script, rédigé par les étudiants de l'année précédente, et de l'optimiser.

Nous disposions également d'un dossier de fichiers DICOM fonctionnant parfaitement avec
[`rotation_script.py`](rotation_script.py), utilisé pour tester le script.

## Problèmes rencontrés

### Problème 1 : Le téléchargement des dossiers de patients

Les dossiers patients nous ont été fournis par M. Galli sous forme de fichiers `.cab` sur OneDrive. Nous avons
découvert que l'on ne pouvait pas tout télécharger d'un coup, car la taille totale des fichiers était trop importante.
Et surtout que le format des fichiers `.cab` posait un problème à OneDrive, qui ne pouvait pas les zipper correctement.

### Problème 2 : Le script ne fonctionne pas avec tous les dossiers de patients

Nous avons identifié que le script ne fonctionnait pas correctement avec certains dossiers de patients. Nous avons
découvert que les fichiers n'étaient parfois pas correctement classés dans les dossiers des patients et que certains
scans ne contenaient qu'un seul fichier DICOM.

## Ce qu'on a fait

Afin de résoudre ces problèmes, nous avons décidé d'écrire un autre script
[`organize_dicom_files.py`](organize_dicom_files.py)qui lit tous les fichiers
dans tous les dossiers et les classe par patient et par scan. Ceci nous permettra de nous assurer que les fichiers sont
correctement organisés et facilitera l'analyse des images pour détecter les sténoses carotidiennes.

### Le script [`organize_dicom_files.py`](organize_dicom_files.py)

Voici un aperçu des principales fonctionnalités du script :

<ol>
<li>Le script lit les métadonnées des fichiers DICOM en utilisant la bibliothèque pydicom.</li>
<li>Il vérifie si le fichier est un scan CT (tomodensitométrie) et extrait l'ID du patient et l'UID de la série.</li>
<li>Le script crée un nouveau dossier pour chaque patient et série de scans, s'ils n'existent pas déjà.</li>
<li>Il déplace les fichiers DICOM valides vers les dossiers correspondants aux patients et aux séries de scans.</li>
<li>Les fichiers DICOM invalides sont déplacés vers un dossier spécifique invalid_dicom_files.</li>
<li>Les fichiers non-DICOM sont également identifiés et les fichiers avec l'extension .cab sont supprimés.</li>
<li>Enfin, le script affiche des messages d'information et d'avertissement pour faciliter le suivi de son exécution.</li>
</ol>

Pour utiliser le script, il suffit d'exécuter la commande suivante :

```bash
python organize_dicom_files.py <source_folder> <output_folder>
```

où `<source_folder>` est le dossier contenant les fichiers DICOM à organiser.

### Résultats du script [`organize_dicom_files.py`](organize_dicom_files.py) et conclusion