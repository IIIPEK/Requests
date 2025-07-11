from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Department, Right, UserDepartmentRight, NotificationRole, DepartmentNotificationRecipient

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    fieldsets = UserAdmin.fieldsets # + (
    #     ('Дополнительно', {'fields': ['email']}),
    # )

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('code', 'description')
    search_fields = ('code', 'description')

@admin.register(Right)
class RightAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')

@admin.register(UserDepartmentRight)
class UserDepartmentRightAdmin(admin.ModelAdmin):
    list_display = ('user', 'department', 'right')
    list_filter = ('department', 'right')
    search_fields = ('user__username',)

@admin.register(NotificationRole)
class NotificationRoleAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')


@admin.register(DepartmentNotificationRecipient)
class DepartmentNotificationRecipientAdmin(admin.ModelAdmin):
    list_display = ('department', 'role', 'user')
    list_filter = ('department', 'role')
    search_fields = ('user__username',)

