from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('roomin/', admin.site.urls),

    path('', include('portal.urls')),
    path('accounts/', include('accounts.urls')),
    path('rooms/', include('rooms.urls')),
    path('api/', include('api.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
