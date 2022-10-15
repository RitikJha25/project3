from django import forms
from .models import editor, FeedBack, ConversionEditor
from tinymce.models import HTMLField
from tinymce.widgets import TinyMCE
class ScriptEditor(forms.ModelForm):
    ScriptName = forms.CharField(max_length=50)
    bodyTxt = forms.CharField(widget=TinyMCE(attrs={'cols': 30, 'rows': 30 ,'style': 'text-align:right;'}))
    class Meta:
        model = editor
        fields = ["ScriptName","bodyTxt"]


class CScriptEditor(forms.ModelForm):
    ScriptName = forms.CharField(max_length=50)
    bodyTxt = forms.CharField(widget=TinyMCE(attrs={'cols': 30, 'rows': 30 ,'style': 'text-align:right;'}))
    class Meta:
        model = ConversionEditor
        fields = ["ScriptName","bodyTxt"]




class ScriptEdit(forms.Form):
   script = forms.FileField()

class InputText(forms.Form):
    mySavedName = forms.CharField(max_length=50)
    AreaTxt = forms.CharField(widget=forms.Textarea)
