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
    completed_libs = Madlib.objects.filter(user=request.user)
    for lib in completed_libs:
        templates = templates.exclude(name=lib.name)
    return render(request, 'main_app/madlib_new.html', {
        'templates': templates,
    })

@login_required
def madlib_create(request, template_id):
    if request.method == 'POST':
        madlib = Madlib(
            name = request.POST.get('name'),
            words = request.POST.getlist('blanks'),
            text = request.POST.get('text'),
            user = request.user,
        )
        madlib.save()
        return redirect('madlib_detail', pk=madlib.pk)
    template = Template.objects.get(id=template_id)
    return render(request, 'main_app/madlib_create.html', {
        'template': template,
    })

class MadlibListView(LoginRequiredMixin, ListView):
    def get_queryset(self):
        return Madlib.objects.filter(user=self.request.user)

class MadlibDetailView(LoginRequiredMixin, DetailView):
    queryset = Madlib.objects.all()

class MadlibDeleteView(LoginRequiredMixin, DeleteView):
    model = Madlib
    success_url = '/madlib/'

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

