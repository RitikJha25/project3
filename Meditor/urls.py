from django.contrib import admin
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('',views.index),
    path('/editSavedScript/<int:id>', views.edit_Script),
    path('/editTranslatedScript/<int:id>', views.edit_TScript),
    path('/<int:id>', views.delete_script)
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

