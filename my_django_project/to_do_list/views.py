from zipfile import ZipFile
import shutil

from django.shortcuts import render, redirect
# Import ToDo model class defined in current models.py file.
from .models import ToDo
from django.core.files.storage import FileSystemStorage
from urllib.parse import urlencode
from .Core.manager import Manager
from django.urls import reverse
from django.http import HttpResponse, Http404

import os

# Calculate django application execute directory path.
PROJECT_PATH = os.path.realpath(os.path.dirname(__file__))

# This function will return and render the home page when url is http://localhost:8000/to_do/.
def home(request):
    # Get the index template file absolute path.
    index_file_path = PROJECT_PATH + '/pages/home.html'

    # Return the index file to client.
    return render(request, index_file_path)

def upload(request):
    if request.method == 'POST':
        upload_file = request.FILES.get('document')
        if upload_file and upload_file.size > 0:
            fs = FileSystemStorage()
            fs.save(upload_file.name, upload_file)
            manager = Manager()

            base_url = 'prediction'
            prediction = manager.predict(fs.path(upload_file.name)) # 2 category=42
            url = '{}/{}'.format(base_url, prediction)
            return redirect(url)
    return render(request, PROJECT_PATH + '/pages/upload.html')

def upload_zip(request):
    if request.method == 'POST':
        upload_file = request.FILES.get('document')
        with ZipFile(upload_file) as zip_file:
            names = zip_file.namelist()

            for name in names[1:]:
                if "__MACOSX" not in name:
                    with zip_file.open(name) as f:
                        split_name = name.split('/')
                        name_to_store = split_name[1] if len(split_name) > 1 else name
                        fs = FileSystemStorage()
                        fs.save('input/'+name_to_store, f)
                        manager = Manager()
                        prediction = manager.predict(fs.path('input/'+name_to_store)) # 2 category=42
                        url_output = 'output/{0}/{1}'.format(prediction,name_to_store)
                        fs.save(url_output, f)

        shutil.make_archive('media/music', 'zip', 'media/output')
        with open('media/music.zip', 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename('media/music.zip')
            return response
    return render('', PROJECT_PATH + '/pages/upload.html')

def prediction(request, value):
    return render(request, PROJECT_PATH + '/pages/prediction.html', {'value': value})

def about_us(request):
    return render(request, PROJECT_PATH + '/pages/about_us.html')

# This function will display todos in a list page the request url is http://localhost:8000/to_do/list_all.
def to_do_list(request):
    # Get all todos model object order by handle_date column.
    todos = ToDo.objects.order_by('handle_date')

    # Add the todos list in Django context.
    context = {'todos' : todos}

    # Get the list page absolute path.
    to_do_list_file_path = PROJECT_PATH + '/pages/list.html'

    # Render and return to the list page.
    return render(request, to_do_list_file_path, context)

# Display the todo detail information in web page. The input parameter is todo id. The request url is http://localhost:8000/to_do/show_detail/3/.
def to_do_detail(request, id):

    # Get todo object by id.
    todo = ToDo.objects.get(id=id)

    # Set the todo object in context.
    context = {'todo' : todo}

    # Get todo detail page absolute file path.
    to_do_detail_file_path = PROJECT_PATH + '/pages/detail.html'

    # Return the todo detail page.
    return render(request, to_do_detail_file_path, context)
