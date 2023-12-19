from pathlib import Path
import sys

images_files = list()
video_files = list()
documents_files = list()
audio_files = list()
archives_files = list()
folders = list()
other = list()
unknown = set()
extensions = set()

image_extensions = ['JPEG', 'PNG', 'JPG', 'SVG']
video_extensions = ['AVI', 'MP4', 'MOV', 'MKV']
audio_extensions = ['MP3', 'OGG', 'WAV', 'AMR']
documents_extensions = ['DOC', 'DOCX', 'TXT', 'PDF', 'XLSX', 'PPTX']
archives_extensions = ['ZIP', 'GZ', 'TAR']

list_of_all_extensions = (
    image_extensions + video_extensions +
    audio_extensions + documents_extensions +
    archives_extensions
)

registered_extensions = dict()
registered_extensions.update({i: 'images' for i in image_extensions})
registered_extensions.update({i: 'video' for i in video_extensions})
registered_extensions.update({i: 'audio' for i in audio_extensions})
registered_extensions.update({i: 'documents' for i in documents_extensions})
registered_extensions.update({i: 'archives' for i in archives_extensions})

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
        new_name = folder/item.name
        if not extension:
            other.append(new_name)
        else:
            try:
                container = registered_extensions[extension]
                extensions.add(extension)
                globals()[container + "_files"].append(new_name)
            except KeyError:
                unknown.add(extension)
                other.append(new_name)

if __name__ == '__main__':
    path = sys.argv[1]
    print(f"Start in {path}")

    folder = Path(path)

    scan(folder)

    print(f'images: {images_files}')
    print(f'video: {video_files}')
    print(f'documents: {documents_files}')
    print(f'audio: {audio_files}')
    print(f'archives: {archives_files}')
    print(f"other: {other}")
    print(f"unknowns extensions: {unknown}")
    print(f"unique extensions: {extensions}")
