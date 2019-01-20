# Third party import
import pytest
import requests

# App level import
from url_shortener import settings

# Fixture import
from .fixture import resource

class TestUrlShortenerAPI(object):

    def test_api_status_code(self, resource):
        """Test cases for checking status code"""
        unique_urls_list = resource
        for unique_url in unique_urls_list:
            for each_url in unique_url:
                data = {'url': each_url}
                res = requests.post('http://localhost:8000/shorten-url/', json=data)
                assert res.status_code == 200

        data = {}
        res = requests.post('http://localhost:8000/shorten-url/', json=data)
        assert res.status_code == 400

        res = requests.get('http://localhost:8000/shorten-url/')
        assert res.status_code == 400

    def test_api_function(self, resource):
        unique_urls_list = resource
        expected_output = ['http://localhost:8000/1', 'http://localhost:8000/6']

        for c, unique_url in enumerate(unique_urls_list):
            for each_url in unique_url:
                data = {'url': each_url}
                res = requests.post('http://localhost:8000/shorten-url/', json=data)
                count = settings.UrlCollection.count_documents(
                    {'shortend_url': expected_output[c]})
                assert count == 1
    
