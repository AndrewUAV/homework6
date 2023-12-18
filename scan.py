from pathlib import Path
import sys

image_files = []
video_files = []
document_files = []
music_files = []
archives_files = []
folders = []
other = []
unknown = set()
extensions = set()

image_extensions = ['JPEG', 'PNG', 'JPG', 'SVG']
video_extensions = ['AVI', 'MP4', 'MOV', 'MKV']
music_extensions = ['MP3', 'OGG', 'WAV', 'AMR']
document_extensions = ['DOC', 'DOCX', 'TXT', 'PDF', 'XLSX', 'PPTX']
archive_extensions = ['ZIP', 'GZ', 'TAR']

list_of_all_extensions = (
    image_extensions + video_extensions +
    music_extensions + document_extensions +
    archive_extensions
)

registered_extensions = {
    tuple(image_extensions): image_files,
    tuple(video_extensions): video_files,
    tuple(music_extensions): music_files,
    tuple(document_extensions): document_files,
    tuple(archive_extensions): archives_files
}

def get_extensions(file_name):
    return Path(file_name).suffix[1:].upper()

def scan(folder):
    for item in folder.iterdir():
        if item.is_dir():
            if item.name not in list_of_all_extensions:
                folders.append(item)
                scan(item)
            continue

        extension = get_extensions(file_name=item.name)
        new_name = folder / item.name

        if not extension:
            other.append(new_name)
        else:
            matched = False
            for ext_tuple, container in registered_extensions.items():
                if extension in ext_tuple:
                    extensions.add(extension)
                    container.append(new_name)
                    matched = True
                    break

            if not matched:
                unknown.add(extension)
                other.append(new_name)


if __name__ == '__main__':
    if len(sys.argv) != 2:
        sys.exit(1)

    path = sys.argv[1]
    print(f'Start in {path}')
    folder = Path(path)
    scan(folder)

    print(f'image: {image_files}')
    print(f'video: {video_files}')
    print(f'document: {document_files}')
    print(f'music: {music_files}')
    print(f'archive: {archives_files}')
    print(f"other: {other}")
    print(f"unknown extensions: {unknown}")
    print(f"unique extensions: {extensions}")
