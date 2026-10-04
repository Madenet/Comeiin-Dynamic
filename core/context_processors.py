from django.conf import settings


def site_metadata(request):
    """Expose the configured public origin to templates."""
    return {'SITE_URL': settings.SITE_URL}
