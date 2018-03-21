from tests.base_test import BaseTestWithHTTPMethodsMixin, BaseTest


class ExampleTest(BaseTest, BaseTestWithHTTPMethodsMixin):

    def test_sample(self):
        raw_response = self.get(url='api.ping')
        self.assertEqual(raw_response.get_data(as_text=True), 'pong')
