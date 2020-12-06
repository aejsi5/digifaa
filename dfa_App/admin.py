from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm
from .models import User as DFA_User
from .models import *
from django.contrib.auth.models import Permission

# Register your models here.
class DFA_UserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = DFA_User


class DFA_UserAdmin(UserAdmin):
    form = DFA_UserChangeForm

    fieldsets = UserAdmin.fieldsets + (
            (None, {'fields': ('Workshop',)}),
    )

admin.site.register(Permission)
admin.site.register(DFA_User, DFA_UserAdmin)
admin.site.register(Workshop)
admin.site.register(Vehicle)
admin.site.register(Note)
admin.site.register(Recall)
admin.site.register(Constraint)
admin.site.register(Recall_Doc)
admin.site.register(Vehicle_Recall)
admin.site.register(History)
