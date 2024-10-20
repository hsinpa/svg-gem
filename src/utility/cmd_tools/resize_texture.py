import argparse
import os

from utility.image_utility import resize_canvas


def process_directory(new_file_name: str, target_directory: str, dest_directory: str, size: int):
    if not os.path.isdir(target_directory):
        return
    index = 0

    for file in os.listdir(target_directory):
        if file.endswith(".png"):
            base_name, _ = os.path.splitext(file)
            resize_canvas(
                old_image_path=os.path.join(target_directory, file),
                new_image_path=os.path.join(dest_directory, f'{new_file_name}-{index}.jpg'),
                canvas_width=size,
                canvas_height=size,
            )
        index += 1

parser = argparse.ArgumentParser(add_help=False)
parser.add_argument('-name', '-n', dest="name", type=str)
args = parser.parse_args()

target_directory = './assets/raw_images'
dest_directory = './assets/resize_images'
name = args.name
size = 512

process_directory(name, target_directory, dest_directory, size)