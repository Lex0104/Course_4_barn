from django import forms
from django.forms import ModelForm

from mailings.models import Mailing, MailingRecipient, Message


class MailingRecipientForm(ModelForm):

    class Meta:
        model = MailingRecipient
        exclude = ("owner",)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["email"].widget.attrs.update({"placeholder": "Укажите email", "class": "form-control"})

        self.fields["full_name"].widget.attrs.update({"placeholder": "Укажите Ф.И.О", "class": "form-control"})

        self.fields["comment"].widget = forms.Textarea(attrs={"rows": 4})

        self.fields["comment"].widget.attrs.update(
            {"placeholder": "Комментарий к клиенту (не обязательно)", "class": "form-control"}
        )


class MessageForm(ModelForm):

    class Meta:
        model = Message
        exclude = ("owner",)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["subject"].widget.attrs.update({"placeholder": "Напишите тему письма", "class": "form-control"})

        self.fields["message"].widget.attrs.update({"placeholder": "Напишите сообщение", "class": "form-control"})


class MailingForm(ModelForm):

    class Meta:
        model = Mailing
        exclude = (
            "date_of_first_sending",
            "date_of_sending_end",
            "status",
            "owner",
            "mailing_is_working",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["message"].widget.attrs.update({"class": "form-control"})

        self.fields["recipients"].widget.attrs.update({"class": "form-control"})


class ManagerMailingForm(ModelForm):

    class Meta:
        model = Mailing
        fields = ("mailing_is_working",)