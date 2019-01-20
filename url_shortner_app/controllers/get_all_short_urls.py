# Third party import
from pymongo import errors

# App level import
from url_shortener import settings


def url_list(request):
    """Fetch all urls."""
    try:
        get_all_urls = settings.UrlCollection.find({}, {'_id': 0})
        get_all_urls = list(get_all_urls)
        result, status = get_all_urls, 200

    except (errors.ServerSelectionTimeoutError, errors.OperationFailure) as e:
        result, status = e, 400

    return result, status
