# coding=utf-8
import enum
import unittest
import json
from app import *

# Custom test class, setUp method and tearDown method will be executed before and after the test respectively.
# The function starting with test_ is the specific test code.
from app.models import User


class GenderEnum(enum.Enum):
    MALE = 1
    FEMALE = 2
    SECRET = 3
    UNKNOW = 4


class DatabaseTestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqldb://root:111@127.0.0.1:3306/sys?charset=utf8'
        self.app = app
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    # test code
    def test_append_data(self):
        ac = User(telephone='15238681389', username='zqy',
                  email='947440142@qq.com', password='111')
        db.session.add(ac)
        db.session.commit()
        user = User.query.filter_by(telephone='15238681389').first()

        # Assert that data exists
        self.assertIsNotNone(user)
    # def tearDown(self):
    #     db.session.remove()
    #     db.drop_all()


class TestLogin(unittest.TestCase):
    """定义测试案例"""
    def setUp(self):
        """在执行具体的测试方法前，先被调用"""
        self.app = app
        # Activate test flag
        app.config['TESTING'] = True
        # You can use python's http standard client for testing
        # urllib  urllib2  requests
        # Here, use the test client provided by flask for testing
        self.client = app.test_client()

    def test_empty_name_password(self):
        """Test simulation scenario, user name or password is incomplete"""
        # Use the client to send a post request to the backend,
        # data indicates the sent data, and a response object will be returned
        response = self.client.post("/login/", data={})
        # respoonse.data is response body data
        resp_json = response.data
        # Parse according to json
        resp_dict = json.loads(resp_json)
        # Use assertion to verify: whether there is a code string in the dictionary
        self.assertIn("code", resp_dict)
        # Get the value of the return code of the code and verify whether it is the error code 400
        code = resp_dict.get("code")
        self.assertEqual(code, 400)
        # Test only pass telephone
        response = self.client.post("/login/", data={"telephone": "15238681389"})
        # respoonse.data is the response body data
        resp_json = response.data
        # Parse according to json
        resp_dict = json.loads(resp_json)
        # Use assertions for verification
        self.assertIn("code", resp_dict)
        # Verification error code 400
        code = resp_dict.get("code")
        self.assertEqual(code, 400)
        # Verify the return information
        msg = resp_dict.get('message')
        self.assertEqual(msg, "Form input format error")

    def test_wrong_name_password(self):
        """Incorrect test username or password"""
        # Use the client to send a post request to the backend,
        # data indicates the sent data, and a response object will be returned
        response = self.client.post("/login/", data={"telephone": "15238681389", "password": "123456789"})
        # Incorrect test username or password
        resp_json = response.data
        # Parse according to json
        resp_dict = json.loads(resp_json)
        # Use assertions for verification
        self.assertIn("code", resp_dict)
        # Verify error code
        code = resp_dict.get("code")
        self.assertEqual(code, 400)
        # Verify the return information
        msg = resp_dict.get('message')
        self.assertEqual(msg, "Wrong phone number or password！Please confirm before logging in")


if __name__ == '__main__':
    unittest.main()
