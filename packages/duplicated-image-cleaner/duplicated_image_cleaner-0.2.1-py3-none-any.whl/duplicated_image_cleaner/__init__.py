from PIL import Image
import os
import imagehash
import argparse

def calculate_hash(image_path):
    try:
        with Image.open(image_path) as img:
            return imagehash.average_hash(img)
    except (OSError, Image.UnidentifiedImageError):
        return None

def delete_duplicates(directory, include_similar=False, threshold=5, dry_run=False):
    # Get a list of all image files in the directory
    image_files = [file for file in os.listdir(directory) if is_image_file(file)]

    # Create a dictionary to store the hashes
    hashes = {}

    # Iterate over the image files and calculate the hash for each image
    for image_file in image_files:
        file_path = os.path.join(directory, image_file)
        file_hash = calculate_hash(file_path)
        if file_hash is not None:
            if file_hash in hashes:
                # Delete the duplicate if it matches exactly or if similarity check is enabled
                if not include_similar or file_hash - hashes[file_hash] <= threshold:
                    if not dry_run:
                        os.remove(file_path)
                        print(f"Match found: {image_file} exactly like {hashes[file_hash]} -- {image_file} deleted.")
                    else:
                        print(f"Match found: {image_file} exactly like {hashes[file_hash]} -- {image_file} will be deleted.")
            else:
                # Add the hash to the dictionary if it's not a duplicate
                hashes[file_hash] = image_file

def is_image_file(filename):
    image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp']
    return any(filename.lower().endswith(ext) for ext in image_extensions)

def delete_similar_images(directory, threshold=5, dry_run=False):
    # Get a list of all image files in the directory
    image_files = [file for file in os.listdir(directory) if is_image_file(file)]

    # Iterate over the image files and compare them with each other
    for i, reference_image in enumerate(image_files):
        reference_path = os.path.join(directory, reference_image)
        reference_hash = calculate_hash(reference_path)
        if reference_hash is not None:
            for j, duplicate_image in enumerate(image_files[i + 1:]):
                duplicate_path = os.path.join(directory, duplicate_image)
                duplicate_hash = calculate_hash(duplicate_path)
                if duplicate_hash is not None:
                    # Compare the perceptual hashes using a similarity metric
                    similarity = reference_hash - duplicate_hash
                    if similarity <= threshold:
                        # Delete the similar image
                        if not dry_run:
                            os.remove(duplicate_path)
                            print(f"Match found: {reference_image} is similar to {duplicate_image} -- {reference_image} deleted.")
                        else:
                            print(f"Match found: {reference_image} is similar to {duplicate_image} -- {reference_image} will be deleted.")

def main():
    parser = argparse.ArgumentParser(description='Delete duplicate or similar images.')
    parser.add_argument('directory', help='Path to the directory containing the images')
    parser.add_argument('--include_similar', action='store_true', help='Delete similar images')
    parser.add_argument('--threshold', type=int, default=5, help='Threshold for similarity comparison')
    parser.add_argument('--dry_run', action='store_true', help='Dry run mode (show images to delete without deleting them)')

    args = parser.parse_args()

    if args.include_similar:
        delete_similar_images(args.directory, threshold=args.threshold, dry_run=args.dry_run)
    else:
        delete_duplicates(args.directory, dry_run=args.dry_run)

if __name__ == '__main__':
    main()
