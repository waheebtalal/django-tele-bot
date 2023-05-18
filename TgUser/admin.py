from django.contrib import admin

from TgUser.models import TgProcess, TgMessageStore,TgUser

# Register your models here.

admin.site.register(TgUser)
admin.site.register(TgProcess)
admin.site.register(TgMessageStore)

