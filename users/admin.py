from django.contrib import admin
from users.models import Permission, Role, User

    
    
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display=('username','email','role')

@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    pass

@admin.register(Permission)    
class PermissionAdmin(admin.ModelAdmin):
     list_display=['name']