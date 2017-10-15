from tests.base_test import BaseTestWithHTTPMethods
from flask import current_app

class ExampleTest(BaseTestWithHTTPMethods):
    def test_sample(self):
        config = current_app.config
        response = self.get('main.index')
        self.assertIn('It works :)', response, "The HTML of the index page doesn't contain expected text")
