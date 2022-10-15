from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterFrom
from django.contrib.auth.decorators import login_required
from .forms import UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
import os


#user Verification
# email verification
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text, DjangoUnicodeDecodeError
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.conf import settings
from django.views.generic import View


# Create your views here.


def signin(request):
    return render(request, 'users/signin.html')


def signup(request):
    return render(request, 'users/signup.html')


def password_reset(request):
    return render(request, 'users/password_reset.html')

def password_reset_done(request):
    return render(request, 'users/password_reset_done.html')


def register(request):
    if request.method == "POST":
        fullname = request.POST['fullname']
        email = request.POST['email']
        username = request.POST['username']
        password = request.POST['password']
        # mobile = request.POST['mobile']
        # companyname = request.POST['cname']
        # fname, lname = fullname.split(" ")
        print(os.environ.get('EMAIL_USER'))
        user = User.objects.create_user(username=username,
                                        email=email, password=password)
        # pro = Profile(user=user, company_name=companyname, mobile=mobile)
        # user.is_active = False
        # user.save()
        # current_site = get_current_site(request)
        # email_subject = 'Activate Your account'
        # message = render_to_string('users/activate.html',
        # {
        #     'user':user,
        #     'domain':current_site.domain,
        #     'uid':urlsafe_base64_encode(force_bytes(user.pk)),
        #     'token':default_token_generator.make_token(user),
        # })
        # email_message = EmailMessage(
        #     email_subject,
        #     message,
        #     settings.EMAIL_HOST_USER,
        #     [email]
        # )
        # email_message.send()
        # pro = Profile(user=user, company_name=companyname, mobile=mobile)
        # pro.save()
        messages.success(request, "Registered successfully. Please Login")
        # pro.save()
        return redirect('signin')
    else:
        messages.warning(request, "Error occurred. Please Try Again")
        return redirect('signup')


def auth_login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if request.POST.get('next'):
                return redirect(request.POST.get('next'))
            else:
                messages.success(request, "Logged In Successfully")
                return redirect('base')
    # return redirect('base')
    # return redirect('member')

        else:
            messages.warning(request, "Invalid Credentials. Please Try Again")
            return redirect('signin')


def user_logout(request):
    logout(request)
    messages.success(request, "Logged Out Successfully")
    return redirect('home')



class ActivateAccountView(View):
    def get(self, request, uidb64, token):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user= User.object.get(id= uid)
        except Exception as identifier:
            user=None

        if user is not None:
            user.is_active = True
            user.save()
            messages.add_message(request, messages.INFO, 'account activated successfully')
            return redirect('login')
        return render(request, 'users/activate_failed.html',{})