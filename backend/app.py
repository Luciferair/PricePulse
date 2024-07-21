from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)
CORS(app)

def get_amazon_item_name(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
    }

    session = requests.Session()
    try:
        response = session.get(url, headers=headers)
        print(f"Response status code: {response.status_code}")
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            title_tag = soup.find('span', {'id': 'productTitle'})
            if title_tag:
                return title_tag.get_text(strip=True)
            else:
                print("Title tag not found")
                return None
        else:
            print(f"Request failed with status code: {response.status_code}")
            return None
    except requests.RequestException as e:
        print(f"Error fetching URL: {e}")
        return None

@app.route('/save_url', methods=['POST'])
def save_url_data():
    data = request.get_json()
    url = data.get('url')
    print(f"Received URL: {url}")

    if url == "HOME":
        print("Home URL not supported")
        return jsonify({"error": "Home URL is not supported"}), 400

    try:
        item_name = get_amazon_item_name(url)
        print(f"Item name: {item_name}")

        if item_name:
            # For simplicity, skip price scraping for now
            response = {
                'message': 'URL received and item name retrieved successfully.',
                'itemName': item_name,
            }
            return jsonify(response), 200
        else:
            print("Failed to retrieve item name from URL")
            return jsonify({"error": "Failed to retrieve item name from URL"}), 400
    except Exception as e:
        print(f"Error in save_url_data: {e}")
        return jsonify({"error": "An error occurred processing the request"}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
