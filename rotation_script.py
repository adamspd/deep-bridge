"""
Versions :
Python 3.11.0
pip 23.0

Pour installer les bibliothèques, utilisez la commande suivante :
- pip install -r requirements.txt
"""
import os

import pydicom
import numpy as np
import matplotlib.pyplot as plt
import scipy
from matplotlib import cm
from matplotlib.widgets import Slider, Button, RadioButtons
import sys
import glob
from scipy import ndimage
import math
import tkinter
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.backend_bases import key_press_handler


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
dossier = "/Volumes/exFAT_Adams/deepbridge_result/0350623919/2.16.840.1.113669.632.21.1401581570.2685747106.20459161902428661"

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
print(f"len(files): {len(files)}")
print(f"len(slices): {len(slices)}")
img_shape = list(slices[0].pixel_array.shape)
img_shape.append(len(slices))


def rotate_x(origin_x, origin_y, x, y, angle_d):
    angle = angle_d * np.pi / 180
    dy = y - origin_y
    dyy = origin_y - y

    if origin_y <= y:
        cos = np.cos(angle) * dy
        sin = np.sin(angle) * dy
    else:
        cos = np.cos(angle + np.pi) * dyy
        sin = np.sin(angle + np.pi) * dyy

    rotated_y = cos + origin_y
    rotated_x = sin + origin_x

    return rotated_y, rotated_x


def img3d_with_rotation(angle, depth):
    imgFinal = []
    for i, s in enumerate(slices):
        img2d = s.pixel_array
        rowArray = []
        img2d_len = len(img2d)
        for j in range(img2d_len):
            cos, sin = rotate_x(depth, ROTATION_X, depth, j, angle)

            sin_floor = np.floor(sin).astype(int)
            sin_ceil = np.ceil(sin).astype(int)
            cos_floor = np.floor(cos).astype(int)
            cos_ceil = np.ceil(cos).astype(int)

            image_size = img2d.shape[0]

            if sin_ceil >= image_size or cos_ceil >= image_size:
                rowArray.append(0)
            else:
                rowArray.append(img2d[sin_floor][cos_floor])
                if sin_floor != sin_ceil:
                    rowArray[-1] = (rowArray[-1] + img2d[sin_ceil][cos_floor]) / 2
                elif cos_floor != cos_ceil:
                    rowArray[-1] = (rowArray[-1] + img2d[sin_floor][cos_ceil]) / 2
        imgFinal.append(rowArray)

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


def update(val):
    global lines
    global ROTATION_X
    angleV = sliders['angle'].val
    depthV = sliders['depth'].val
    minV = sliders['min'].val
    maxV = sliders['max'].val
    ROTATION_X = sliders['center'].val
    lines.pop(0).remove()
    ax.imshow(coronal_hu_depth(angleV, depthV), cmap=cm.gray, vmin=minV, vmax=maxV)
    lines = ax.plot([ROTATION_X, ROTATION_X], [0, 570], "c")


def on_key_press(event):
    print("you pressed {}".format(event.key))
    key_press_handler(event, canvas, toolbar)


if __name__ == '__main__':

    root = tkinter.Toplevel()
    root.title('Deep Bridge')

    # Configure plot
    fig, ax = plt.subplots()
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)
    plt.subplots_adjust(left=0.1, right=0.9, top=0.7, bottom=0.1)

    # Initialize plot with an image with an angle of 73 and depth of img_shape[0] / 2
    coronal_hu = coronal_hu_depth(73, img_shape[0] // 2)
    lines = ax.plot([ROTATION_X, ROTATION_X], [0, 570], "c")
    ax.imshow(coronal_hu, cmap=cm.gray, vmin=0, vmax=1000)

    # Add sliders to modify the center, minimum and maximum density, angle and depth
    slider_ax_specs = {
        'center': [0, 512, ROTATION_X, 1, 0.75],
        'min': [-1000, 1000, 0, 10, 0.8],
        'max': [-1000, 1000, 1000, 10, 0.85],
        'angle': [0, 360, 73, 1, 0.9],
        'depth': [150, 350, img_shape[0] // 2, 1, 0.95]
    }

    axes = {}
    sliders = {}

    for name, ax_spec in slider_ax_specs.items():
        slider_ax = plt.axes([0.25, ax_spec[4], 0.65, 0.03], facecolor='lightgoldenrodyellow')
        slider = Slider(slider_ax, name.capitalize(), ax_spec[0], ax_spec[1], valinit=ax_spec[2], valstep=ax_spec[3])
        axes[name] = slider_ax
        sliders[name] = slider
        slider.on_changed(update)

    toolbar = NavigationToolbar2Tk(canvas, root)
    toolbar.update()
    canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)

    canvas.mpl_connect("key_press_event", on_key_press)
    bottomframe = tkinter.Frame(root)
    bottomframe.pack(side=tkinter.BOTTOM)

    # Start main loop
    tkinter.mainloop()
