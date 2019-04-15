import random

from django.shortcuts import render, redirect
# Import ToDo model class defined in current models.py file.
from django.core.files.storage import FileSystemStorage
from urllib.parse import urlencode
from .core.manager import Manager
from .core.plotter import Plotter
from django.urls import reverse
from zipfile import ZipFile
import zipfile
import shutil
from django.http import HttpResponse, Http404
from django.views.decorators.csrf import csrf_exempt, csrf_protect  # Add this
from django.http import JsonResponse

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
            plotter = Plotter()

            base_url = 'prediction'
            prediction, values = manager.predict(fs.path(upload_file.name))  # 2 category=42
            bar = plotter.prediction_bar_plot(values, upload_file.name)
            mfcc_path = plotter.save_mfcc(fs.path(upload_file.name), upload_file.name)
            url = '{}/{}/{}/{}'.format(base_url, prediction, mfcc_path, bar)
            return redirect(url)
    return render(request, PROJECT_PATH + '/pages/upload.html')


@csrf_exempt
def upload_zip(request):
    if request.method == 'POST':
        upload_file = request.FILES.get('file') if request.FILES.get('file') else request.FILES.get('zip_doc')
        # form = FileUploadForm(data=request.POST, files=request.FILES)
        if upload_file and upload_file.size > 0:
            is_valid_zip = zipfile.is_zipfile(upload_file)
            if is_valid_zip:
                request_id = random.randint(1,100001)
                with ZipFile(upload_file) as zip_file:
                    names = zip_file.namelist()
                    for name in names[1:]:
                        if "__MACOSX" not in name:
                            if "DS_Store" not in name:
                                with zip_file.open(name) as f:
                                    split_name = name.split('/')
                                    name_to_store = split_name[1] if len(split_name) > 1 else name
                                    directory_to_save = str(request_id)+'/input/' + name_to_store
                                    fs = FileSystemStorage()
                                    fs.save(directory_to_save, f)
                                    manager = Manager()
                                    prediction,values = manager.predict(fs.path(directory_to_save))  # 2 category=42
                                    url_output = '{0}/output/{1}/{2}'.format(str(request_id),prediction, name_to_store)
                                    fs.save(url_output, f)
                return JsonResponse({'code': 'ok','request_id':request_id})
            return JsonResponse({'message': 'Not valid Zip File'},status=400)
        return JsonResponse({'message': 'Empty file'},status=400)


def download_zip(request):
    if request.method == 'POST':

        request_id = request.POST.get('request_id')
        output_dir = 'media/{0}/output'.format(request_id)
        shutil.make_archive('media/music', 'zip', output_dir)
        shutil.rmtree('media/{0}'.format(request_id))
        with open('media/music.zip', 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename('media/music.zip')
            response["Cache-Control"] = "must-revalidate"
            response["Pragma"] = "must-revalidate"
            response["Content-type"] = "application/bib"
            return response


def prediction(request, value, mfcc_path, bar):
    return render(request, PROJECT_PATH + '/pages/prediction.html',
                  {'value': value, 'mfcc_path': mfcc_path, 'bar': bar})


def about_us(request):
    return render(request, PROJECT_PATH + '/pages/about_us.html')
