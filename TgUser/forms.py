from django import forms
from TgUser.models import TgUser,TgProcess,TgMessageStore
from . import models


class TgUserForm(forms.ModelForm):
    class Meta:
        model = models.TgUser
        fields = [
            "username",
            "long_lim",
            "id",
            "size_lim",
            "message",
            "phone",
            "name",
        ]



class TgMessageStoreForm(forms.ModelForm):
    class Meta:
        model = models.TgMessageStore

        fields = [
            "message_text",

            "message_user_constraint",
        ]

    def __init__(self, *args, **kwargs):
        super(TgMessageStoreForm, self).__init__(*args, **kwargs)
        self.fields["message_user_constraint"].queryset = TgUser.objects.all()



class TgProcessForm(forms.ModelForm):
    class Meta:
        model = models.TgProcess

        fields = [
            "process_id",
            "start_time",
            "messege_id",
            "end_time",
            "is_run",
            "process_user_constraint",
        ]

    def __init__(self, *args, **kwargs):
        super(TgProcessForm, self).__init__(*args, **kwargs)
        self.fields["process_user_constraint"].queryset = TgUser.objects.all()

