from django.contrib import admin
from .models import PassageUser

@admin.register(PassageUser)
class PassageUserAdmin(admin.ModelAdmin):
    pass
