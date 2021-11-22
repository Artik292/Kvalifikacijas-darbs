from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from account.views import (
    registration_view
)

urlpatterns = [
    path('', views.index, name='home'),
    path('register', registration_view, name='register'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
