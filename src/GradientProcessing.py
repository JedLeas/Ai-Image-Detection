import os
import numpy as np
import scipy.ndimage
from skimage import io, util


def get_radial_profile(noise_image, bins=100):
    f = np.fft.fft2(noise_image)
    fshift = np.fft.fftshift(f)

    magnitude_spectrum = 20 * np.log(np.abs(fshift) + 1e-8)

    h, w = noise_image.shape
    center = (h // 2, w // 2)
    y, x = np.indices((h, w))
    r = np.sqrt((x - center[1]) ** 2 + (y - center[0]) ** 2)
    r = r.astype(int)

    hist, bin_edges = np.histogram(r, bins=bins, weights=magnitude_spectrum, density=True)

    return hist


def extract_fft_features(filepath):
    try:
        image = io.imread(filepath)
    except FileNotFoundError:
        print(f"Error: Not found {filepath}")
        return None

    # Convert to float and Grayscale
    img_float = util.img_as_float(image)
    if img_float.ndim == 3:
        img_float = np.mean(img_float, axis=2)

    # Denoise (Median Filter works best for structure)
    denoised_img = scipy.ndimage.median_filter(img_float, size=3)

    # Get Residual
    noise_residual = img_float - denoised_img

    # Extract Frequency Features (100 dimensions)
    features = get_radial_profile(noise_residual, bins=100)

    return features


def process_all_images(input_folder, output_folder):
    input_dir = f"../images/GreyScalledImages/{input_folder}"
    cov_dir = f"../images/CovarianceMatrices/{output_folder}"

    os.makedirs(cov_dir, exist_ok=True)

    supported = ('.png', '.jpg', '.jpeg')
    try:
        files = os.listdir(input_dir)
    except FileNotFoundError:
        print(f"Error: {input_dir} missing")
        return

    files = [f for f in files if f.lower().endswith(supported)]

    print(f"Processing {len(files)} images in {input_folder} (Frequency Analysis)...")

    for filename in files:
        input_path = os.path.join(input_dir, filename)

        features = extract_fft_features(input_path)

        if features is not None:
            base_name = os.path.splitext(filename)[0]
            save_path = os.path.join(cov_dir, f"{base_name}.npy")
            np.save(save_path, features)

    print(f"Done processing {input_folder}.")


if __name__ == "__main__":
    process_all_images("GenAI", "GenAI")
    process_all_images("Real", "Real")