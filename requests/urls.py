from django.urls import path
from . import views

app_name = 'requests'

urlpatterns = [
    path('', views.request_list, name='request_list'),
    path('create/', views.request_create_or_edit, name='request_create'),
    path('<int:pk>/edit/', views.request_create_or_edit, name='request_edit'),
    path('<int:pk>/', views.request_detail, name='request_detail'),
    path('<int:pk>/status/<str:new_status>/', views.change_request_status, name='change_status'),
    path('export/excel/', views.export_requests_excel, name='export_excel'),
    path('<int:pk>/update-po/', views.update_po, name='update_po'),
]
