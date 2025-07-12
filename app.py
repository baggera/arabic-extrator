from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup
import re
from collections import Counter

app = Flask(__name__)

@app.route('/extract-keywords', methods=['POST'])
def extract_keywords():
    data = request.get_json()
    url = data.get('url')
    selectors = data.get('selectors')

    if not url or not selectors:
        return jsonify({'error': 'URL and selectors are required'}), 400

    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        return jsonify({'error': str(e)}), 400

    soup = BeautifulSoup(response.content, 'html.parser')

    text_parts = []
    for selector in selectors:
        for element in soup.select(selector):
            text_parts.append(element.get_text())

    full_text = ' '.join(text_parts)

    # Clean and tokenize the text
    words = re.findall(r'\b\w+\b', full_text.lower())

    # Remove common stop words (you can expand this list)
    stop_words = set(['the', 'a', 'in', 'of', 'to', 'and', 'is', 'for', 'on', 'with', 'that', 'it', 'as', 'at', 'by', 'from'])
    filtered_words = [word for word in words if word not in stop_words and not word.isdigit()]

    # Count word frequency
    word_counts = Counter(filtered_words)

    # Get the most common keywords
    keywords = word_counts.most_common(20) # Return top 20 keywords

    return jsonify({'keywords': keywords})

if __name__ == '__main__':
    app.run(debug=True, port=8080)
