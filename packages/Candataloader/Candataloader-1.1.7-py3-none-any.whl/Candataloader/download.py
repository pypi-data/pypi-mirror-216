import os
import requests

dataset_mapping = {
        'Survival': 'https://3670-203-205-29-5.ngrok-free.app/Survival Analysis Dataset for automobile IDS.csv',
        'SynCAN': 'https://3670-203-205-29-5.ngrok-free.app/SynCAN.csv',
        'ROAD': 'https://3670-203-205-29-5.ngrok-free.app/ROAD.csv',
        'Car Hacking': 'https://3670-203-205-29-5.ngrok-free.app/Car Hacking.csv',
        'OTIDS': 'https://3670-203-205-29-5.ngrok-free.app/OTIDS.csv',
        'Automotive': 'https://3670-203-205-29-5.ngrok-free.app/autoCAN_Prototype.csv',
    }

def list_datasets():
    datasets = list(dataset_mapping.keys())
    print("Available datasets:")
    for dataset in datasets:
        print(dataset)
        
def get_dataset_path(dataset_name):
    if dataset_name not in dataset_mapping:
        print(f"Error: Dataset '{dataset_name}' is not available.")
        return

    filename = os.path.basename(dataset_mapping[dataset_name])
    if os.path.exists(filename):
        return os.path.abspath(filename)
    else:
        print(f"Error: Dataset '{dataset_name}' has not been downloaded.")
        return None
    
def download_dataset(dataset_name):
    if dataset_name not in dataset_mapping:
        print(f"Dataset '{dataset_name}' is not available for download.")
        return

    url = dataset_mapping[dataset_name]
    filename = url.split('/')[-1]  # Extract the filename from the URL
    current_dir = os.getcwd()  # Get the current directory path

    file_path = os.path.join(current_dir, filename)

    try:
        response = requests.get(url)
        response.raise_for_status()

        with open(file_path, 'wb') as file:
            file.write(response.content)

        print(f"Dataset '{dataset_name}' downloaded successfully to '{file_path}'.")
    except requests.exceptions.HTTPError as err:
        print(f"Error downloading dataset '{dataset_name}': {err}")
    except Exception as err:
        print(f"An error occurred while downloading dataset '{dataset_name}': {err}")

