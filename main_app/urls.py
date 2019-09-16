from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('template/about', views.about, name='about'),
    path('template/', views.TemplateListView.as_view(), name='template_index'),
    path('template/<int:pk>/', views.TemplateDetailView.as_view(), name='template_detail'),
    path('madlib/new/', views.madlib_new_view, name='madlib_new'),
    path('madlib/create/<int:template_id>/', views.madlib_create, name='madlib_create'),
    path('madlib/', views.madlib_list_view, name='madlib_list'),
    path('madlib/<int:pk>/', views.MadlibDetailView.as_view(), name='madlib_detail'),
    path('madlib/<int:madlib_id>/update/', views.madlib_update, name='madlib_update'),
    path('madlib/<int:pk>/delete/', views.MadlibDeleteView.as_view(), name='madlib_delete'),
    path('accounts/signup', views.signup, name='signup'),
]