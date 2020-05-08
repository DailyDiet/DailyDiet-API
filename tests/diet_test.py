import unittest
import requests
import json

ip = getenv('TEST_URL')

class TestDiet(unittest.TestCase):

    def test_sevade(self):
        r = requests.get(ip + '/food/sevade', json={'calorie': 2300})
        result = r.result()
        assert result['diet'][3] in range(2990, 2310, 1), 'Test Failed :('

    def test_zero_sevade(self):
        r = requests.get(ip + '/food/sevade', json={'calorie': 0})
        assert r.status_code == 404, 'Khak bar saret :('
