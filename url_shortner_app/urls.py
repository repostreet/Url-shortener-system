# Third party import
from django.urls import path, re_path

# App level import
from .views import (
    home, shorten_url, shortend_urls,
    fetch_original_url, delete_url, redirect_url
)


urlpatterns = [
    path('', home, name='home'),
    path('shorten-url/', shorten_url, name='shorten_url'),
    path('shortend-urls/', shortend_urls, name='shortend_urls'),
    path('fetch-original-url/', fetch_original_url, name='fetch_original_url'),
    path('delete-url/', delete_url, name='delete_url'),
    # path('<str:short_url>/', redirect_url, name='redirect_shortened_url')
    re_path(r'^(?P<short_url>[\w+])/$',
            redirect_url, name='redirect_shortened_url'),
]
