from .models import Platform
from django.shortcuts import render, redirect
from . import forms

# platforms/views.py
from django.shortcuts import render, get_list_or_404
from .forms import ComparisonForm
from .models import Platform
from django.contrib.auth.decorators import login_required


def add_platform(request):
    if request.method == "POST":
        form = forms.PlatformForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("home")
    else:
        form = forms.PlatformForm()
    return render(request, 'forms.html', {
        "form": form
    })


def update_platform(request, p_id):
    p = Platform.objects.get(pk=p_id)
    if request.method == "POST":
        form = forms.PlatformForm(request.POST or None, request.FILES, instance=p )
        if form.is_valid():
            form.save()
            return redirect("home")
    else:
        form = forms.PlatformForm(instance=p)
    return render(request, 'forms.html', {
        "form": form
    })


def delete_platform(request, p_id):
    Platform.objects.get(pk=p_id).delete()
    return redirect("home")

@login_required(login_url='login')
def compare_properties(request):
    if request.method == "POST":
        form = ComparisonForm(request.POST)
        if form.is_valid():
            selected_properties = form.cleaned_data['properties']
            return render(request, 'compare.html', {
                'properties': selected_properties
            })
    else:
        form = ComparisonForm()

    return render(request, 'select_properties.html', {
        'form': form
    })
