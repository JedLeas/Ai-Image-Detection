import os
from PIL import Image


def delete_small_images(input_folder, min_size=600, dry_run=True):
    """
    Scans a folder and deletes images smaller than min_size x min_size.
    """
    deleted_count = 0
    kept_count = 0
    errors = 0

    supported_extensions = ('.png', '.jpg', '.jpeg', '.bmp', '.tif', '.tiff')

    # Check if folder exists
    if not os.path.exists(input_folder):
        print(f"Skipping: Directory '{input_folder}' not found.")
        return

    print(f"\n--- Processing: {input_folder} ---")

    try:
        files = [f for f in os.listdir(input_folder) if f.lower().endswith(supported_extensions)]
    except Exception as e:
        print(f"Error accessing folder: {e}")
        return

    if not files:
        print("No images found.")
        return

    for filename in files:
        filepath = os.path.join(input_folder, filename)

        try:
            with Image.open(filepath) as img:
                width, height = img.size

            # Check dimensions (Delete if EITHER dimension is too small)
            if width < min_size or height < min_size:
                if dry_run:
                    print(f"[DRY RUN] Would delete: {filename} ({width}x{height})")
                else:
                    os.remove(filepath)
                    # print(f"[DELETED] {filename} ({width}x{height})") # Uncomment to see every deletion
                deleted_count += 1
            else:
                kept_count += 1

        except Exception as e:
            print(f"[ERROR] Could not process {filename}: {e}")
            errors += 1

    # Folder Summary
    print(f"  > Kept: {kept_count} | Deleted: {deleted_count} | Errors: {errors}")


if __name__ == "__main__":
    # List of all folders to process
    folders_to_check = [
        "../images/Original Photos/REALIMAGES",
        "../images/Original Photos/Adobe Firefly",
        "../images/Original Photos/GPT4o",
        "../images/Original Photos/Leonardo AI",
        "../images/Original Photos/Midjourney",
        "../images/Original Photos/Ideogram",
        "../images/Original Photos/Nano Banana"
    ]

    # Settings
    minimum_resolution = 600

    # !!! CHANGE THIS TO False TO PERMANENTLY DELETE FILES !!!
    enable_dry_run = False

    print(f"Starting Cleanup Process (Min Size: {minimum_resolution}x{minimum_resolution})")
    if enable_dry_run:
        print("MODE: DRY RUN (No files will be deleted)\n")
    else:
        print("MODE: LIVE (Files WILL be deleted)\n")

    for folder in folders_to_check:
        delete_small_images(folder, minimum_resolution, enable_dry_run)

    print("\nAll folders processed.")