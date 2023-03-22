import os
import sys
import pydicom
import logging
import shutil
from collections import defaultdict

patient_series_to_folder = defaultdict(lambda: defaultdict(str))


def create_directory(path):
    if not os.path.exists(path):
        os.makedirs(path)


def move_file(source, destination):
    if os.path.exists(destination) and os.path.getsize(source) == os.path.getsize(destination):
        os.remove(source)
    else:
        shutil.move(source, destination)


def read_dicom_metadata(filename, output_folder):
    try:
        ds = pydicom.dcmread(filename, stop_before_pixels=True)
        if ds.Modality != 'CT':
            logging.warning('File {} is not a CT scan'.format(filename))
        else:
            patient_id = ds.PatientID
            series_uid = ds.SeriesInstanceUID
            series_folder = os.path.join(output_folder, patient_id, series_uid)
            if series_uid not in patient_series_to_folder[patient_id]:
                logging.info('Found new patient: {}'.format(patient_id))
                logging.info('Found new series: {}'.format(series_uid))
                patient_series_to_folder[patient_id][series_uid] = series_folder
                create_directory(series_folder)
            move_file(filename, os.path.join(series_folder, os.path.basename(filename)))
    except pydicom.errors.InvalidDicomError as e:
        invalid_dicom_folder = os.path.join(output_folder, 'invalid_dicom_files')
        create_directory(invalid_dicom_folder)
        move_file(filename, os.path.join(invalid_dicom_folder, os.path.basename(filename)))
    except FileNotFoundError:
        pass


def load_scan(path, output_folder):
    print('glob: {}'.format(path))
    for root, dirs, filenames in os.walk(path):
        for filename in filenames:
            if filename.endswith('.dcm'):
                filepath = os.path.join(root, filename)
                read_dicom_metadata(filepath, output_folder)
            else:
                if filename.endswith('.cab'):
                    os.remove(os.path.join(root, filename))
                else:
                    logging.warning('File {} is not a dicom file'.format(filename))
    logging.info('Finished reading dicom files')


def main(source_folder, output_folder):
    create_directory(output_folder)
    load_scan(source_folder, output_folder)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python organize_dicom_files.py <source_folder> <output_folder>")
        sys.exit(1)
    main(sys.argv[1], sys.argv[2])
