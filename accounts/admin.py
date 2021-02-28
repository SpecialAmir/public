from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model
from .forms import CustomUserCreationForm 


User = get_user_model()



class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    model = User
    list_display = ('email','is_active','is_dev','date_joined','wallet_counter','api_counter')
    list_filter = ('email', 'is_staff', 'is_active',)
    readonly_fields = ('date_joined','last_login',)
    fieldsets = (
        (None, {'fields': ('email', 'password','date_joined','last_login')}),
        ('Permissions', {'fields': ('is_staff', 'is_active','is_dev')}),
        ('Groups',{'fields':('groups',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password', 'is_staff', 'is_active','groups')}),
    )
    search_fields = ('email',)
    ordering = ('email',)




admin.site.register(User,CustomUserAdmin)
