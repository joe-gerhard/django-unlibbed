from django.shortcuts import render
from .models import User, Template, Madlib
from django.views.generic import (
    CreateView,
    ListView,
    DetailView,
    UpdateView,
    DeleteView
)

def home(request):
    return render(request, 'main_app/home.html')

class TemplateListView(ListView):
    queryset = Template.objects.all()

class TemplateDetailView(DetailView):
    queryset = Template.objects.all()

class MadlibCreateView(CreateView):
    model = Madlib
    fields = '__all__'
