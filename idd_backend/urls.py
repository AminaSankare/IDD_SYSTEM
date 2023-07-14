from django.contrib import admin
from django.urls import include, path

from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from . import settings


urlpatterns = [
    # path('', include('management.urls')),
    path('admin/', admin.site.urls),
]
urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


# THE FOLLOWING FUNCTION WILL HELP US TO HANDLE THE UNVAILABLE LINK OR WEB PAGE
handler404 = "management.views.handle_not_found"


# Configure Admin Title
admin.site.site_header = "INDIVIDUAL DESCRIPTIVE DOCUMENT ACQUISITION SYSTEM"
admin.site.index_title = "MANAGEMENT"
admin.site.site_title = "Control Panel"
