from django.contrib import admin
from .models import editor, ScriptToEdit, ConversionEditor

# Register your models here.
admin.site.register(editor)
admin.site.register(ScriptToEdit)
admin.site.register(ConversionEditor)