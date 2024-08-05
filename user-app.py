import requests
import json
import os

def generate_images(text, save_directory):
    api_url = 'https://microservice-a-cs361-c3c3bdb288e7.herokuapp.com/generate-image'
    
    payload = {
        "text": text,
        "save_directory": save_directory
    }
    headers = {
        "Content-Type": "application/json"
    }
    
    response = requests.post(api_url, data=json.dumps(payload), headers=headers)
    
    if response.status_code == 200:
        response_data = response.json()
        print("Response data:", json.dumps(response_data, indent=2))
        return response_data
    else:
        print("Failed to generate images. Status code:", response.status_code)
        print("Response:", response.text)
        return None

def download_image(filename, save_directory):
    if not os.path.exists(save_directory):
        os.makedirs(save_directory)
        
    download_url = f'https://microservice-a-cs361-c3c3bdb288e7.herokuapp.com/download/{filename}'
    response = requests.get(download_url)
    
    if response.status_code == 200:
        file_path = os.path.join(save_directory, filename)
        with open(file_path, 'wb') as f:
            f.write(response.content)
        print(f"Image saved as {file_path}")
    else:
        print(f"Failed to download image. Status code: {response.status_code}")
        print("Response:", response.text)

# Example usage
if __name__ == "__main__":
    text = "car"
    save_directory = "Pictures"  # Ensure this directory exists locally
    if not os.path.exists(save_directory):
        os.makedirs(save_directory)
    images = generate_images(text, save_directory)
    if images and 'saved_images' in images:
        for image_path in images['saved_images']:
            filename = os.path.basename(image_path)  # Extract the filename from the path
            download_image(filename, save_directory)
    else:
        print("No images were generated.")
