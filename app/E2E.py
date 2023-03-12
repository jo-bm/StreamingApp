import requests
import random
import unittest

# Define constants for URLs
BASE_URL = 'http://localhost'
FILE_LIST_URLS = [
    '/file_list/Black_Lagoon',
    '/file_list/ChainsawMan',
    '/file_list/CowboyBebop',
    '/file_list/BakiHanma',
    '/file_list/Dr.Stone',
    '/file_list/AOT'
]

class CatalogTestCase(unittest.TestCase):

    def setUp(self):
        self.headers = {'Accept': 'application/json'}

    def test_get_localhost(self):
        url = f"{BASE_URL}"
        res = requests.get(url)
        self.assertEqual(res.status_code, 200)

    def test_get_404(self):
        url = f"{BASE_URL}/nonexistent"
        res = requests.get(url)
        self.assertEqual(res.status_code, 404)

    def test_get_file_list(self):
        for url in FILE_LIST_URLS:
            res = requests.get(f"{BASE_URL}{url}")
            self.assertEqual(res.status_code, 200)

    def test_get_episodes(self):
        url = f"{BASE_URL}/file_list/Black_Lagoon"
        res = requests.get(url, headers=self.headers)
        self.assertEqual(res.status_code, 200)
        for i in range(5):
            episode_number = str(random.randint(1, 10)).zfill(2)
            episode_name = f"Black_Lagoon_S01E{episode_number}"
            episode_name_bytes = bytes(episode_name, 'utf-8')
            self.assertIn(episode_name_bytes, res.content)

            
            