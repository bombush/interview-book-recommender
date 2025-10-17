import os
import json

def run():
    # check for Kaggle API token
    if not os.path.exists('.kaggle') or not os.path.exists('.kaggle/kaggle.json'):
        try:
            os.path.mkdir('.kaggle', exist_ok=True, mode=0o755)
        except PermissionError as e:
            print("Could not create .kaggle directory due to permission error: {e}")
        except Exception as e:
            print(f"An error occurred while creating .kaggle directory: {e}")
            exit(1)

        print("Kaggle API token not found. Please create a Kaggle API token and put the kaggle.json file to the .kaggle folder.")
        exit(1)

    # read Kaggle token
    with open('.kaggle/kaggle.json', 'r') as f:
        kaggle_token_json = json.load(f)

    os.environ['KAGGLE_USERNAME'] = kaggle_token_json['username']
    os.environ['KAGGLE_KEY'] = kaggle_token_json['key']

    import kaggle as kg
    kg.api.authenticate()
    print("Downloading dataset files...")
    try:
        kg.api.dataset_download_files('arashnic/book-recommendation-dataset', path='Downloads', quiet=False, unzip=True)
    except ConnectionError as e:
        print("Connection error while downloading dataset. Please check your connection and retry later")
        exit(1)
    except Exception as e:
        print("Exception while downloading dataset: {e}")
        exit(1)

    
    # @TODO: download only files I am actually interested in
    # @TODO: friendlier exceptions