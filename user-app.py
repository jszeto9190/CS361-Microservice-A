import requests
import json
import os

#Please note: Only modify text, save_directory, and num_images under __main__.

def generate_images(text, save_directory, num_images=10):
    # Define the API endpoint for generating images
    api_url = 'https://microservice-a-cs361-c3c3bdb288e7.herokuapp.com/generate-image'
    
    # Prepare the payload for the POST request
    payload = {
        "text": text,
        "save_directory": save_directory,
        "num_images": num_images
    }

    headers = {
        "Content-Type": "application/json"
    }
    
    try:
        # Send POST request to the API
        response = requests.post(api_url, data=json.dumps(payload), headers=headers)
        
        # Check if the request was successful
        if response.status_code == 200:
            response_data = response.json() #URL DATA AND FILE LOCATION DATA STORED HERE
            print("Successfully generated images:")  
            print(json.dumps(response_data, indent=2))
            return response_data
        else:
            print("Failed to generate images. Status code:", response.status_code)
            print("Response:", response.text)
            return None
    except requests.exceptions.RequestException as e:
        print("Error during the API request:", e)
        return None

def download_image(filename, save_directory):
    # Ensure the save directory exists
    if not os.path.exists(save_directory):
        os.makedirs(save_directory)

    # Create the download URL    
    download_url = f'https://microservice-a-cs361-c3c3bdb288e7.herokuapp.com/download/{filename}'
    
    try:
        # Attempt to download the image
        response = requests.get(download_url)
        
        # Check if the download was successful
        if response.status_code == 200:
            file_path = os.path.join(save_directory, filename)
            with open(file_path, 'wb') as f:
                f.write(response.content)
            print(f"Image saved as {file_path}")
        else:
            print(f"Failed to download image. Status code: {response.status_code}")
            print("Response:", response.text)
    except requests.exceptions.RequestException as e:
        print("Error during the image download:", e)

if __name__ == "__main__":
    # Sample input for generating images
    text = "oregon state university" # MODIFY THIS SEARCH TERM
    save_directory = "Pictures" # MODIFY THIS FOLDER NAME
    num_images = 2 # MODIFY THIS IMAGE AMOUNT (MAX 10 IMAGES)

    # Ensure the save directory exists
    if not os.path.exists(save_directory):
        os.makedirs(save_directory)

    # Generate images and handle the response
    images = generate_images(text, save_directory, num_images)
    if images and 'saved_images' in images:
        for image_path in images['saved_images']:
            filename = os.path.basename(image_path) 
            download_image(filename, save_directory)
    else:
        print("No images were generated.")
