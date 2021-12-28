from django.contrib import admin
from django.urls import path, include, re_path
from . import views
from .views import *
from django.conf import settings
from django.conf.urls.static import static
from account.views import (
    registration_view,
    docAppl_view
)

urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    path('', include('main.urls')),
    path('dataBase/<int:slide_id>/', dataBase, name='dataBase'),
    path('dataBaseAll',dataBaseAll,name='dataBaseAll'),
    path('viewer/<str:slide_id>/', viewer, name="viewer"),    
    path('upload', upload, name='upload'),
    path('uploadEdit/<int:pk>',uploadEdit, name='unploadInfo'),
    path('uploadView/<int:pk>',uploadView, name='unploadView'),
    path('analysis', views.analysis, name='analysis'),
    path('deleteDicom/<pk>', deleteDicom, name='deleteDicom'),
    path('accept/<int:slide_id>',accept_view, name = 'accept'),
    path('decline/<int:slide_id>',decline_view,name='decline'),
    path('finish/<int:slide_id>',finish,name='finish')
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)