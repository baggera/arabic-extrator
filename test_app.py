import unittest
import json
from unittest.mock import patch, MagicMock
from app import app

class KeywordExtractorTestCase(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    @patch('requests.get')
    def test_extract_keywords_mocked(self, mock_get):
        # Mock the response from requests.get
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.content = """
        <html>
            <head><title>Test Page</title></head>
            <body>
                <h1>Welcome to the Test</h1>
                <p>This is a test paragraph for testing keyword extraction. test test.</p>
                <a>link1</a>
                <a>link2</a>
            </body>
        </html>
        """
        mock_get.return_value = mock_response

        payload = {
            "url": "http://mock-test.com",
            "selectors": ["h1", "p"]
        }
        response = self.app.post('/extract-keywords',
                                 data=json.dumps(payload),
                                 content_type='application/json')

        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('keywords', data)
        # Expected keywords: 'test' (4), 'welcome' (1), 'paragraph' (1), 'testing' (1), 'keyword' (1), 'extraction' (1)
        # Note: 'the', 'to', 'is', 'a', 'for' are stop words and should be removed.
        keywords = {item[0]: item[1] for item in data['keywords']}
        self.assertEqual(keywords.get('test'), 4)
        self.assertIn('welcome', keywords)
        print("Mock test passed. Keywords extracted:")
        print(data['keywords'])


    def test_missing_params(self):
        response = self.app.post('/extract-keywords',
                                 data=json.dumps({}),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn('error', data)

if __name__ == '__main__':
    unittest.main()
