# Core import
import json
import string

# Third party import
from pymongo import errors

# App level import
from url_shortener import settings

BAD_REQUEST_MESSAGE = 'Please post a valid data'
ENCODING_CHARACTER = (string.digits + string.ascii_lowercase +
                      string.ascii_uppercase)


class UrlShortenerClass:
    """
    Class which takes request parameter as theinstance attribute.
    When __call__ in invoked it generates a shortlink for
    the an url which is supposed to be passed in the body as
    a field named 'url'. The shortlink is then
    inserted into the database.
    """

    def __init__(self, request):
        self.request = request

    def shorten_url(self):
        cleaned_url = self._get_cleaned_url()
        response, status = self._generate_shortend_url(cleaned_url)
        return response, status

    def _get_cleaned_url(self):
        """
        Do the following things.
        1. Remove the protocol if it exists.
        2. Remove the www CNAME as well if it exists.
        """
        try:
            request_body = self.request.body.decode('utf-8')
            request_body = json.loads(request_body)

            url = request_body.get('url')
            cleaned_url = self._strip_url(url)
        except Exception as e:
            print(e)
            cleaned_url = str()

        return cleaned_url

    def _generate_shortend_url(self, cleaned_url):
        """
        The url shorteneing takes place in this function.
        1.  Query a collection which stores the number of
            url that have been shortened which we will get
            from the counter field of a document(Only single docs exists).

        2.  Increment the value by 1 of the retrieved counter.

        3.  Generate has value by using follwing method
            a. We want to use a technique which will convert the number
               (counter) from base 10 encoding to base 62
                encoding (which will be a combination od [A-Za-z0-9])
            b. After encoding store the encoded number into db.

        4.  Return appropriate success message and status code
        """
        status, response = 200, str()
        letter_list, base = [], len(ENCODING_CHARACTER)
        req = self.request
        domain = req.scheme + '://' + req.get_host()

        if not cleaned_url:
            response = BAD_REQUEST_MESSAGE
            status = 400
            return response, status

        try:
            last_inserted = settings.LastInsertedCounter.find_one_and_update(
                {}, {'$inc': {'counter': 1}}, upsert=True) or {}
            last_inserted = last_inserted.get('counter', 1)
            incr_counter = last_inserted + 1

            while incr_counter > 0:
                val = incr_counter % base
                letter_list.append(ENCODING_CHARACTER[val])
                incr_counter = incr_counter // base

            letter = domain + '/' + ''.join(letter_list[::-1])
            short_url_data = {'$setOnInsert': {'shortend_url': letter,
                              'original_url': cleaned_url}}

            settings.UrlCollection.update_one(
                {'original_url': cleaned_url},
                short_url_data, upsert=True)

            response = 'Short Url created'

        except (errors.ServerSelectionTimeoutError,
                errors.OperationFailure) as e:
            status = 400
            response = e

        return response, status

    @staticmethod
    def _strip_url(url):
        if url[:8] == 'https://':
            url = url[8:]
        if url[:7] == 'http://':
            url = url[7:]
        if url[:4] == 'www.':
            url = url[4:]
        return url

    def __call__(self):
        result, status = self.shorten_url()
        response = {'message': result}
        return response, status
