import json

from tests.base_test import HTTPMethodsMixin, BaseTest, PatchMixin


class ExampleTest(BaseTest, HTTPMethodsMixin):

    def test_sample(self):
        response = json.loads(self.get(url='api.ping'))
        self.assertEqual(response['result'], 'pong')


class ExampleMocking(BaseTest, HTTPMethodsMixin, PatchMixin):

    def test_(self):
        self.mocked_http_get = self.patch('tests.test_example.sample_for_patch.sample.get')

        self.mocked_http_get.return_value = 'ok'
        from tests.test_example.sample_for_patch.sample import some_method

        self.assertEqual(some_method(), 'ok')
