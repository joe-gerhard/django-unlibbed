from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('template/', views.TemplateListView.as_view(), name='template_index'),
    path('template/<int:pk>', views.TemplateDetailView.as_view(), name="template_detail"),
]