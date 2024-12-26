from django import forms


class UserRegistrationForm(forms.Form):
    """Форма для регистрации пользователя"""
    phone_number = forms.CharField(label="Номер телефона")
    password = forms.CharField(widget=forms.PasswordInput, label="Введите пароль")
    password2 = forms.CharField(widget=forms.PasswordInput, label="Повторить пароль")

class LoginForm(forms.Form):
    """Войти по номеру телефона и паролю"""
    phone_number = forms.CharField(label="Номер телефона")
    password = forms.CharField(widget=forms.PasswordInput, label="Пароль")

class ImageForm(forms.Form):
    """Загрузка изображения"""
    image = forms.ImageField(label='Картинка')

