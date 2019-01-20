import pytest

from url_shortener import settings

@pytest.fixture()
def resource():
    test_data = open('tests/test_data/original_urls.txt', 'r')
    url_list = test_data.readlines()
    url_chunks = set()
    unique_urls_list = []

    for i in url_list:
        url_chunks.add(i.strip())
        if len(url_chunks) == 5:
           unique_urls_list.append(url_chunks)
           url_chunks = set()

    yield unique_urls_list

    settings.UrlCollection.delete_many({})
    settings.LastInsertedCounter.delete_many({})
