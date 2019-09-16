import collections

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
    templates = Template.objects.all().order_by('name')
    completed_libs = Madlib.objects.filter(user=request.user).order_by('name')
    for lib in completed_libs:
        templates = templates.exclude(name=lib.name)
    scenes = {}
    for template in templates:
        scene_num = template.name[6]
        template.name = template.name[10:]
        if scene_num not in scenes:
            scenes[scene_num] = []
            scenes[scene_num].append(template)
        else:
            scenes[scene_num].append(template)

    ordered_scenes = collections.OrderedDict(sorted(scenes.items()))

    return render(request, 'main_app/madlib_new.html', {
        'templates': templates, 
        'scenes': ordered_scenes
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

def madlib_list_view(request):

    # variable declarations
    madlibs = Madlib.objects.filter(user=request.user).order_by('name')
    scenes = {}

    # push madlib instances into scenes dict
    for madlib in madlibs:

        # the 7th char in madlib name (i.e. "Scene 1 - Part 2")
        #                                          ^
        scene_num = madlib.name[6]

        # remove the "Scene 1 - " from madlib.name
        # so just "Part 2" remains
        madlib.name = madlib.name[10:]

        # contruct scenes dict into 
        # {<scene_num>: [<madlib object>, ...]} format
        if scene_num not in scenes:
            scenes[scene_num] = []
            scenes[scene_num].append(madlib)
        else:
            scenes[scene_num].append(madlib) 

    # sort scenes dict by scene number
    ordered_scenes = collections.OrderedDict(sorted(scenes.items()))
    
    return render(request, 'main_app/madlib_list.html', {
        "madlibs": madlibs,
        "scenes": ordered_scenes
    })

class MadlibDetailView(LoginRequiredMixin, DetailView):
    queryset = Madlib.objects.all()

@login_required
def madlib_update(request, madlib_id):
    madlib = Madlib.objects.get(id=madlib_id) 
    if request.method == 'POST':
        madlib.words = request.POST.getlist('blanks')
        madlib.save()
        return redirect('madlib_detail', pk=madlib.pk)
    template = Template.objects.get(name=madlib.name)
    return render(request, 'main_app/madlib_update.html', {
        'template': template,
    })

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

def about(request):
    return render(request, 'main_app/about.html')

