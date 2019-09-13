from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('template/', views.TemplateListView.as_view(), name='template_index'),
    path('template/<int:pk>/', views.TemplateDetailView.as_view(), name='template_detail'),
    path('madlib/new/', views.madlib_new_view, name='madlib_new'),
    path('madlib/create/<int:template_id>/', views.madlib_create, name='madlib_create'),
    path('madlib/', views.MadlibListView.as_view(), name='madlib_list'),
    path('accounts/signup', views.signup, name='signup'),
]