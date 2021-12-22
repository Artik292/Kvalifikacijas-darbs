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
    path('dataBase', views.dataBase, name='dataBase'),
    path('viewer/<str:slide_id>/', Viewer.as_view(), name="viewer"),    
    path('upload', upload, name='upload'),
    path('uploadInfo/<int:pk>',uploadInfo, name='unploadInfo'),
    path('analysis', views.analysis, name='analysis'),
    path('deleteDicom/<pk>', deleteDicom, name='deleteDicom')
]



if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)