# core/views.py
from django.shortcuts import redirect, render
from django.core.mail import send_mail
from django.conf import settings
import os
from xml.sax.saxutils import escape
from django.http import JsonResponse, HttpResponse
from django.conf import settings
from django.views.decorators.cache import cache_control
from rest_framework import generics, status
from rest_framework.response import Response

from .models import ContactMessage, Testimonial, Highlight, HeroSlide
from .serializers import (
    ContactMessageSerializer,
    TestimonialSerializer,
    HighlightSerializer,
    HeroSlideSerializer,
)


# ============================================================
# TEMPLATE (HTML) VIEWS
# ============================================================

def home_view(request):
    """Homepage — pulls highlights, testimonials, hero slides, categories, featured products."""
    from products.models import Category, Product

    context = {
        'highlights': Highlight.objects.all()[:8],
        'testimonials': Testimonial.objects.filter(is_active=True)[:10],
        'hero_slides': HeroSlide.objects.filter(is_active=True)[:5],
        'categories': Category.objects.filter(is_active=True)[:8],
        'featured_products': Product.objects.filter(
            is_active=True, is_featured=True
        ).select_related('category')[:3],
    }
    return render(request, 'index.html', context)


def about_view(request):
    return render(request, 'about.html')


def industries_view(request):
    """Show the sectors Comeiin Works supports and their typical requirements."""
    return render(request, 'industries.html')


def laboratory_redirect(request):
    """Keep older Laboratory links working after the navigation restructure."""
    query = request.GET.urlencode()
    destination = '/industries/'
    if query:
        destination = f'{destination}?{query}'
    return redirect(destination, permanent=True)


def engineering_redirect(request):
    """Keep old Engineering links useful after consolidating project support."""
    return redirect('/industries/?industry=manufacturing#industry-paths', permanent=True)


def contact_view(request):
    return render(request, 'contact.html')


def privacy_view(request):
    return render(request, 'privacy.html')


def terms_view(request):
    return render(request, 'terms.html')


def cookies_view(request):
    return render(request, 'cookies.html')


def legacy_home_redirect(request):
    return redirect('core:home', permanent=True)


def legacy_about_redirect(request):
    return redirect('core:about', permanent=True)


def legacy_contact_redirect(request):
    return redirect('core:contact', permanent=True)


def legacy_laboratory_redirect(request):
    return redirect('core:industries', permanent=True)


def legacy_engineering_redirect(request):
    return redirect('/industries/?industry=manufacturing#industry-paths', permanent=True)


def legacy_privacy_redirect(request):
    return redirect('core:privacy', permanent=True)


def legacy_terms_redirect(request):
    return redirect('core:terms', permanent=True)


def legacy_cookies_redirect(request):
    return redirect('core:cookies', permanent=True)


@cache_control(max_age=3600, public=True)
def robots_txt(request):
    body = f'User-agent: *\nAllow: /\n\nSitemap: {settings.SITE_URL}/sitemap.xml\n'
    return HttpResponse(body, content_type='text/plain; charset=utf-8')


@cache_control(max_age=3600, public=True)
def sitemap_xml(request):
    """Return only canonical, public URLs that should appear in search."""
    from django.urls import reverse
    from products.models import Product

    paths = [
        reverse('core:home'),
        reverse('core:about'),
        reverse('products:catalogue'),
        reverse('core:industries'),
        reverse('core:contact'),
    ]
    paths.extend(
        reverse('products:product-detail', kwargs={'slug': product.slug})
        for product in Product.objects.filter(is_active=True).only('slug')
    )
    xml_urls = [
        f'  <url><loc>{escape(settings.SITE_URL + path)}</loc></url>'
        for path in paths
    ]
    xml = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + '\n'.join(xml_urls)
        + '\n</urlset>\n'
    )
    return HttpResponse(xml, content_type='application/xml; charset=utf-8')


# ============================================================
# API VIEWS
# ============================================================

class ContactMessageCreateView(generics.CreateAPIView):
    """POST /api/contact/ — submit contact form"""
    queryset = ContactMessage.objects.all()
    serializer_class = ContactMessageSerializer

    def perform_create(self, serializer):
        instance = serializer.save()

        # Send notification email (fails silently if email not configured)
        try:
            send_mail(
                subject=f"New Contact: {instance.subject or 'Website enquiry'}",
                message=(
                    f"Name: {instance.name}\n"
                    f"Email: {instance.email}\n"
                    f"Phone: {instance.phone}\n"
                    f"Company: {instance.company}\n\n"
                    f"{instance.message}"
                ),
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.CONTACT_RECEIVER_EMAIL],
                fail_silently=True,
            )
        except Exception:
            pass


class TestimonialListView(generics.ListAPIView):
    queryset = Testimonial.objects.filter(is_active=True)
    serializer_class = TestimonialSerializer


class HighlightListView(generics.ListAPIView):
    queryset = Highlight.objects.all()
    serializer_class = HighlightSerializer


class HeroSlideListView(generics.ListAPIView):
    queryset = HeroSlide.objects.filter(is_active=True)
    serializer_class = HeroSlideSerializer

# ============================================================
# PWA — MANIFEST
# ============================================================

@cache_control(max_age=3600, public=True)
def pwa_manifest(request):
    """Serve PWA manifest — embedded, no filesystem dependency."""
    manifest = {
        "id": "/?source=pwa",
        "name": "Comeiin Works — Laboratory Equipment & Consumables",
        "short_name": "Comeiin",
        "description": "Laboratory equipment, consumables, glassware, plasticware and safety supplies.",
        "start_url": "/?source=pwa",
        "scope": "/",
        "display": "standalone",
        "display_override": ["window-controls-overlay", "standalone"],
        "orientation": "portrait",
        "background_color": "#ffffff",
        "theme_color": "#0f172a",         # navy
        "lang": "en-ZA",
        "dir": "ltr",
        "categories": ["business", "shopping", "science"],
        "prefer_related_applications": False,

        "icons": [
            {"src": "/static/assets/pwa/icon-72.png",  "sizes": "72x72",   "type": "image/png", "purpose": "any"},
            {"src": "/static/assets/pwa/icon-72-maskable.png",  "sizes": "72x72",   "type": "image/png", "purpose": "maskable"},
            {"src": "/static/assets/pwa/icon-96.png",  "sizes": "96x96",   "type": "image/png", "purpose": "any"},
            {"src": "/static/assets/pwa/icon-96-maskable.png",  "sizes": "96x96",   "type": "image/png", "purpose": "maskable"},
            {"src": "/static/assets/pwa/icon-128.png", "sizes": "128x128", "type": "image/png", "purpose": "any"},
            {"src": "/static/assets/pwa/icon-128-maskable.png", "sizes": "128x128", "type": "image/png", "purpose": "maskable"},
            {"src": "/static/assets/pwa/icon-144.png", "sizes": "144x144", "type": "image/png", "purpose": "any"},
            {"src": "/static/assets/pwa/icon-144-maskable.png", "sizes": "144x144", "type": "image/png", "purpose": "maskable"},
            {"src": "/static/assets/pwa/icon-152.png", "sizes": "152x152", "type": "image/png", "purpose": "any"},
            {"src": "/static/assets/pwa/icon-152-maskable.png", "sizes": "152x152", "type": "image/png", "purpose": "maskable"},
            {"src": "/static/assets/pwa/icon-192.png", "sizes": "192x192", "type": "image/png", "purpose": "any"},
            {"src": "/static/assets/pwa/icon-192-maskable.png", "sizes": "192x192", "type": "image/png", "purpose": "maskable"},
            {"src": "/static/assets/pwa/icon-384.png", "sizes": "384x384", "type": "image/png", "purpose": "any"},
            {"src": "/static/assets/pwa/icon-384-maskable.png", "sizes": "384x384", "type": "image/png", "purpose": "maskable"},
            {"src": "/static/assets/pwa/icon-512.png", "sizes": "512x512", "type": "image/png", "purpose": "any"},
            {"src": "/static/assets/pwa/icon-512-maskable.png", "sizes": "512x512", "type": "image/png", "purpose": "maskable"},
        ],

        "screenshots": [
            {
                "src": "/static/assets/pwa/screenshot-desktop.png",
                "sizes": "1280x720",
                "type": "image/png",
                "platform": "wide",
                "label": "Browse the Comeiin catalogue on desktop",
            },
            {
                "src": "/static/assets/pwa/screenshot-mobile.png",
                "sizes": "750x1334",
                "type": "image/png",
                "platform": "narrow",
                "label": "Search laboratory supplies on mobile",
            },
        ],

        "shortcuts": [
            {
                "name": "Catalogue",
                "short_name": "Catalogue",
                "description": "Browse all laboratory products",
                "url": "/products/",
                "icons": [{"src": "/static/assets/pwa/shortcut-catalogue.png", "sizes": "96x96", "type": "image/png"}],
            },
            {
                "name": "About",
                "short_name": "About",
                "description": "About Comeiin Works",
                "url": "/about/",
                "icons": [{"src": "/static/assets/pwa/shortcut-about.png", "sizes": "96x96", "type": "image/png"}],
            },
            {
                "name": "Contact",
                "short_name": "Contact",
                "description": "Contact the Comeiin team",
                "url": "/contact/",
                "icons": [{"src": "/static/assets/pwa/shortcut-contact.png", "sizes": "96x96", "type": "image/png"}],
            },
        ],
    }
    response = JsonResponse(manifest, content_type='application/manifest+json')
    response['Cache-Control'] = 'public, max-age=3600'
    response['Access-Control-Allow-Origin'] = '*'
    return response


# ============================================================
# PWA — SERVICE WORKER
# ============================================================

def pwa_sw(request):
    """Serve service worker from static/js/serviceworker.js"""
    sw_path = os.path.join(settings.BASE_DIR, 'static', 'js', 'serviceworker.js')
    print(f"[PWA] Checking SW: {sw_path}")

    try:
        with open(sw_path, 'r', encoding='utf-8') as f:
            sw_content = f.read()
        response = HttpResponse(sw_content, content_type='application/javascript')
        response['Cache-Control'] = 'no-cache'
        response['Service-Worker-Allowed'] = '/'
        return response
    except FileNotFoundError:
        print(f"[PWA] ❌ SW not found at: {sw_path}")
        return HttpResponse('// service worker not found', status=404, content_type='application/javascript')
