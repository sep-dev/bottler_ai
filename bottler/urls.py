from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

app_name ='bottler'
urlpatterns = [
    path('', views.index, name='index'),
    path('predict/', views.predict, name='predict'),
    path('recog/', views.recog, name='recog')
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
