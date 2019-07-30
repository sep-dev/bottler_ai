from logging import basicConfig, getLogger, DEBUG
from django.shortcuts import redirect
from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader
from .forms import PhotoForm
from .models import Photo
from django.conf import settings
from .consts import *

import pprint
import requests
import json
import io
import os

from common import utils
from PIL import Image

basicConfig(level=DEBUG)
logger = getLogger(__name__)


def index(request):
    """
    入力フォーム画面を表示
    """
    logger.debug('index')

    template = loader.get_template('bottler/index.html')
    context = {'form': PhotoForm()}
    return HttpResponse(template.render(context, request))
    # return HttpResponse("Hello World!")


def predict(request):
    """
    画像アップロード後の結果表示画面
    """
    logger.debug('predict')

    if not request.method == 'POST':
        return redirect('bottler:index')

    form = PhotoForm(request.POST, request.FILES)
    if not form.is_valid():
        raise ValueError('Formが不正です')

    photo = Photo(image=form.cleaned_data['image'])

    # 画像ファイルをbase64で受け取る
    base64 = photo.image_src()

    # AIメーカー
    response = utils.AiMakerRequest(base64)
    result = utils.AiMakerResponse(response)

    template = loader.get_template('bottler/result.html')

    context = {
        'photo_name': 'StabName',
        'base64': base64,
        'predicted': 'OK',
        'percentage': '80',
        'state': result['state'],
        'label': result['label'],
        'score': result['score'] * 100,
    }
    # logger.debug(context)

    return HttpResponse(template.render(context, request))


def recog(request):
    """
    画像アップロード後の結果表示画面
    """
    logger.debug('recog')

    if not request.method == 'POST':
        return redirect('bottler:index')

    form = PhotoForm(request.POST, request.FILES)
    if not form.is_valid():
        raise ValueError('Formが不正です')

    model = request.POST.get('model')

    if model == '1':
        model = VISUAL_RECOGNITION_MODEL[model]
        # model = 'DefaultCustomModel_592439278'
    else:
        model = VISUAL_RECOGNITION_MODEL['0']
        # model = 'default'

    photo = Photo(image=form.cleaned_data['image'])
    photo.save()

    # file_path = photo.image.url
    file_path = photo.image.name
    file_path = settings.MEDIA_URL + file_path

    # 画像ファイルをbase64で受け取る
    base64 = Photo(image=form.cleaned_data['image'])
    base64 = base64.image_src()

    # IBM Visual Recognition (FILE)
    path = file_path.lstrip('/')
    # path = "media/images/005_1res6jA.png"
    response = utils.VisualRecognitionRequestFile(path, model)

    # IBM Visual Recognition (URL)
    # dummy = 'dummy'
    # response = utils.VisualRecognitionRequest(dummy, model)
    vr_classes = utils.VisualRecognitionResponse(response)

    template = loader.get_template('bottler/visual_recognition.html')

    photo.delete()
    # os.remove(settings.BASE_DIR + file_path)

    context = {
        'vr_classes': vr_classes,
        'file_path': file_path,
        'photo_obj': photo,
        'base64': base64,
    }
    # logger.debug(context)

    return HttpResponse(template.render(context, request))


def hello(request):
    return HttpResponse("Hello World!")
