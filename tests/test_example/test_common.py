import json

from tests.base_test import HTTPMethodsMixin, BaseTest, PatchMixin


class ExampleTest(BaseTest, HTTPMethodsMixin):

    def test_sample(self):
        response = json.loads(self.get(url='api.ping'))
        self.assertEqual(response['result'], 'pong')


class ExampleMocking(BaseTest, HTTPMethodsMixin, PatchMixin):

    def test_(self):
        self.mocked_time = self.patch('app.helpers.time.utc_now_str')

        self.mocked_time.return_value = '1969'

        from app.helpers.time import utc_now_str
        self.assertEqual(utc_now_str(), '1969')
