import os

from download_datasets import run as download_datasets

# install requirements
print("Running pip install for required packages...")
result = os.system('pip install -r requirements.txt')
if(result != 0):
    print("Could not install required packages. Please check your internet connection and permissions.")
    exit(1)



download_datasets()


