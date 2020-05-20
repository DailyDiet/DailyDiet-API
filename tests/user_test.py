import unittest
import requests
from os import getenv

ip = 'https://dailydiet-api.herokuapp.com/'


class TestUser(unittest.TestCase):

    def test_create1(self):
        # correct things :D
        r = requests.post(ip + '/users/signup',
                          json={'full_name': 'Ken Adams', 'email': 'nimaafshar79@gmail.com',
                                'password': 'Audio123', 'confirm_password': 'Audio123'})
        assert r.status_code == 201, r.content

    def test_create2(self):
        # mismatching passwords
        r = requests.post(ip + '/users/signup',
                          json={'full_name': 'Ken Adams', 'email': 'yasi_ommi@yahoo.com',
                                'password': 'Audio123', 'confirm_password': 'Audio456'})
        assert r.status_code == 400, 'Test Failed :('

    def test_create3(self):
        # invalid email
        r = requests.post(ip + '/users/signup',
                          json={'full_name': 'Ken Adams', 'email': 'chertopert@chert.con',
                                'password': 'Audio123', 'confirm_password': 'Audio123'})
        assert r.status_code == 400, 'Test Failed :('

    def test_signin1(self):
        # correct
        r = requests.post(ip + '/users/signin',
                          json={'email': 'arnold.schwarzenegger@gmail.com', 'password': 'p@$$word123'})
        assert r.status_code == 200, r.content

    def test_signin2(self):
        # mismatching email and passwords
        r = requests.post(ip + '/users/signin',
                          json={'email': 'arnold.schwarzenegger@gmail.com', 'password': 'probablywrong'})
        assert r.status_code == 403, 'Test Failed :('

    def test_signin3(self):
        # invalid email
        r = requests.post(ip + '/users/signin',
                          json={'email': 'chertopert@chert.con', 'password': 'p@$$word123'})
        assert r.status_code == 400, 'Test Failed :('

    def test_modify1(self):
        # change password
        r = requests.post(ip + '/users/signup/modify',
                          json={'old_password': 'p@$$word123', 'new_password': '123456', 'confirm_password': '123456'})
        assert r.status_code == 204, 'Test Failed :('

    def test_modify2(self):
        # mismtach passwords
        r = requests.post(ip + '/users/signup/modify',
                          json={'old_password': 'p@$$word123', 'new_password': '123456', 'confirm_password': '7891011'})
        assert r.status_code == 400, 'Test Failed :('


if __name__ == '__main__':
    unittest.main()
