"""
    this file generate files like:
    image - JPEG,PNG,JPG,SVG
    video files - AVI,MP4,MOV,MKV
    documents - DOC,DOCX,TXT,PDF,XLSX,PPTX
    music - MP3,OGG,WAV,AMR
    archives - ZIP,GZ,TAR
    unknown ......
"""
import cv2
import numpy
import numpy as np
import shutil
import random
from PIL import Image
from pathlib import Path
from pydub import AudioSegment
from random import randint, choice, choices

MESSAGE = 'Hi my friend'


def get_random_filename():
    """
    function for generate a randon filename
    """
    random_value = '()+,-0123456789;=@ABCDEFGHIJKLMNOPQRSTUVWXYZ[]^_`abcdefghijklmnopqrstuvwxyz' \
                   '{}~абвгдеєжзиіїйклмнопрстуфхцчшщьюяАБВГДЕЄЖЗИІЇЙКЛМНОПРСТУФХЦЧШЩЬЮЯ'
    return ''.join(choices(random_value, k=8))


def generate_images_files(path):
    # image - JPEG,PNG,JPG,SVG
    images = ('JPEG', 'PNG', 'JPG', 'SVG')
    image_array = numpy.random.rand(100, 100, 3) * 255
    image = Image.fromarray(image_array.astype('uint8'))
    image.save(f"{path}/{get_random_filename()}.{choice(images).lower()}")


def generate_video_files(path):
    # video files - AVI,MP4,MOV,MKV
    videos = ('AVI', 'MP4', 'MOV', 'MKV')
    selected_format = random.choice(videos)

    file_path = path / f"{get_random_filename()}.{selected_format.lower()}"
    # Set the video properties
    width, height = 640, 480
    fps = 30
    seconds = 10
    fourcc = cv2.VideoWriter_fourcc(*'XVID')  # Default codec (you can change it based on the selected format)

    # Create a VideoWriter object
    video_writer = cv2.VideoWriter(str(file_path), fourcc, fps, (width, height))

    # Generate frames and write them to the video file
    for frame_number in range(fps * seconds):
        # Create a simple gradient image for each frame
        frame = np.zeros((height, width, 3), dtype=np.uint8)
        frame[:, :, 0] = frame_number % 256  # Blue channel
        frame[:, :, 1] = (frame_number // 2) % 256  # Green channel
        frame[:, :, 2] = 255  # Red channel

        # Write the frame to the video file
        video_writer.write(frame)

    # Release the VideoWriter object
    video_writer.release()


def generate_documents_files(path):
    # documents - DOC,DOCX,TXT,PDF,XLSX,PPTX
    documents = ('DOC', 'DOCX', 'TXT', 'PDF', 'XLSX', 'PPTX')
    with open(path / f"{get_random_filename()}.{choice(documents).lower()}", "wb") as f:
        f.write(MESSAGE.encode())

def generate_music_files(path):
    # music - MP3,OGG,WAV,AMR
    music = ('mp3','ogg','wav','amr')
    audio = AudioSegment.silent(duration=1000)
    selected_extension = random.choice(music)
    file_path = path / f'{get_random_filename()}.{selected_extension}'
    audio.export(file_path,format=selected_extension)

def generate_archive_files(path):
    archive = ('ZIP', 'GZ', 'TAR')
    shutil.make_archive(f"{path}/{get_random_filename()}", f'{choice(archive).lower()}', path)

def generate_folders(path):
    folder_name = ['temp', 'folder', 'dir', 'tmp', 'OMG', 'is_it_true', 'no_way', 'find_it']
    folder_path = Path(
        f"{path}/" + '/'.join(choices(folder_name, weights=[10, 10, 1, 1, 1, 1, 1, 1], k=randint(5, len(folder_name)))))
    folder_path.mkdir(parents=True, exist_ok=True)


def generate_folder_forest(path):
    for i in range(0, randint(2, 5)):
        generate_folders(path)

def generate_random_files(path):
    for i in range(3, randint(5, 7)):
        function_list = [generate_images_files,generate_video_files,
                         generate_documents_files, generate_music_files,
                         generate_archive_files]
        choice(function_list)(path)


def parse_folder_recursion(path):
    for elements in path.iterdir():
        if elements.is_dir():
            generate_random_files(path)
            parse_folder_recursion(elements)


def exist_parent_folder(path):
    path.mkdir(parents=True, exist_ok=True)


def file_generator(path):
    exist_parent_folder(path)
    generate_folder_forest(path)
    parse_folder_recursion(path)


if __name__ == '__main__':
    parent_folder_path = Path("Temp")
    file_generator(parent_folder_path)