import os

from download_datasets import run as download_datasets

def is_dataset_downloaded() -> bool:
    """Check if required datasets are already downloaded."""
    required_files = [
        'Downloads/Books.csv',
        'Downloads/Ratings.csv',
        'Downloads/Users.csv'
    ]
    for file in required_files:
        if not os.path.isfile(file):
            return False
    return True

# install requirements
print("Running pip install for required packages...")
result = os.system('pip install -r requirements.txt')
if(result != 0):
    print("Could not install required packages. Please check your internet connection and permissions.")
    exit(1)


if not is_dataset_downloaded():   
    download_datasets()


