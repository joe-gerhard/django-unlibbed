from django.shortcuts import render, redirect
from .models import Template, Madlib
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (
    CreateView,
    ListView,
    DetailView,
    UpdateView,
    DeleteView
)

def home(request):
    return render(request, 'main_app/home.html')

class TemplateListView(LoginRequiredMixin, ListView):
    queryset = Template.objects.all()

class TemplateDetailView(LoginRequiredMixin, DetailView):
    queryset = Template.objects.all()

@login_required
def madlib_new_view(request):
    templates = Template.objects.all()
    return render(request, 'main_app/madlib_new.html', {
        'templates': templates,
    })

@login_required
def madlib_create(request, template_id):
    if request.method == 'POST':
        print(request.POST)
    template = Template.objects.get(id=template_id)
    return render(request, 'main_app/madlib_create.html', {
        'template': template,
    })

class MadlibListView(LoginRequiredMixin, ListView):
    queryset = Madlib.objects.all()

def signup(request):
    error_message = ''
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('madlibs')
        else:
            error_message = 'Invalid sign up - try again'
    form = UserCreationForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'registration/signup.html', context)

