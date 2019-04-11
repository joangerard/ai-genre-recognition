from django.shortcuts import render, redirect
# Import ToDo model class defined in current models.py file.
from .models import ToDo
from django.core.files.storage import FileSystemStorage
from urllib.parse import urlencode
from .core.manager import Manager
from django.urls import reverse

import os

# Calculate django application execute directory path.
PROJECT_PATH = os.path.realpath(os.path.dirname(__file__))

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

def prediction(request, value):
    return render(request, PROJECT_PATH + '/pages/prediction.html', {'value': value})

def about_us(request):
    return render(request, PROJECT_PATH + '/pages/about_us.html')