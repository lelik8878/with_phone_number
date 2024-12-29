
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import UserRegistrationForm, LoginForm, ImageForm
from .models import User, Image
import re

def get_main_page(request):
    context = {}
    return render(request, 'main_page.html', context)

def user_registration(request):
    form = UserRegistrationForm()
    error_value = ''
    if request.method == 'POST':
        new_user = UserRegistrationForm(request.POST)
        if re.match("^((\+375|375)+([0-9]){9})$", request.POST.get('phone_number')):
            if new_user.is_valid():
                if new_user.cleaned_data.get('password') == new_user.cleaned_data.get('password2'):
                    if new_user.cleaned_data.get('phone_number').startswith('+'):
                        new_user.cleaned_data['phone_number'] = new_user.cleaned_data.get('phone_number')[1:]
                    pre_save_user = User(phone_number=new_user.cleaned_data.get('phone_number'))
                    pre_save_user.set_password(new_user.cleaned_data.get('password'))
                    pre_save_user.save()
                    messages.success(request, f'Account created for {new_user.cleaned_data["phone_number"]}')
                    return redirect('main_page')
                else:
                    error_value = 'Пароли не совпадают'
            else:
                error_value = 'Форма не валидна'
        else:
            error_value = 'Неверный формат номера телефона'

    context = {'form': form, 'error': error_value}
    return render(request, 'user_registration.html', context)


def get_login_page(request):
    form = LoginForm()
    error_value = ''
    if request.method == 'POST':
        pre_login = LoginForm(request.POST)
        if pre_login.is_valid():
            if pre_login.cleaned_data.get('phone_number').startswith('+'):
                pre_login.cleaned_data['phone_number'] = pre_login.cleaned_data.get('phone_number')[1:]
            pre_authenticate = authenticate(phone_number=pre_login.cleaned_data.get('phone_number'),
                                            password=pre_login.cleaned_data.get('password'))
            if pre_authenticate is not None:
                login(request, pre_authenticate)
                return redirect('main_page')
            else:
                error_value = 'Неверный номер телефона или пароль'
        else:
            error_value = 'Неверный номер телефона или пароль'
    context = {'form': form, 'error': error_value}
    return render(request, 'login_page.html', context)

def log_out(request):
    logout(request)
    return redirect('main_page')

def get_user_profile(request, user_id):
    print('Rabotala view ++++++++++++++++++++++')
    current_user = User.objects.get(pk=user_id)
    image_instances = Image.objects.filter(user=user_id)
    form = ImageForm()
    if request.method == 'POST':
        new_image = ImageForm(request.POST, request.FILES)
        if new_image.is_valid():
            if current_user.main_image == 'media/no_photo.png':
                current_user.main_image = new_image.cleaned_data.get('image')
                current_user.save()
                print('Rabotal redirect ------------------------')
                return render(request, 'user_profile.html', {'current_user': current_user,
                                                                                 'form': form,
                                                                                 'images': image_instances})
            else:
                pre_new_image = Image(additional_image=new_image.cleaned_data.get('image'),
                                      user=current_user)
                pre_new_image.save()
                return render(request, 'user_profile.html', {'current_user': current_user,
                                                                                 'form': form,
                                                                                 'images': image_instances})
    context = {'current_user': current_user, 'form': form, 'images': image_instances}
    return render(request, 'user_profile.html', context)

def redirect_render(request):
    if request.method == 'POST':
        new_data = request.POST.get('our_input')
        response = redirect(new_data)
        print(type(response), response)
        response.status_code = 303
        print(response.__dict__)
        return response
    return render(request, 'redirect_render.html')

def set_as_main_image(request):
    context = {}
    return redirect('user_profile', user_id=request.user.id)

def delete_image(request):
    if request.method == 'POST':
        print('rabotaet post--------------------------')
        print(request.FILES)
    # pre_delete_image = Image.objects.filter(user=request.user)
    # pre_delete_image.delete()
    return redirect('user_profile', user_id=request.user.id)
def delete_main_image(request):
    return redirect('user_profile', user_id=request.user.id)
