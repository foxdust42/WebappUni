import os

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.core.files.storage import default_storage
from django.core.mail import EmailMessage
from django.http import JsonResponse, HttpResponse, HttpResponseBadRequest
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout, get_user_model
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views import View
from users.forms import LoginForm, RegisterForm, ProfileForm
from .models import Profile
from .tokens import account_activation_token


# Create your views here.


def sign_in(request):
    if request.method == 'GET':
        form = LoginForm()
        return render(request, 'users/login.html', {'form': form})

    elif request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                messages.success(request, f'Hello {username.title()}!')
                return redirect('home')

        messages.error(request, f'Invalid username or password')
        return render(request, 'users/login.html', {'form': form})


def sign_out(request):
    logout(request)
    messages.success(request, f'Logged out.')
    return redirect('home')


def register(request):
    if request.method == 'GET':
        form = RegisterForm()
        form['password2'].label = "Confirm password"
        return render(request, 'users/register.html', {'form': form})

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            new_profile = Profile(user=user)
            new_profile.save()
            if send_email_confirm(request, user):
                # login(request, user)
                return redirect('home')
            else:
                return render(request, 'users/register.html', {'form': form})
        else:
            messages.error(request, "Failed to register")
            return render(request, 'users/register.html', {'form': form})


class SelfProfileView(LoginRequiredMixin, View):
    def get(self, request):
        # self_form = UserUpdateForm(instance=request.user)
        pass


def send_email_confirm(request, user) -> bool:
    subject = 'Activate your account'
    msg = render_to_string('users/account_activation_email.html',
                           {'username': user.username,
                            'domain': get_current_site(request).domain,
                            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                            'token': account_activation_token.make_token(user),
                            'protocol': 'https' if request.is_secure() else 'http'})
    # messages.debug(request, f'{urlsafe_base64_encode(force_bytes(user.pk))}') ##Testing only
    email = EmailMessage(subject, msg, to=[user.email])
    if email.send():
        messages.success(request, f'Account created for {user.username}; Please verify your email.')
        return True
    else:
        messages.error(request, f'Couldn\'t send confirmation email. Please try again later.')
        return False


def email_confirm(request, uidb64, token):
    try:
        uid = (urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Your account has been activated')
        return redirect('login')
    else:
        messages.error(request, 'Invalid or expired activation link. Please try again.')
        return redirect('home')


@login_required
def my_profile(request):
    profile = Profile.objects.get(user=request.user)
    return render(request, 'users/profile_view.html', {'profile': profile, 'own': True, 'p_user': request.user})


@login_required
def profile_edit(request):
    profile = get_object_or_404(Profile, user=request.user)
    if request.method == 'GET':
        form = ProfileForm(initial={'profile': profile.avatar, 'description': profile.description,
                                    'public': profile.is_public, 'DateOfBirth': profile.date_of_birth, 'webpage': profile.webpage})
        return render(request, 'users/profile_edit.html', {'form': form, 'profile': profile})

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES)
        if form.is_valid():
            img = form.cleaned_data.get('profile_picture')
            if img is not None:
                default_storage.delete(profile.avatar.path)
                profile.avatar = img
            profile.description = form.cleaned_data['description']
            if profile.description == "":
                profile.description = None
            profile.is_public = form.cleaned_data['public']
            profile.date_of_birth = form.cleaned_data['DateOfBirth']
            profile.webpage = form.cleaned_data['webpage']
            print(profile.webpage)
            profile.save()
            messages.success(request, 'Profile updated successfully')
            return redirect('my_profile')
        messages.error(request, 'Failed to update profile: Invalid form')
        return render(request, 'users/profile_edit.html', {'form': form, 'profile': profile})


def user_profile(request, username):
    profile_user = get_object_or_404(User, username=username)
    profile = get_object_or_404(Profile, user=profile_user)
    if profile.is_public:
        return render(request, 'users/profile_view.html', {'own': False, 'profile': profile, 'p_user': profile_user})
    else:
        return render(request, 'users/private_profile.html')


# This is used in the ajax call in the registration form, checks for taken usernames
def username_validator(request):
    uname = request.GET.get('username', None)
    response = {
        'is_taken': User.objects.filter(username=uname).exists()
    }
    return JsonResponse(response)



