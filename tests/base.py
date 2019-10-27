"""
Contains a baseclass which all test classes extends.

Sets up the flask app and a client object which can make requests to the flask app.
The HTTP mixin provides common methods to make it easier to make HTTP requests to the app.
"""
import json
import unittest
from flask import url_for, Response
from app import create_app
from unittest.mock import patch
from dotenv import find_dotenv, load_dotenv


class BaseTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        path = find_dotenv('.env_test')
        assert path
        load_dotenv(path)

        from config import EnvironmentName, configs

        conf = configs[EnvironmentName.testing]
        cls.app = create_app(conf)
        cls.app.config['SERVER_NAME'] = 'localhost.lo'

        cls.app_context = cls.app.app_context()
        cls.app_context.push()

        # the client acts as a client browser - it can make requests to our app as if a client is making them
        cls.client = cls.app.test_client(use_cookies=True)

    @classmethod
    def tearDownClass(cls):
        cls.app_context.pop()

    def setUp(self):
        pass

    def tearDown(self):
        pass


class HTTPMethodsMixin(object):
    """
    Class to be subclassed when doing client testing.
    """

    def post(self, url, data, **kwargs):
        return self.full_response(method='POST', data=data, url=url, **kwargs)

    def get(self, url, **kwargs):
        return self.full_response(url=url, **kwargs)

    def put(self, **kwargs):
        return self.full_response(method='PUT', **kwargs)

    def delete(self, **kwargs):
        return self.full_response(method='DELETE', **kwargs)

    def full_response(self, method='GET', data=None,
                      url="",
                      url_args=None,
                      url_for_args=None,
                      raw_response=False,
                      headers=None) -> Response:
        """
        convenience method that wraps a http request to the flask app.

        :arg method [str] - the name of the http method
        :arg data [dict] - a dict with the payload. it will jsonified before passing to the test client
        :arg url  [string] - endpoint (NOT a ready url) e.g. main.index and *not* /main
        :arg url_args - these will be passed as url query arguments:
            e.g. in /user&id=1 id=1 would have been made by url_args={'id':1}
        :arg raw_response [boolean] - if false, the return value of this method will be the text response from the server;
            otherwise the raw response as returned by the `requests` library
        :arg url_for_args [dict] - will be passed to url_for when building the url for the endpoint
        :returns the data of the response (e.g. the return of the view function of the server)
        """

        if url_for_args is None:  # avoid mutable default kwargs
            url_for_args = {}
        if url_args is None:
            url_args = {}

        common_args = [url_for(url, **url_for_args, _external=True)]
        jsonified = data
        if not isinstance(data, str) and data:
            jsonified = json.dumps(data)

        # http://werkzeug.pocoo.org/docs/0.14/test/#werkzeug.test.EnvironBuilder
        common_kwargs = {
            "data": jsonified if jsonified else None,
            "follow_redirects": True,
            "query_string": url_args,
            "headers": headers  # [('Content-Type', 'text/html; charset=utf-8'),]
        }
        method_name = method.lower()

        method = getattr(self.client, method_name)
        if not method:
            raise Exception("unknown HTTP method %s" % method_name)
        res = method(*common_args, **common_kwargs)

        return res if raw_response else res.get_data(as_text=True)


class PatchMixin(object):
    """
    used when mocking. extending class should be a unittest.TestCase
    https://makina-corpus.com/blog/metier/2013/dry-up-mock-instanciation-with-addcleanup

    Testing utility mixin that provides methods to patch objects so that they
    will get unpatched automatically.
    """

    def patch(self, *args, **kwargs):
        patcher = patch(*args, **kwargs)
        self.addCleanup(patcher.stop)
        return patcher.start()

    def patch_object(self, *args, **kwargs):
        patcher = patch.object(*args, **kwargs)
        self.addCleanup(patcher.stop)
        return patcher.start()

    def patch_dict(self, *args, **kwargs):
        patcher = patch.dict(*args, **kwargs)
        self.addCleanup(patcher.stop)
        return patcher.start()
