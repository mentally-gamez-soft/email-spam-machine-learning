import unittest
from flask import current_app
from core.ws_spam_model_updater import api


class TestWeServiceRefineModel(unittest.TestCase):
    def setUp(self):
        self.app = api.web_service_api.run(debug=True)
        self.appctx = self.app.app_context()
        self.appctx.push()
        self.client = self.app.test_client()

    def tearDown(self): 
        self.appctx.pop()
        self.app = None
        self.appctx = None
        self.client = None

    def test_app(self):
        assert self.app is not None
        assert current_app == self.app

    def test_home_page_redirect(self):
        response = self.client.get('/spam-email-refine/api/v1.0')
        assert response.status_code == 200

    def test_api_get_users(self):
        token = self.get_api_token()
        response = self.client.get(
            '/api/users', headers={'Authorization': f'Bearer {token}'})
        assert response.status_code == 200
        assert len(response.json['items']) == 1
        assert response.json['items'][0]['username'] == 'susan'
