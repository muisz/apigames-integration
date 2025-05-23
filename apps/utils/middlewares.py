import zoneinfo

from django.utils import timezone


class TimezoneMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        timezone_name = request.headers.get('X-Timezone', 'Asia/Jakarta')
        if timezone_name:
            timezone.activate(zoneinfo.ZoneInfo(timezone_name))
        else:
            timezone.deactivate()
        return self.get_response(request)
