# comeiin/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView


urlpatterns = [
    path('admin/', admin.site.urls),

    # Favicon
    path('favicon.ico', RedirectView.as_view(
        url=f'{settings.STATIC_URL}assets/favicon.png',
        permanent=True,
    )),

    # allauth — sign in, signup, Google OAuth
    path('accounts/', include('allauth.urls')),

    # Core — home, public pages, crawler files, PWA manifest and service worker
    path('', include('core.urls')),

    # Products
    path('products/', include('products.urls')),

    # Quotes
    path('quote/', include('quotes.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
