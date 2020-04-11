import unittest
import requests
from os import getenv

ip = getenv('TEST_URL')

class TestAPI(unittest.TestCase):

    def test_bmi(self):
        r = requests.post(ip + '/calculate/bmi', json={'height': 158, 'weight': 39.4})
        result = r.json()
        # print(result)
        assert result['bmi_value'] == 15.78 and result['bmi_status'] == 'Underweight', "Test Failed :("

    def test_calorie(self):
        r = requests.post(ip + '/calculate/calorie', json={"goal": "maintain", "gender": "female",
                                                           "height": 158, "weight": 39.4, "age": 21,
                                                           "activity": "sedentary"})
        result = r.json()
        # print(result)
        assert result['calorie'] == 1462, "Test Failed :("


if __name__ == '__main__':
    unittest.main()
