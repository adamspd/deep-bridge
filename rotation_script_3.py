"""
Versions :
Python 3.11.0
pip 23.0

Pour installer les bibliothèques, utilisez la commande suivante :
- pip install -r requirements.txt
"""
import os
import sys

import cv2
import numpy as np
import pydicom

np.set_printoptions(threshold=sys.maxsize)

"""
ROTATION_X : la valeur du centre de la rotation par default
files : la liste des fichiers d'un dossier patients
dossier : le chemin vers LE dossier patient à afficher,
        vous devez laisser que les fichier .dcm dans ce dossier.
        (pas de fichier .txt ou .tmp)
"""

ROTATION_X = 332
files = []
dossier = "/Users/adamspierredavid/developer/PycharmProjects/deep_bridge/deep-bridge-tpt/patients/dossier_1"

"""
Chargement des fichiers
"""
print('glob: {}'.format(dossier))
for root, dirs, filenames in os.walk(dossier):
    for filename in filenames:
        if filename.endswith('.dcm') and not filename.startswith('.'):
            filepath = os.path.join(root, filename)
            files.append(pydicom.dcmread(filepath, force=True))

print("file count: {}".format(len(files)))

"""
Supprimer les fichier qui n'ont pas une SliceLocation
SliceLocation nous permet de connaitre l'emplacement du fichier 
dans l'ensemble du dossier patients.
"""
slices = []
skip_count = 0
for f in files:
    if hasattr(f, 'SliceLocation'):
        slices.append(f)
    else:
        skip_count = skip_count + 1
print("skipped, no SliceLocation: {}".format(skip_count))

"""
Ordonner les fichiers
"""

slices = sorted(slices, key=lambda s: s.SliceLocation)

img_shape = list(slices[0].pixel_array.shape)
img_shape.append(len(slices))


def img3d_with_rotation(angle, depth):
    imgFinal = []
    for i, s in enumerate(slices):
        img2d = s.pixel_array
        rows, cols = img2d.shape

        M = cv2.getRotationMatrix2D((depth, ROTATION_X), angle, 1)
        rotated_img = cv2.warpAffine(img2d, M, (cols, rows))

        imgFinal.append(rotated_img[depth])

    # Convert imgFinal to a NumPy array
    print("imgFinal: {}".format(len(imgFinal)))
    return np.array(imgFinal)


def get_pixels_hu(image):
    image = image.astype(np.int16)
    image[image == -2000] = 0
    slopes = [slice_.RescaleSlope for slice_ in slices]
    intercepts = [slice_.RescaleIntercept for slice_ in slices]

    images = [slope * img.astype(np.float64) + np.int16(intercept)
              if slope != 1
              else img.astype(np.int16) + np.int16(intercept)
              for slope, intercept, img in zip(slopes, intercepts, image)]

    return np.array(images, dtype=np.int16)


def coronal_hu_depth(angle, depth):
    imgFinal = img3d_with_rotation(angle, depth)
    coronal = np.array(imgFinal)
    coronal_hu_ = get_pixels_hu(coronal)
    return coronal_hu_[::-1]


def update():
    angleV = sliders['angle']
    depthV = sliders['depth']
    minV = sliders['min']
    maxV = sliders['max']
    ROTATION_X = sliders['center']

    coronal_hu = coronal_hu_depth(angleV, depthV)
    coronal_hu_display = cv2.normalize(coronal_hu, None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8U)
    cv2.imshow('Deep Bridge', coronal_hu_display)


def key_events(key):
    if key == ord('q'):
        cv2.destroyAllWindows()
        sys.exit(0)
    elif key in {ord('+'), ord('=')}:
        sliders['depth'] += 1
    elif key == ord('-'):
        sliders['depth'] -= 1
    elif key == ord('w'):
        sliders['angle'] += 1
    elif key == ord('s'):
        sliders['angle'] -= 1
    elif key == ord('d'):
        sliders['center'] += 1
    elif key == ord('a'):
        sliders['center'] -= 1
    update()


if __name__ == '__main__':
    sliders = {
        'center': ROTATION_X,
        'min': 0,
        'max': 1000,
        'angle': 73,
        'depth': img_shape[0] // 2,
    }

    update()
    cv2.namedWindow('Deep Bridge', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('Deep Bridge', 650, 800)
    cv2.setMouseCallback('Deep Bridge', key_events)

    while True:
        k = cv2.waitKey(0)
        key_events(k)
