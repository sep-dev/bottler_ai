from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .forms import PhotoForm
from .models import Photo

# indexへのアクセス
def index(request):
    template = loader.get_template('bottler/index.html')
    context = {'form':PhotoForm()}
    return HttpResponse(template.render(context, request))
    # return HttpResponse("Hello World!")

def predict(request):
    if not request.method == 'POST':
        return
        redirect('bottler:index')
    form = PhotoForm(request.POST, request.FILES)
    if not form.is_valid():
        raise ValueError('Formが不正です')

    photo = Photo(image=form.cleaned_data['image'])
    predicted, percentage = photo.predict()

    template = loader.get_template('bottler/result.html')

    # context = {
    #     'photo_name': photo.image.name,
    #     'photo_data': photo.image_src(),
    #     'predicted': predicted,
    #     'percentage': percentage,
    # }
    context = {
        'photo_name': 'StabName',
        'photo_data': 'https://www.google.com/images/branding/googlelogo/2x/googlelogo_color_92x30dp.png',
        'predicted': 'OK',
        'percentage': '80',
    }

    return HttpResponse(template.render(context, request))

def hello(request):
    return HttpResponse("Hello World!")
