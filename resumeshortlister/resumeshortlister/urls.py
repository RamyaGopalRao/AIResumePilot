from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.conf import settings
urlpatterns = [
    path('admin/', admin.site.urls),
    path('resumeapp/', include('resumeapp.urls')),
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)