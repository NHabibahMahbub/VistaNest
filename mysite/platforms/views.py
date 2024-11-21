from .models import Platform
from django.shortcuts import render, redirect, get_list_or_404, get_object_or_404
from . import forms
from .models import Platform
from django.contrib.auth.decorators import login_required
from .forms import ComparisonForm


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
        form = forms.PlatformForm(request.POST or None, request.FILES, instance=p)
        if form.is_valid():
            form.save()
            return redirect("home")
    else:
        form = forms.PlatformForm(instance=p)
    return render(request, 'forms.html', {
        "form": form
    })


def delete_platform(request, p_id):
    platform = get_object_or_404(Platform, pk=p_id)
    if request.method == "POST":
        platform.delete()
        return redirect("home")
    return render(request, "delete.html", {"cat": platform})



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
