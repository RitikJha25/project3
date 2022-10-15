from django.core.mail import message
from django.http import request
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
#from django.forms import UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
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
# Create your views here.


def signin(request):
    return render(request, 'users/signin.html')


def signup(request):
    return render(request, 'users/signup.html')


def forgot_password(request):
    return render(request, 'users/forgot-password.html')


def register(request):
    MyMessage = ''
    if request.method == "POST":
        fullname = request.POST['fullname']
        email = request.POST['email']
        username = request.POST['username']
        password = request.POST['password']
        user_in = User.objects.get(email = email)
        user_in1 = User.objects.get(username = username)
        if 2 ==4 :
            pass
        # if user_in1:
        #     print("username ka issue")
        #     return render(request, 'users/signup.html',{'MyMessage': 'username already exists.'})
        # if user_in:
        #     print("email ka issue")
        #     return render(request, 'users/signup.html',{'MyMessage': 'email already exists please try with another email or login.'})
        else:
            print("isssue hi issue")
            user = User.objects.create_user(username=username,email=email, password=password)
            user.is_active = False
            user.save()
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
            messages.success(request, "Registered successfully. Please Login")
            return redirect('signin')
    else:
        messages.warning(request, "Error occurred. Please Try Again")
        return redirect('signup')


def auth_login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user_in = User.objects.get(username = username)
        if user_in:
            if user_in.is_active==False:
                return HttpResponse('user email not verified.')
            else:
                user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                if request.POST.get('next'):
                    return redirect(request.POST.get('next'))
                else:
                    messages.success(request, "Logged In Successfully")
                    return redirect('/landing')
                        
            else:
                messages.warning(request, "Invalid Credentials. Please Try Again")
                return redirect('signin')


def user_logout(request):
    logout(request)
    messages.success(request, "Logged Out successfully")
    return redirect('home')



# class ActivateAccountView(View):
#     def get(self, request, uidb64, token):
#         try:
#             uid = force_text(urlsafe_base64_decode(uidb64))
#             user= User.objects.get(pk = uid)
#         except Exception as identifier:
#             user=None

#         if user is not None and default_token_generator.check_token(user, token):
#             user.is_active = True
#             user.save()
#             messages.add_message(request, messages.INFO, 'account activated successfully')
#             return redirect('login')
#         return render(request, 'users/activate_failed.html',{})




def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(id = uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')