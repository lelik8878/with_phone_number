import os

from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.shortcuts import render, redirect
from django.conf import settings
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
            print(new_image.cleaned_data.get('image').name)
            print(new_image.cleaned_data.get('image').size)
            print(type(new_image.cleaned_data.get('image')))
            if current_user.main_image == 'media/no_photo.png':
                current_user.main_image = new_image.cleaned_data.get('image')
                current_user.save()
                return render(request, 'user_profile.html', {'current_user': current_user,
                                                                                 'form': form,
                                                                                 'images': image_instances})
            if current_user.main_image == 'media/' + new_image.cleaned_data.get('image').name:
                messages.info(request, 'Файл существует в базе данных')
                return render(request, 'user_profile.html', {'current_user': current_user,
                                                             'form': form,
                                                             'images': image_instances})
            else:
                check_image = Image.objects.filter(additional_image='media/' + new_image.cleaned_data.get('image').name,
                                                   user=user_id)
                print(check_image)
                if check_image.exists():
                    messages.info(request, 'Файл существует в базе данных')
                    return render(request, 'user_profile.html', {'current_user': current_user,
                                                                 'form': form,
                                                                 'images': image_instances})
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
    pre_delete = User.objects.get(pk=request.user.id)
    # print(pre_delete.main_image.url)
    pre_delete.main_image = 'media/no_photo.png'
    pre_delete.save()
    return redirect('user_profile', user_id=request.user.id)

def get_data_from_form(request):
    current_user = User.objects.get(id=1)
    images = Image.objects.filter(user_id=1)
    if request.method == 'POST':
        print(request.POST)
        if request.POST['action'] == 'delete_main_image':
            path_to_delete_img = str(current_user.main_image)
            file_path = os.path.join(settings.MEDIA_ROOT, path_to_delete_img)
            print(path_to_delete_img)
            print(file_path)
            print(type(path_to_delete_img))
            if current_user.main_image == 'media/no_photo.png':
                messages.info(request, 'Главная картинка не установлена или была удалена')
                return render(request, 'get_data_from_form.html',
                      {'current_user': current_user, 'images': images})
            current_user.main_image = 'media/no_photo.png'

            current_user.save()
            if os.path.isfile(file_path):
                os.remove(file_path)
            print('Hello, Johan')
        if request.POST['action'] == 'set_as_main' and 'our_images' in request.POST:
            new_image = Image.objects.create(additional_image=current_user.main_image,
                                             user=current_user)
            current_user.main_image = images.get(pk=request.POST['our_images']).additional_image
            delete_img = images.get(pk=request.POST['our_images'])
            delete_img.delete()
            new_image.save()
            current_user.save()
            return render(request, 'get_data_from_form.html',
                          {'current_user': current_user, 'images': images})
        if request.POST['action'] == 'delete_image' and 'our_images' in request.POST:
            path_to_delete_img = str(images.get(pk=request.POST['our_images']).additional_image)
            file_path = os.path.join(settings.MEDIA_ROOT, path_to_delete_img)
            delete_img = images.get(pk=request.POST['our_images'])
            delete_img.delete()
            if os.path.isfile(file_path):
                os.remove(file_path)
            return render(request, 'get_data_from_form.html',
                          {'current_user': current_user, 'images': images})
        if request.POST['action'] == 'set_as_main' or 'delete_main_image':
            messages.info(request,"Для выполнения действия необходимо выбрать картинку")
    context = {'current_user': current_user, 'images': images}
    return render(request, 'get_data_from_form.html', context)
