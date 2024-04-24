from django.contrib import admin
from django.urls import path, include
from django.conf.urls.i18n import i18n_patterns
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('api/', include('restapi.urls')),
]
urlpatterns += i18n_patterns(
    path("", include("acl.urls")),
    path('admin/', admin.site.urls),
    path('resource/', include("resource.urls")),

)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

