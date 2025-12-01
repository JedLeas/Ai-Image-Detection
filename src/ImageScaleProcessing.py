import os
from skimage import io, util

def crop_image(filepath, output_path):
    try:
        image = io.imread(filepath)
    except FileNotFoundError:
        print(f"Error: Input file not found at {filepath}")
        return


    h, w = image.shape[:2]
    target_size = 600


    if h < target_size or w < target_size:
        print(f"Skipping: Image too small ({w}x{h}) - {filepath}")
        return


    start_y = (h - target_size) // 2
    start_x = (w - target_size) // 2


    img_cropped = image[start_y : start_y + target_size, start_x : start_x + target_size]


    processed_uint8 = util.img_as_ubyte(img_cropped)
    io.imsave(output_path, processed_uint8)
    print(f"Processed: {output_path}")

def process_all_images(inputfile, outputfile, start_num):
    input_dir = f"../images/Original Photos/{inputfile}"
    output_dir = f"../images/ScaledPictures/{outputfile}"

    os.makedirs(output_dir, exist_ok=True)

    supported_extensions = ('.png', '.jpg', '.jpeg', '.bmp', '.tif', '.tiff')

    try:
        all_files = os.listdir(input_dir)
    except FileNotFoundError:
        print(f"Error: Directory not found {input_dir}")
        return

    image_files = [f for f in all_files if f.lower().endswith(supported_extensions)]

    for i, filename in enumerate(image_files):
        input_path = os.path.join(input_dir, filename)
        output_filename = f"{i + start_num}.png"
        output_path = os.path.join(output_dir, output_filename)
        crop_image(input_path, output_path)

if __name__ == "__main__":

    #process_all_images("Adobe Firefly", "GenAI", 1)
    #process_all_images("GPT4o", "GenAI", 100)
    #process_all_images("Ideogram", "GenAI", 1000)
    #process_all_images("Leonardo AI", "GenAI", 10000)
    #process_all_images("Midjourney", "GenAI", 100000)
    #process_all_images("Nano Banana", "GenAI", 1000000)

    process_all_images("REALIMAGES", "Real", 1)