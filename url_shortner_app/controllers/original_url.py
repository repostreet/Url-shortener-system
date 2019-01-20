# Core import
import json

# App level import
from url_shortener import settings


def get_original_url(request):
    """Fetch all urls."""
    try:
        body = json.loads(request.body.decode('utf-8'))
        url = body.get('url')
        get_original_url = settings.UrlCollection.find_one(
            {'shortend_url': url}, {'_id': 0})

        if get_original_url:
            get_original_url = [get_original_url]
            status = 200
        else:
            get_original_url = 'Not found.'
            status = 400

        result, status = get_original_url, status

    except Exception as e:
        result, status = e, 400

    return result, status
