from django.contrib import admin
from .models import Request, RequestStatus, RequestStatusHistory

@admin.register(Request)
class RequestAdmin(admin.ModelAdmin):
    list_display = ('title', 'department', 'month', 'year', 'requester', 'approver')
    list_filter = ('department', 'month', 'year')
    search_fields = ('title', 'description')

@admin.register(RequestStatus)
class RequestStatusAdmin(admin.ModelAdmin):
    list_display = ('code', 'description')

@admin.register(RequestStatusHistory)
class RequestStatusHistoryAdmin(admin.ModelAdmin):
    list_display = ('request', 'status', 'changed_at', 'changed_by')
    list_filter = ('status',)
