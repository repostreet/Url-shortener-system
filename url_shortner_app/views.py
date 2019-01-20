# Third party import
from django.shortcuts import render
from django.http import JsonResponse, HttpResponseRedirect

# App level import
from .controllers.url_shortener import UrlShortenerClass
from .controllers.get_all_short_urls import url_list
from .controllers.original_url import get_original_url
from .controllers.delete_shortened_url import delete_short_url
from .controllers.redirect import get_redirect_url

FORBIDDEN_MESSAGE = {'message': 'Method not allowed'}


def home(request):
    """Some docs string."""
    context = {'Message': 'Welcome to home.'}
    return render(request, 'home.html', context)


def shorten_url(request):
    """Some docs string."""
    if request.method == 'POST':
        response, status_code = UrlShortenerClass(request)()
        return JsonResponse(response, status=status_code)
    else:
        return JsonResponse(FORBIDDEN_MESSAGE, status=400,)


def shortend_urls(request):
    """Some doc string."""
    if request.method == 'GET':
        response, status_code = url_list(request)
        return JsonResponse(response, status=status_code, safe=False)
    else:
        return JsonResponse(FORBIDDEN_MESSAGE, status=400)


def fetch_original_url(request):
    """Some docs string."""
    if request.method == 'POST':
        response, status_code = get_original_url(request)
        return JsonResponse(response, status=status_code, safe=False)
    else:
        return JsonResponse(FORBIDDEN_MESSAGE, status=400)


def delete_url(request):
    """Some docs string."""
    if request.method == 'POST':
        response, status_code = delete_short_url(request)
        return JsonResponse(response, status=status_code, safe=False)
    else:
        return JsonResponse(FORBIDDEN_MESSAGE, status=400)


def redirect_url(request, short_url):
    """Some docs string."""
    if request.method == 'GET':
        url = get_redirect_url(request, short_url)
        if url:
            return HttpResponseRedirect(url)
        else:
            JsonResponse({'message': 'No url to redirect'}, status=400)
    else:
        return JsonResponse(FORBIDDEN_MESSAGE, status=400)
