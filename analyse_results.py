import os
import logging


# counts the number of subdirectories in a given directory.
def count_subdirectories(path):
    try:
        return len([name for name in os.listdir(path) if os.path.isdir(os.path.join(path, name))])
    except FileNotFoundError:
        logging.error('Directory {} does not exist'.format(path))
        return 0


# counts the number of files in a given directory and all its subdirectories.
def count_files(path):
    try:
        return sum([len(files) for r, d, files in os.walk(path)])
    except FileNotFoundError:
        logging.error('Directory {} does not exist'.format(path))
        return 0


# counts the number of all subdirectories and their directories in a given directory.
def count_all_subdirectories(path):
    try:
        return sum([len(d) for r, d, files in os.walk(path)])
    except FileNotFoundError:
        logging.error('Directory {} does not exist'.format(path))
        return 0


def count_subdirectories_(path, result=None):
    try:
        if result is None:
            result = {}

        if os.path.isdir(path):
            subdirs = []
            files = []

            for entry in os.scandir(path):
                if entry.is_file():
                    files.append(entry.name)
                elif entry.is_dir():
                    subdirs.append(entry.path)

            if not files:
                result[os.path.basename(path)] = len(subdirs)
                for subdir in subdirs:
                    count_subdirectories_(subdir, result)

        return result
    except FileNotFoundError:
        logging.error('Directory {} does not exist'.format(path))
        return 0


def count_dcm_files(path, result=None):
    try:
        if result is None:
            result = {}

        if os.path.isdir(path):
            subdirs = []
            dcm_files = 0

            for entry in os.scandir(path):
                if entry.is_file() and entry.name.endswith('.dcm'):
                    dcm_files += 1
                elif entry.is_dir():
                    subdirs.append(entry.path)

            if dcm_files > 0:
                result[os.path.basename(path)] = dcm_files

            for subdir in subdirs:
                count_dcm_files(subdir, result)

        return result
    except FileNotFoundError:
        logging.error('Directory {} does not exist'.format(path))
        return 0


if __name__ == '__main__':
    initial_directory_path = "/Volumes/exFAT_Adams/deepbridge/data"
    directory_path_after_sorting = "/Volumes/exFAT_Adams/deepbridge_result"

    number_of_patients_directory_before_sorting = count_subdirectories(initial_directory_path)
    number_of_patients_directory_after_sorting = count_subdirectories(directory_path_after_sorting)

    print(f"Nombre de dossier patients : {count_subdirectories(initial_directory_path)}")
    print(f"Nombre de dossier patients après tri : {count_subdirectories(directory_path_after_sorting)}")

    initial_number_of_files = count_files(initial_directory_path)
    number_of_files_after_sorting = count_files(directory_path_after_sorting)
    number_of_unusable_files = initial_number_of_files - number_of_files_after_sorting

    print(f"Nombre de fichiers avant tri : {initial_number_of_files}")
    print(f"Nombre de fichiers après tri : {number_of_files_after_sorting}")
    print(f"Nombre de fichiers non utilisables : {number_of_unusable_files}")

    number_total_subdirectories = count_all_subdirectories(initial_directory_path)
    number_of_scan_before_sorting = number_total_subdirectories - number_of_patients_directory_before_sorting
    print(f"Nombre de scans avant tri: {number_of_scan_before_sorting}")

    number_total_subdirectories_after_sorting = count_all_subdirectories(directory_path_after_sorting)
    number_of_scan_after_sorting = number_total_subdirectories_after_sorting - number_of_patients_directory_after_sorting
    print(f"Nombre de scans après tri: {number_of_scan_after_sorting}")

    number_of_scan_by_patient = count_subdirectories_(directory_path_after_sorting)
    print(f"Nombre de scans par patient: {number_of_scan_by_patient}")

    number_of_dcm_by_scan = count_dcm_files(directory_path_after_sorting)
    print(f"Nombre de fichiers dcm par scan: {number_of_dcm_by_scan}")
