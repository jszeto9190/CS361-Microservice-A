import requests
import json

def generate_images(text, save_directory):
    api_url = 'http://localhost:5000/generate-image'
    
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

# Example usage
if __name__ == "__main__":
    text = "bball"
    save_directory = r"C:\Users\jason\Pictures"
    images = generate_images(text, save_directory)

