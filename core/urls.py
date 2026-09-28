# core/urls.py
from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    # HTML pages
    path('', views.home_view, name='home'),
    path('about/', views.about_view, name='about'),
    path('contact/', views.contact_view, name='contact'),
    path('industries/', views.industries_view, name='industries'),
    path('laboratory/', views.laboratory_redirect, name='laboratory'),
    path('engineering/', views.engineering_redirect, name='engineering'),
    path('privacy/', views.privacy_view, name='privacy'),
    path('terms/', views.terms_view, name='terms'),
    path('cookies/', views.cookies_view, name='cookies'),

    # Crawler discovery
    path('robots.txt', views.robots_txt, name='robots-txt'),
    path('sitemap.xml', views.sitemap_xml, name='sitemap-xml'),

    # Permanent redirects for URLs published by the previous static site.
    path('index.html', views.legacy_home_redirect, name='legacy-home'),
    path('home.html', views.legacy_home_redirect, name='legacy-home-file'),
    path('about.html', views.legacy_about_redirect, name='legacy-about'),
    path('contact.html', views.legacy_contact_redirect, name='legacy-contact'),
    path('laboratory.html', views.legacy_laboratory_redirect, name='legacy-laboratory'),
    path('engineering.html', views.legacy_engineering_redirect, name='legacy-engineering'),
    path('privacy.html', views.legacy_privacy_redirect, name='legacy-privacy'),
    path('terms.html', views.legacy_terms_redirect, name='legacy-terms'),
    path('cookies.html', views.legacy_cookies_redirect, name='legacy-cookies'),

    # API
    path('api/contact/', views.ContactMessageCreateView.as_view(), name='api-contact'),
    path('api/testimonials/', views.TestimonialListView.as_view(), name='api-testimonials'),
    path('api/highlights/', views.HighlightListView.as_view(), name='api-highlights'),
    path('api/hero-slides/', views.HeroSlideListView.as_view(), name='api-hero-slides'),

    # PWA
    path('manifest.json', views.pwa_manifest, name='pwa-manifest'),
    path('serviceworker.js', views.pwa_sw, name='pwa-sw'),
]
