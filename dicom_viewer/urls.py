from django.contrib import admin
from django.urls import path, include
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
    path('dataBase/<str:slide_id>/', DataBase.as_view(), name='dataBase'),
    path('dataBaseAll',dataBaseAll,name='dataBaseAll'),
    path('viewer/<str:slide_id>/', Viewer.as_view(), name="viewer"),    
    path('upload', upload, name='upload'),
    path('uploadInfo/<int:pk>',uploadInfo, name='unploadInfo'),
    path('analysis', views.analysis, name='analysis'),
    path('deleteDicom/<pk>', deleteDicom, name='deleteDicom'),
    path('accept/<int:slide_id>',accept_view, name = 'accept'),
    path('decline/<int:slide_id>',decline_view,name='decline'),
]



if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)