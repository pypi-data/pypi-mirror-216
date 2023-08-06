from setuptools import setup

setup(
    name='duplicated_image_cleaner',
    version='0.2.1',
    description='Script to delete duplicate or similar images',
    author='Jorge Anzola',
    author_email='jorgeanzola@gmail.com',
    packages=['duplicated_image_cleaner'],
    install_requires=[
        'Pillow==8.3.2',
        'imagehash==4.2.1',
    ],
    entry_points={
        'console_scripts': [
            'delete_duplicates=duplicated_image_cleaner:main',
        ],
    },
)
