import os
import re
import logging
from io import StringIO
from flask import Flask, request, jsonify, render_template, send_from_directory
from googleapiclient.discovery import build
from dotenv import load_dotenv
import requests

load_dotenv()

app = Flask(__name__)

# Hide API keys and search engine ID
api_key = os.getenv('API_KEY')
search_engine_id = os.getenv('SEARCH_ENGINE_ID')

# Initialize log
log_stream = StringIO()
handler = logging.StreamHandler(log_stream)
handler.setLevel(logging.INFO)
app.logger.addHandler(handler)
app.logger.setLevel(logging.INFO)

# Initialize search function
def search(search_term, num_images=10):
    custom_search = build("customsearch", "v1", developerKey=api_key)
    res = custom_search.cse().list(q=search_term, cx=search_engine_id, searchType='image', num=num_images).execute()
    return res['items']

# Sanitize filenames to avoid premature parsing
def sanitize_filename(filename):
    # Replace percent-encoded characters with an underscore
    filename = re.sub(r'%[0-9A-Fa-f]{2}', '_', filename)
    # Replace other problematic characters with an underscore
    filename = re.sub(r'[:"/\\|<>?*]', '_', filename)
    return filename

# Ensure the correct file extension
def check_extension(filename, content_type):
    ext = os.path.splitext(filename)[1]
    if not ext:
        if 'image/jpeg' in content_type:
            filename += '.jpg'
        elif 'image/png' in content_type:
            filename += '.png'
        elif 'image/webp' in content_type:
            filename += '.webp'
        elif 'image/gif' in content_type:
            filename += '.gif'
    return filename

def download_and_save_image(image_url, save_directory, timeout=5):
    # Ensure the save directory exists
    if not os.path.exists(save_directory):
        os.makedirs(save_directory)
        
    try:
        # Attempt to download the image
        response = requests.get(image_url, timeout=timeout)
        if response.status_code == 200:
            content_type = response.headers['Content-Type']
            sanitized_filename = sanitize_filename(image_url.split("/")[-1].split('?')[0])
            sanitized_filename = check_extension(sanitized_filename, content_type)
            image_name = os.path.join(save_directory, sanitized_filename)
            app.logger.info(f"The image has been saved to the following location: {image_name}")
            with open(image_name, 'wb') as f:
                f.write(response.content)
            return image_name
    except requests.exceptions.Timeout:
        app.logger.info(f"Image download has timed out: {image_url}")
    except Exception as e:
        app.logger.info(f"An error occurred while attempting to download the image: {image_url}, Error: {e}")
    return None

@app.route('/')
def home():
    return render_template('index.html')

# Generate images and save them to a directory
@app.route('/generate-image', methods=['POST'])
def generate_image():
    data = request.json
    text = data.get('text', '')
    save_directory = '/tmp/Pictures'
    num_images = int(data.get('num_images', 10))

    if not os.path.exists(save_directory):
        os.makedirs(save_directory)

    search_results = search(text, num_images)
    image_urls = [item['link'] for item in search_results if 'link' in item]

    saved_images = [download_and_save_image(url, save_directory) for url in image_urls]

    # Prepare the response
    response_data = {
        "saved_images": [img for img in saved_images if img is not None],
        "image_urls": image_urls
    }

    return jsonify(response_data)

# Log the actions
@app.route('/logs')
def get_logs():
    log_stream.seek(0)
    log_contents = log_stream.read()
    return render_template('logs.html', logs=log_contents)

#clear logs
@app.route('/clear-logs', methods=['POST'])
def clear_logs():
    log_stream.truncate(0)
    log_stream.seek(0)
    return redirect(url_for('get_logs'))

#save photos
@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory('/Pictures', filename)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
