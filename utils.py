import os

IMAGE_EXTENSIONS = (".jpg", ".jpeg", ".png", ".bmp", ".gif", ".tiff", ".tif", ".pgm")


def get_image_files(folder_path):
    image_files = []
    name_files = []
    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.lower().endswith(IMAGE_EXTENSIONS):
                image_files.append(os.path.join(root, file))
                name_files.append(file)
    return name_files, image_files
