# Duplicated Image Cleaner

Duplicated Image Cleaner is a Python script that helps you find and delete duplicate or similar images in a given directory. It uses perceptual hashing and image comparison techniques to identify duplicate or similar images based on their content.

**Disclaimer: Use this script with caution as it can lead to the deletion of images. Make sure to back up your images or test it on a separate copy of your image directory before using it on your original images. The script does not provide any recovery option for deleted images.**

## Features

- Delete exact duplicate images in a directory
- Delete similar images based on perceptual hashing and threshold comparison

## Prerequisites

- Python 3.7 or higher
- Required Python packages (install them using `pip install -r requirements.txt`):
  - Pillow
  - imagehash

## Installation

1. Clone the repository to your local machine:

<pre>
git clone https://github.com/your-username/duplicated-image-cleaner.git
</pre>

2. Navigate to the project directory:

<pre>
cd duplicated-image-cleaner
</pre>

3. Install the required Python packages:

<pre>
pip install -r requirements.txt
</pre>

## Usage

### Delete Exact Duplicate Images

To delete exact duplicate images in a directory, use the following command:

<pre>
python duplicated_image_cleaner.py /path/to/directory
</pre>

Replace `/path/to/directory` with the path to the directory containing your images. The script will compare the images and delete the duplicates, keeping only one copy of each image.

### Delete Similar Images

To delete similar images in a directory, use the following command:

<pre>
python duplicated_image_cleaner.py --include_similar /path/to/directory
</pre>

Replace `/path/to/directory` with the path to the directory containing your images. The script will compare the images and delete the similar ones based on a threshold comparison. By default, the threshold is set to 5. You can modify the threshold by using the `--threshold` option followed by the desired value.

### Dry Run (Show Images to Delete Without Deleting)

To perform a dry run and see which images would be deleted without actually deleting them, use the `--dry_run` option along with the above commands. This will provide you with a list of images that would be deleted if you run the script without the `--dry_run` option.

**Note: Exercise caution when using the script, especially when deleting images. Always double-check the command and make sure you have a backup of your images before running the script.**

## License

This project is licensed under the [MIT License](LICENSE).
