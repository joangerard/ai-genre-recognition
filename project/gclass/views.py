from django.shortcuts import render, redirect
# Import ToDo model class defined in current models.py file.
from .models import ToDo
from django.core.files.storage import FileSystemStorage
from urllib.parse import urlencode
from .core.manager import Manager
from django.urls import reverse
from zipfile import ZipFile
import zipfile
import shutil
from django.http import HttpResponse, Http404

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
            prediction, values = manager.predict(fs.path(upload_file.name))  # 2 category=42
            bar = manager.prediction_bar_plot(values, upload_file.name)
            mfcc_path = manager.save_mfcc(fs.path(upload_file.name), upload_file.name)
            url = '{}/{}/{}/{}'.format(base_url, prediction, mfcc_path, bar)
            return redirect(url)
    return render(request, PROJECT_PATH + '/pages/upload.html')


def upload_zip(request):
    if request.method == 'POST':
        upload_file = request.FILES.get('document')
        if upload_file and upload_file.size > 0:
            is_valid_zip = zipfile.is_zipfile(upload_file)
            if is_valid_zip:
                with ZipFile(upload_file) as zip_file:
                    names = zip_file.namelist()
                    for name in names[1:]:
                        if "__MACOSX" not in name:
                            with zip_file.open(name) as f:
                                split_name = name.split('/')
                                name_to_store = split_name[1] if len(split_name) > 1 else name
                                fs = FileSystemStorage()
                                fs.save('input/' + name_to_store, f)
                                manager = Manager()
                                prediction = manager.predict(fs.path('input/' + name_to_store))  # 2 category=42
                                url_output = 'output/{0}/{1}'.format(prediction, name_to_store)
                                fs.save(url_output, f)

                shutil.make_archive('media/music', 'zip', 'media/output')
                with open('media/music.zip', 'rb') as fh:
                    response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
                    response['Content-Disposition'] = 'inline; filename=' + os.path.basename('media/music.zip')
                    return response
            return render(request, PROJECT_PATH + '/pages/upload.html', {'not_valid_zip': True})
    return render(request, PROJECT_PATH + '/pages/upload.html', {'not_valid_object': True})


def prediction(request, value, mfcc_path, bar):
    return render(request, PROJECT_PATH + '/pages/prediction.html',
                  {'value': value, 'mfcc_path': mfcc_path, 'bar': bar})


def about_us(request):
    return render(request, PROJECT_PATH + '/pages/about_us.html')
