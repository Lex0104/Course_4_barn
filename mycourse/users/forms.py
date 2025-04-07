from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm

from users.models import User


class UserRegisterForm(UserCreationForm):
    usable_password = None

    class Meta:
        model = User
        fields = ("email", "password1", "password2")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["email"].widget.attrs.update({"placeholder": "Укажите ваш email", "class": "form-control"})

        self.fields["password1"].widget.attrs.update({"placeholder": "Создайте пароль", "class": "form-control"})

        self.fields["password2"].widget.attrs.update({"placeholder": "Повторите пароль", "class": "form-control"})


class UserForm(ModelForm):

    class Meta:
        model = User
        fields = (
            "avatar",
            "phone_number",
            "country",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["avatar"].widget.attrs.update({"class": "form-control"})

        self.fields["phone_number"].widget.attrs.update(
            {"placeholder": "Введите номер телефона", "class": "form-control"}
        )

        self.fields["country"].widget.attrs.update({"placeholder": "Укажите страну", "class": "form-control"})


class ManagerForm(ModelForm):

    class Meta:
        model = User
        fields = ("is_active",)