import requests
import json

def generate_images(text, save_directory='/tmp'):
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

def download_image(filename):
    download_url = f'https://microservice-a-cs361-c3c3bdb288e7.herokuapp.com/download/{filename}'
    response = requests.get(download_url)
    
    if response.status_code == 200:
        with open(filename, 'wb') as f:
            f.write(response.content)
        print(f"Image saved as {filename}")
    else:
        print(f"Failed to download image. Status code: {response.status_code}")
        print("Response:", response.text)

# Example usage
if __name__ == "__main__":
    text = "car"
    images = generate_images(text)
    if images and 'saved_images' in images:
        for image_path in images['saved_images']:
            filename = image_path.split('/')[-1]  # Extract the filename from the path
            download_image(filename)
    else:
        print("No images were generated.")
