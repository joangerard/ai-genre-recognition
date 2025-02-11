from django.contrib import admin
from django.urls import include, path
from django.conf.urls import url
from django.conf.urls.static import static
from django.conf import settings
from django.views.generic.base import RedirectView

urlpatterns = [

    path('', RedirectView.as_view(pattern_name='gclass:upload')),
    # When request http://localhost:8000/admin/, it will use url mappings defined in admin.site.urls.py file
    path('admin/', admin.site.urls),

    # When request http://localhost:8000/to_do, it will use url mappings defined in to_do_list.urls.py file
    # The include function must contains a tuple and a namespace key value pair. 
    # The tuple first element is the app urls mapping file, the second element is the application name.
    # If do not provide the application name, it will throw Specifying a namespace in include() without providing an app_name is not supported error.
    url('^gclass/', include(('gclass.urls', 'gclass'), namespace='gclass'))
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root= settings.MEDIA_ROOT)