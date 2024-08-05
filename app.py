import os
from flask import Flask, request, jsonify
from googleapiclient.discovery import build
from dotenv import load_dotenv
import requests

load_dotenv()

app = Flask(__name__)

api_key = os.getenv('API_KEY')
search_engine_id = os.getenv('SEARCH_ENGINE_ID')

def google_search(search_term):
    service = build("customsearch", "v1", developerKey=api_key)
    res = service.cse().list(q=search_term, cx=search_engine_id, searchType='image').execute()
    return res['items']

def download_and_save_image(image_url, save_directory):
    if not os.path.exists(save_directory):
        os.makedirs(save_directory)
    response = requests.get(image_url)
    if response.status_code == 200:
        image_name = os.path.join(save_directory, image_url.split("/")[-1])
        with open(image_name, 'wb') as f:
            f.write(response.content)
        return image_name
    return None

@app.route('/')
def home():
    return jsonify(message="This is Image Generation API. Use /generate-image to generate images.")

@app.route('/generate-image', methods=['POST'])
def generate_image():
    data = request.json
    text = data.get('text', '')
    save_directory = data.get('save_directory', 'downloaded_images')

    search_results = google_search(text)
    image_urls = [item['link'] for item in search_results if 'link' in item]

    saved_images = [download_and_save_image(url, save_directory) for url in image_urls]

    return jsonify(saved_images)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
