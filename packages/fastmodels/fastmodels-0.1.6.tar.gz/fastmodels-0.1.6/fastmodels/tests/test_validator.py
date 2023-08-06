import unittest
from fastmodels.datavalidator.validator import validate_json

class TestValidator(unittest.TestCase):
    def test_validate_json_valid(self):
        valid_json = '{"prompt": "Hello, world!", "completion": "Hello, user!"}'
        self.assertTrue(validate_json(valid_json))

    def test_validate_json_invalid(self):
        invalid_json = '{"foo": "Hello, world!", "bar": "Hello, user!"}'
        self.assertFalse(validate_json(invalid_json))

    def test_validate_json_not_json(self):
        not_json = 'This is not a JSON string'
        self.assertFalse(validate_json(not_json))

if __name__ == '__main__':
    unittest.main()
