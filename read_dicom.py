import pydicom
import numpy as np
import cv2


def rotate_image(img, angle):
    # Get image height, width and center
    (h, w) = img.shape[:2]
    center = (w / 2, h / 2)

    # Rotate the image by the specified angle
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated_img = cv2.warpAffine(img, M, (w, h), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)

    return rotated_img


def load_dicom_image(dicom_filepath):
    ds = pydicom.dcmread(dicom_filepath)
    img = ds.pixel_array.astype(float)
    img -= np.min(img)
    img /= np.max(img)
    img *= 255
    img = img.astype(np.uint8)
    img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
    return img


if __name__ == '__main__':
    dicom_filepath = '/Users/adamspierredavid/developer/PycharmProjects/deep_bridge/deep-bridge-tpt/patients/dossier_1/1.2.840.113619.2.428.3.2831168016.82.1591422157.475.1.dcm'
    img = load_dicom_image(dicom_filepath)

    # Rotate the image 90 degrees
    angle = 90
    rotated_img = rotate_image(img, angle)
    print("ooookkk")
    # Display the rotated image
    cv2.imshow('Rotated Image', rotated_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
