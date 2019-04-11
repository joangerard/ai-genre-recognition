from django.urls import path
# import views from local directory.
from . import views

urlpatterns = [
    # The first parameter is the url path.
    # The second parameter is the response function defined in views.py file.
    # The third parameter is the url name which will be used in html file url tag.
    # For example, in html code {% url 'to_do_list:to_do_list' %} will be mapped to url http://localhost:8000/to_do/list_all
    path('upload', views.upload, name='upload'),
    path('prediction/<value>/', views.prediction, name='prediction'),
    path('about_us', views.about_us, name='about_us'),
]