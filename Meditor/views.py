from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
import re
from docx2pdf import convert 
from .upload import scriptUpload
from langdetect import detect
from .forms import ScriptEdit, InputText,ScriptEditor,CScriptEditor
from .models import ScriptToEdit, ConversionEditor,editor
from mnfapp.models import MNFScriptDatabase

# for Users


from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User


def save_dict():
    document = Document('F:/MNF/translations/final.docx')
    table = document.tables[0]
    data = []
    keys = None
    for i, row in enumerate(table.rows):
        text = (cell.text for cell in row.cells)
        
        if i == 0:
            keys = tuple(text)
            continue
        row_data = dict(zip(keys, text))
        data.append(row_data)
    df = pd.DataFrame(data)
    myDict = dict(zip(df.Input,df.Output1))
    return myDict

# Create your views here.
login_required(login_url = 'login')
def index(request):
    ProgressRecorder = ProgressRecorder()
    saved = False
    form = ScriptEditor(request.POST)
    MyScript = ScriptEdit()
    text = editor()
    MyURL = ""
    stra = ""
    message = ""
    filename = ""
    form3 = InputText()
    webp_list= ScriptToEdit.objects.all()
    TS_list = MNFScriptDatabase.objects.filter(user_id = request.user)
    webpp_list= editor.objects.filter(user = request.user)

    if request.method == "POST":
        #Get the posted form
        MyScript = ScriptEdit(request.POST, request.FILES)
        form = ScriptEditor(request.POST)
        if form3.is_valid():
            form3 = InputText()
            stra=form3.GET["AreaTxt"]
        if MyScript.is_valid():
            Script = ScriptToEdit()
            Script.script = MyScript.cleaned_data.get("script")
            
            if Script.script in webp_list:
                message= "File Already Exist"
            else:
                Script.save()
                saved = True
            MyURL = Script.script.url
            filename = Script.script.name
            
            if MyURL[-4:] == "docx":
                try:
                    convert("F:/MNF/project3"+MyURL, "F:/MNF/project3"+MyURL[:-4]+"pdf")
                    print("doc file uploaded")
                    stra = scriptUpload(MyURL[:-4]+"pdf")
                    print(detect(stra))
                    
                except:
                    print("some error occured")
            
            if MyURL[-3:] == "pdf":
                stra = scriptUpload(MyURL)
                print(detect(stra))
                
            form = ScriptEditor()
            
        if form.is_valid():
            text=editor(user = request.user)
            text.ScriptName = form.cleaned_data.get("ScriptName")
            text.bodyTxt=form.cleaned_data.get("bodyTxt")
            text.save()
            return HttpResponseRedirect("/scripteditor")
            
    else:
        pass
    return render(request, 'editScript.html',{'filename':filename, "form":form,'TS_list':TS_list, "form2": MyScript,"stra":stra,'web_list':webp_list,'webpp_list':webpp_list, "message":message,"form3":form3})


login_required(login_url = 'login')
def edit_Script(request, id):
    """Edit an existing post."""

    webp_list= editor.objects.filter(user= request.user)
    webpp_list= editor.objects.filter(user = request.user)
    post = editor.objects.get(id=id, user = request.user)
    st = id
    editorData = editor()
    #print(parseDict)
    editor.objects.get(id=st).delete()
    if request != 'POST':
        form = ScriptEditor(instance=post)

    else:
        form = ScriptEditor(instance=post,user = request.user, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/scripteditor")

    context = {'post': post, 'form': form,'web_list':webp_list,'webpp_list':webpp_list,}
    return render(request, 'index2.html', context)


def edit_TScript(request, id):
    stra =""
    data = MNFScriptDatabase.objects.filter(id = id)
    form = CScriptEditor(request.POST)
    for i in data:
        script_title = i.script_title
        edited = ConversionEditor.objects.filter(ScriptName = script_title)
    if edited:
        for j in edited:
            stra = j.bodyTxt
            ConversionEditor.objects.get(ScriptName = i.script_title).delete()
            ln = False
            print("data from editor")
    else:
        MyURL = i.translated_script_path
        stra = scriptUpload(MyURL)
        ln = True
        print("data from conversion")
    if request.method == 'POST':
        if form.is_valid():
            text=ConversionEditor(user = request.user)
            text.ScriptName = form.cleaned_data.get("ScriptName")
            text.bodyTxt=form.cleaned_data.get("bodyTxt")
            text.save()
            return HttpResponseRedirect("/scripteditor")
        else:
            print("problem arrived")   

    return render(request, 'index3.html',{'form':form, 'stra':stra,'ln' : ln, 'script_title': script_title})


def delete_script(request, id):
    editor.objects.get(id = id).delete()
    return HttpResponseRedirect("/scripteditor")
