import unittest, os
from app import create_app
from flask import url_for

# usually, continuous integration providers set the CI env variable
am_i_in_ci = os.environ.get("CI", False)
if am_i_in_ci:
    print("CI environment detected")


class BaseTest(unittest.TestCase):
    # when writing a test class, extend this class

    def setUp(self):
        if am_i_in_ci:
            self.app = create_app('staging')
            print("Running tests in staging environment")
        else:
            self.app = create_app('testing')
            print("Running tests in testing environment")

        # this is needed to make url_for work
        self.app.config['SERVER_NAME'] = 'localhost'

        self.app_context = self.app.app_context()
        self.app_context.push()

        # the client acts as a client browser - it can make requests to our app as if a client is making them
        self.client = self.app.test_client(use_cookies=True)

    def tearDown(self):
        self.app_context.pop()

    # on class creation
    @classmethod
    def setUpClass(cls):
        pass


class BaseTestWithHTTPMethods(BaseTest):
    """
    Class to be subclassed when doing client testing.
    """

    def post(self, url, data, url_args={}):
        return self.full_response(method='POST', data=data, url=url, url_args=url_args).get_data(as_text=True)

    def get(self, url):
        return self.full_response(url=url).get_data(as_text=True)

    def full_response(self, method='GET', data={}, url="", url_args={}):
        """
        :arg method [bool] - are we doing a POST request
        :arg data [dict] - a dict with the payload
        :arg url  [string] - endpoint (NOT a ready url) e.g. main.index and *not* just /
        :arg url_args - these will be passed as url arguments - e.g. in /user&id=1 id=1 would have been made by url_args={'id':1}

        :returns the data of the response (e.g. the return of the view function of the server)
        """
        common_args = [url_for(url, _external=True)]
        common_kwargs = {
            "follow_redirects": True,
            "query_string": url_args
        }

        if method == 'POST':
            return self.client.post(*common_args, data=data, **common_kwargs)
        elif method == 'GET':
            return self.client.get(*common_args, **common_kwargs)
        else:
            raise Exception("unknown method %s" % method)
