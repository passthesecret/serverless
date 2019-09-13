import unittest
import json
import passthesecret.passthesecret as passthesecret

class TestApp(unittest.TestCase):

    def test_create_secret(self):
        plaintext = 'Lorem ipsum dolor sit amet'
        response = passthesecret.create_secret(
            # All of the rest of this object is irrelevant, for now
            {'body': '{\n "secret": "' + plaintext + '",\n "expire_in_seconds": 43200,\n "burn_after_reading": false\n}'},
            {}
        )
        self.assertEqual(response['statusCode'], 200)
        body = json.loads(response['body'])
        self.assertEqual(len(body['secret_request_string']), 76, 'Secret Request String Not 76 Characters')
        self.assertEqual(len(body['wipe_request_string']), 76, 'Wipe Request String Not 76 Characters')

    def test_get_secret(self):
        plaintext = 'Lorem ipsum dolor sit amet'
        create_response = passthesecret.create_secret(
            # All of the rest of this object is irrelevant, for now
            {'body': '{\n "secret": "' + plaintext + '",\n "expire_in_seconds": 43200,\n "burn_after_reading": false\n}'},
            {}
        )
        create_body = json.loads(create_response['body'])
        get_response = passthesecret.get_secret(
            {'pathParameters': {'requestString': create_body['secret_request_string']}},
            {}
        )
        get_body = json.loads(get_response['body'])
        # Test Secret Matches
        self.assertEqual(get_response['statusCode'], 200, 'Retrieved Secret Does Return 200 Status Code')
        self.assertEqual(get_body['secret'], plaintext, 'Retrieved Secret Does Not Match Stored Secret')
        # Test Totally Wrong Secret Request String
        get_response = passthesecret.get_secret(
            {'pathParameters': {'requestString': create_body['secret_request_string'][::-1]}},
            {}
        )
        self.assertEqual(get_response['statusCode'], 422,
                         'Invalid Secret Request String (Reversed) Does Not Raise 422 Error')
        # Test Secret Request String With Invalid UUID
        invalid_request = 'x' + create_body['secret_request_string'][1:]
        get_response = passthesecret.get_secret(
            {'pathParameters': {'requestString': invalid_request}},
            {}
        )
        # Test Secret Request String With Invalid UUID
        self.assertEqual(get_response['statusCode'], 422,
                         'Invalid Secret Request String (Invalid UUID) Does Not Raise 422 Error')
        # Test Secret Request String With Invalid Fernet Key
        invalid_request = create_body['secret_request_string'][:-1] + '*'
        get_response = passthesecret.get_secret(
            {'pathParameters': {'requestString': invalid_request}},
            {}
        )
        self.assertEqual(get_response['statusCode'], 422,
                         'Invalid Secret Request String (Invalid Fernet Key) Does Not Raise Error')

    def test_get_consumable_secret(self):
        plaintext = 'Lorem ipsum dolor sit amet'
        create_response = passthesecret.create_secret(
            # All of the rest of this object is irrelevant, for now
            {'body': '{\n "secret": "' + plaintext + '",\n "expire_in_seconds": 43200,\n "burn_after_reading": true\n}'},
            {}
        )
        create_body = json.loads(create_response['body'])
        get_response = passthesecret.get_secret(
            {'pathParameters': {'requestString': create_body['secret_request_string']}},
            {}
        )
        get_body = json.loads(get_response['body'])
        self.assertEqual(get_response['statusCode'], 200, 'Retrieved Secret Does Return 200 Status Code')
        self.assertEqual(get_body['secret'], plaintext, 'Retrieved Secret Does Not Match Stored Secret')
        get_response_second = passthesecret.get_secret(
            {'pathParameters': {'requestString': create_body['secret_request_string']}},
            {}
        )
        self.assertEqual(get_response_second['statusCode'], 404, 'Retrieved Secret Does Not Return 404 Status Code')


if __name__ == '__main__':
    unittest.main()
