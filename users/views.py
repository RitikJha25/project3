from django.core.mail import message
from django.http import request
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
#from django.forms import UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout

from django.core.files.storage import FileSystemStorage
# email verification

from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text, DjangoUnicodeDecodeError
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.conf import settings
from django.views.generic import View
from .tokens import account_activation_token
import random
from .models import Profile
from .forms import ProfileUpdateForm
# Create your views here.




# your_app.views.py
from allauth.socialaccount.views import SignupView
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.translation import ugettext as _


class CustomSignupView(SignupView):
    http_method_names = ['get']

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        social_login_email: str = self.sociallogin.user.email
        provider: str = self.sociallogin.account.provider

        return render(request,"users/signin.html", {'mymessages':"An account already exists with this email id please login."})








def signin(request):
    if request.user.is_active:
        return redirect("/members-home")
    return render(request, 'users/signin.html', )


def signup(request):
    if request.user.is_active:
        return redirect("/members-home")

    return render(request, 'users/signup.html')


def forgot_password(request):
    if request.user.is_active:
        return redirect("/members-home")

    return render(request, 'users/forgot-password.html')

def password_reset(request):
    if request.user.is_active:
        return redirect("/members-home")

    return render(request, 'users/password_reset.html',{'mylist':mail_list})

def password_reset_done(request):
    if request.user.is_active:
        return redirect("/members-home")

    return render(request, 'users/password_reset_done.html')

from .models import ReferUser
def register(request):
    x = ReferUser()
    if request.user.is_active:
        return redirect("/members-home")

    if request.method == "POST":
        email = request.POST['email']
        username = str(request.POST['firstname']) +"_"+str(request.POST['lastname'])+str(random.randint(1,1000))
        password = request.POST['password']
        sample = User.objects.all()
        mail_list = []
        user_list = []
        for user in sample:
            mail_list.append(user.email)
            user_list.append(user.username)
        if username in user_list:
            print("username ka issue")
            return render(request, 'users/signup.html',{'messageses': 'username already exists.'})
        if email in mail_list:
            print("email ka issue")
            return render(request, 'users/signup.html',{'messageses': 'email already exists please try with another email or login.'})
        else:
            print("isssue hi issue")
            user = User.objects.create_user(username=username,email=email, password=password)
            user.is_active = True
            user.first_name = request.POST['firstname']
            user.last_name = request.POST['lastname']
            user.save()
            x.user = user
            x.referId = str(random.randint(111111,999999))
            x.refferedBy = request.POST.get('refferedBy')
            x.totalRefferals = 0
            x.save()
            if ReferUser.objects.filter(referId = x.refferedBy).exists():
                pq = ReferUser.objects.get(referId = x.refferedBy)
                pq.referId= pq.referId
                pq.refferedBy = pq.refferedBy
                pq.totalRefferals += 1
                pq.save()
            current_site = get_current_site(request)
            email_subject = 'Activate Your account'
            message = render_to_string('users/activate.html',
            {
                'user':user,
                'domain':current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user)
            })
            
            email_message = EmailMessage(
                email_subject,
                message,
                settings.EMAIL_HOST_USER,
                [email]
            )
            email_message.send()
            # pro = Profile(user=user, company_name=companyname, mobile=mobile)
            # pro.save()
            messageses = "Registration Successful. Please verify your email to signin.\nCheck your inbox and spam folder."
            return render(request, 'users/signup_confirm.html',{'messageses':str(user.first_name+" " + user.last_name)})
    else:
        messages.warning(request, "Error occurred. Please Try Again")
        return redirect('signup')

def auth_login(request):
    if request.user.is_active:
        return redirect("/members-home")

    if request.method == "POST":
        password = request.POST['password']
        #user_in = User.objects.get(username = username)
        sample = User.objects.all()
        mail_list = []
        user_list = []
        user_dict = {}
        for user in sample:
            mail_list.append(user.email)
            user_list.append(user.username)
            user_dict[user.email] = user.username
        username = user_dict.get(str(request.POST['username']))
        if username in user_list:
            user_in = User.objects.get(username = username)
            if user_in.is_active==False:
                mymessages = "Account verification pending.\nPlease check your registered email and click on the link we have sent.\n please check spam in case you don't find in inbox." 
                return render(request, 'users/signin.html',{'mymessages':mymessages})
            else:
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    login(request, user)
                    if request.POST.get('next'):
                        return redirect(request.POST.get('next'))
                    else:
                        messages.success(request, "Logged In Successfully")
                        return redirect('base')
                            
                else:
                    mymessages = "Invalid email id or password"
                    return render(request, 'users/signin.html',{'mymessages':mymessages})
        else:
            mymessages = "Invalid email id or password"
            return render(request, 'users/signin.html',{'mymessages':mymessages})
    else:
        return render(request, 'users/signin.html',{})

def user_logout(request):
    logout(request)
    messages.success(request, "Logged Out successfully")
    return redirect('/')



def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(id = uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messageses = "Thanks for verifying your Email. Please Signin."
        return render(request, 'users/signin.html',{'messageses':messageses})
        #return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')


def imgUpload(request):
    if Profile.objects.filter(user = request.user).exists():
        Profile.objects.get(user=request.user).delete()
    profile = Profile()
    form = ProfileUpdateForm(request.FILES)
    if request.method == 'POST':
        form = ProfileUpdateForm(request.FILES)
        profile.user = request.user
        profile.profilePic = request.FILES['profilePic']
        profile.save()
        message = "image uploaded successfully"
        return redirect('/members-home')
        
    else:
        message = "failed"
        form = ProfileUpdateForm()
        return render(request,'mnfapp/profile.html',{'form':form})
    return render(request,'mnfapp/profile.html',{'form':form})
    
    
    

            # script = request.FILES['upload']
            # print(script.name)
            # fs = FileSystemStorage()  
            # document_name = str(script.name)
            # document_name= document_name.replace(' ',"_")
            # filepath = os.path.join(settings.MEDIA_ROOT, document_name)




def passwordRequest(request):
    if request.method == "POST":
        email = request.POST.get('email')
        sample = User.objects.all()
        mail_list = []
        for user in sample:
            mail_list.append(user.email)
            # user_list.append(user.username)
        # if username in user_list:
        #     print("username ka issue")
        #     return render(request, 'users/signup.html',{'messageses': 'username already exists.'})
        if email not in mail_list:
            print("")
            return render(request, 'password/password_reset.html',{'messageses': 'The email id you have entered is not registered at mynextfilm.com . please enter the registered email id.'})
        else:
            current_site = get_current_site(request)
            email_subject = 'Reset Your MyNextFilm Password'
            # users = User.objects.get(email=email)
            message = render_to_string('password/password_reset_email.html',
            {
                'user':User.objects.filter(email=email),
                'domain':current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user)
            })
            email_message = EmailMessage(
                email_subject,
                message,
                settings.EMAIL_HOST_USER,
                [email]
            )
            email_message.send()
            return render(request,'password/password_reset_done.html',{'emailid':email})
    else:
        return render(request,'password/password_reset.html')
