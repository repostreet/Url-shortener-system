# App level import
from url_shortener import settings


def get_redirect_url(request, short_url):
    """Fetch all urls."""
    try:
        url = request.scheme + '://' + request.get_host() + '/' + short_url
        url_instance = settings.UrlCollection.find_one({'shortend_url': url})
        url = url_instance.get('original_url')

        if isinstance(url, str):
            url = 'https://' + url
        else:
            return

    except Exception as e:
        print(e)
        return

    return url
