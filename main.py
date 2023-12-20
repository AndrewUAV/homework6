
import sys
import scan
import shutil
import normalize
from pathlib import Path


def handle_file(path, root_folder, dist):
    target_folder = root_folder / dist
    target_folder.mkdir(exist_ok=True)
    path.replace(target_folder/normalize.normalize(path.name))

def handle_archive(path, root_folder, dist):
    target_folder = root_folder / dist
    target_folder.mkdir(exist_ok=True)
    new_name = normalize.normalize(path.name.replace(".zip", '').replace('.tar', '').replace('.gz', ''))
    archive_folder = target_folder / new_name
    archive_folder.mkdir(exist_ok=True)

    try:
        shutil.unpack_archive(str(path.resolve()), str(archive_folder.resolve()))
    except shutil.ReadError:
        archive_folder.rmdir()
        path.unlink()
        return
    except FileNotFoundError:
        archive_folder.rmdir()
        path.unlink()
        return
    path.unlink()


def remove_empty_folders(path):
    for item in path.iterdir():
        if item.is_dir():
            remove_empty_folders(item)
            try:
                item.rmdir()
            except OSError:
                pass

def main(folder_path):
    print(folder_path)
    scan.scan(folder_path)

    file_types = {
        'images': scan.images_files,
        'documents': scan.documents_files,
        'audio': scan.audio_files,
        'video': scan.video_files,
        'archives': scan.archives_files,
        'other': scan.other
    }

    for file_type, files in file_types.items():
        for file in files:
            if file_type == 'archives':  # Corrected this line
                handle_archive(file, folder_path, file_type)
            else:
                handle_file(file, folder_path, file_type)

    remove_empty_folders(folder_path)
    print("Contents of Organized Folders:")
    for item in folder_path.iterdir():
        if item.is_dir():
            print(f"Folder: {item}")
            for subitem in item.iterdir():
                print(f"  {subitem}")
        else:
            print(f"File: {item}")

if __name__ == '__main__':
    if len(sys.argv) != 2:
        sys.exit(1)
    path = sys.argv[1]
    print(f'Start in {path}')

    folder = Path(path)
    main(folder.resolve())

    print(f'images: {[normalize.normalize(file.name) for file in scan.images_files]}')
    print(f'video: {[normalize.normalize(file.name) for file in scan.video_files]}')
    print(f'documents: {[normalize.normalize(file.name) for file in scan.documents_files]}')
    print(f'audio: {[normalize.normalize(file.name) for file in scan.audio_files]}')
    print(f'archives: {[normalize.normalize(file.name) for file in scan.archives_files]}')
    print(f"other: {[normalize.normalize(file.name) for file in scan.other]}")
    print(f"unknowns extensions: {[normalize.normalize(ext) for ext in scan.unknown]}")
    print(f"unique extensions: {[normalize.normalize(ext) for ext in scan.extensions]}")