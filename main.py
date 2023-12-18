import os
import sys
import scan
import shutil
import normalize
from pathlib import Path


def handle_file(path, root_folder, dist):
    target_folder = root_folder / dist
    target_folder.mkdir(exist_ok=True)

    new_name = normalize.normalize(path.name)

    path.rename(target_folder / new_name)

def handle_archive(path, root_folder, dist):
    target_folder = root_folder / dist
    target_folder.mkdir(exist_ok=True)

    try:
        shutil.unpack_archive(str(path.resolve()), str(target_folder.resolve()))
        for file_path in target_folder.iterdir():
            if file_path.is_file():
                new_name = normalize.normalize(file_path.name.replace('.zip', '').replace('.tar', '').replace('.gz',''))
                new_path = target_folder / new_name
                file_path.rename(new_path)
        path.unlink()
    except (shutil.ReadError, FileNotFoundError):
        print(f"Failed to unpack or file not found: {path}")
def remove_empty_folders(path):

    for root, dirs, files in os.walk(path, topdown=False):
        for directory in dirs:
            current_folder = os.path.join(root, directory)
            if not os.listdir(current_folder):  # If the folder is empty
                os.rmdir(current_folder)
                #print(f"Removed empty folder: {current_folder}")

def main(folder_path):
    print(folder_path)
    scan.scan(folder_path)

    for file in scan.image_files:
        handle_file(file, folder_path, 'Image')

    for file in scan.video_files:
        handle_file(file, folder_path, 'Video')

    for file in scan.document_files:
        handle_file(file, folder_path, 'Document')

    for file in scan.music_files:
        handle_file(file, folder_path, 'Music')

    for file in scan.other:
        handle_file(file, folder_path, 'Other')

    for file in scan.archives_files:
        handle_archive(file, folder_path, 'Archive')


if __name__ == '__main__':
    if len(sys.argv) != 2:
        sys.exit(1)
    path = sys.argv[1]
    #print(f'Start in {path}')
    folder = Path(path)
    main(folder.resolve())

    # Remove empty folders after organizing files
    remove_empty_folders(folder.resolve())