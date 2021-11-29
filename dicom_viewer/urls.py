from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static
from account.views import (
    registration_view,
    docAppl_view
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls')),
    path('dataBase', views.dataBase, name='dataBase'),
    path('viewer', views.viewer, name='viewer'),
]
