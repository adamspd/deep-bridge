import os
import sys
import pydicom
import logging
import shutil

patient_id_to_folder = {}


def create_directory(path):
    if not os.path.exists(path):
        os.makedirs(path)


def move_file(source, destination):
    if os.path.exists(destination) and os.path.getsize(source) == os.path.getsize(destination):
        os.remove(source)
    else:
        shutil.move(source, destination)


def read_dicom_metadata(filename):
    try:
        ds = pydicom.dcmread(filename, stop_before_pixels=True)
        if ds.Modality != 'CT':
            logging.warning('File {} is not a CT scan'.format(filename))
        else:
            patient_id = ds.PatientID
            if patient_id not in patient_id_to_folder:
                logging.info('Found new patient: {}'.format(patient_id))
                patient_id_to_folder[patient_id] = os.path.join('data', patient_id)
                create_directory(patient_id_to_folder[patient_id])
            move_file(filename, os.path.join(patient_id_to_folder[patient_id], os.path.basename(filename)))
    except pydicom.errors.InvalidDicomError as e:
        invalid_dicom_folder = os.path.join('data', 'invalid_dicom_files')
        create_directory(invalid_dicom_folder)
        move_file(filename, os.path.join(invalid_dicom_folder, os.path.basename(filename)))


def load_scan(path):
    print('glob: {}'.format(path))
    for root, dirs, filenames in os.walk(path):
        for filename in filenames:
            if filename.endswith('.dcm'):
                filepath = os.path.join(root, filename)
                read_dicom_metadata(filepath)
            else:
                if filename.endswith('.cab'):
                    os.remove(os.path.join(root, filename))
                logging.warning('File {} is not a dicom file'.format(filename))
    logging.info('Finished reading dicom files')


def main(source_folder):
    create_directory('data')
    load_scan(source_folder)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python organize_dicom_files.py <source_folder>")
        sys.exit(1)
    main(sys.argv[1])
