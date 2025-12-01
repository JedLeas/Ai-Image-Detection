import os
import numpy as np
from skimage import io, util, color


def greyscale_image(filepath, output_path):
    try:
        image = io.imread(filepath)
    except FileNotFoundError:
        print(f"Error: {filepath}")
        return


    if image.ndim == 2:

        io.imsave(output_path, util.img_as_ubyte(image))
        return


    if image.shape[2] == 4:
        image = color.rgba2rgb(image)

    grey_image = color.rgb2gray(image)

    io.imsave(output_path, util.img_as_ubyte(grey_image))
    print(f"Greyscaled: {output_path}")


def process_all_images(inputfile, outputfile, start_num):
    input_dir = f"../images/ScaledPictures/{inputfile}"
    output_dir = f"../images/GreyScalledImages/{outputfile}"

    os.makedirs(output_dir, exist_ok=True)
    supported_extensions = ('.png', '.jpg', '.jpeg')

    try:
        all_files = os.listdir(input_dir)
    except FileNotFoundError:
        return

    image_files = [f for f in all_files if f.lower().endswith(supported_extensions)]

    for i, filename in enumerate(image_files):
        input_path = os.path.join(input_dir, filename)

        output_filename = f"{i + start_num}.png"
        output_path = os.path.join(output_dir, output_filename)
        greyscale_image(input_path, output_path)


if __name__ == "__main__":
    process_all_images("GenAI", "GenAI", 1)
    process_all_images("Real", "Real", 1)