# Core import
import json

# App level import
from url_shortener import settings


def delete_short_url(request):
    """Fetch all urls."""
    try:
        body = json.loads(request.body.decode('utf-8'))
        url = body.get('url')
        settings.UrlCollection.delete_one({'shortend_url': url})

        message = '{} has been removed from the db.'.format(url)
        status = 200

        result, status = message, status

    except Exception as e:
        result, status = e, 400

    return result, status
