import unittest,  os
from app import create_app,db
from flask import  url_for

# usually, continues integraration/deployment providers set the CI env variable
am_i_in_the_cloud = os.environ.get("CI", False)
class BaseTestInit(unittest.TestCase):
    # when writing a test class, extend this class

    # setUp and tearDown are executed before *each* test_method
    def setUp(self):
        if am_i_in_the_cloud:
            self.app = create_app('staging')
        else:
            self.app = create_app('testing')

        # this is needed to make url_for work
        self.app.config['SERVER_NAME'] = 'localhost'

        self.app_context = self.app.app_context()
        self.app_context.push()
        self.db = db
        # clear the session first
        db.session.remove()
        try:
            # drop the db
            db.reflect()
            db.drop_all()
        except Exception:
            print("cannot drop db")
        # create all tables, as defined in /models.py
        db.create_all()
        # the client acts as a client brower - it can make requests to our app as if a client is making them
        self.client = self.app.test_client(use_cookies=True)


    def tearDown(self):
        db.session.remove()
        db.reflect()
        db.drop_all()
        self.app_context.pop()

    # on class creation
    @classmethod
    def setUpClass(cls):
        pass


class BaseTestWithHTTPMethods(BaseTestInit):
    """
    Class to be subclassed when doing client testing.
    """

    def post_adnresponse_data(self, url, data,url_args={}):
        return self.full_response(post=True, data=data, url=url, url_args=url_args).get_data(as_text=True)

    def get_response_data(self, url):
        return self.full_response(url=url).get_data(as_text=True)

    def full_response(self, post=False, data={}, url="", url_args={}):
        """
        :arg post [bool] - are we doing a post request
        :arg data [dict] - a dict with the dataload
        :arg url  [string] - endpoint (NOT a ready url) e.g. main.index and not just /
        :arg url_args - these will be passed as url arguments - e.g. in /user&id=1 id=1 would have been made by url_args={'id':1}

        :returns the data of the response (e.g. the return of the view function of the server)
        """
        if post:
            return self.client.post(url_for(url, _external=True, ), data=data, follow_redirects=True, query_string=url_args)
        else:
            return self.client.get(url_for(url, _external=True), follow_redirects=True, query_string=url_args)