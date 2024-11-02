from django.db.models import Q
from platforms.models import Platform, Bid
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from platforms.forms import SearchForm, BidForm
from django.contrib import messages
from platforms import forms


# Create your views here.

@login_required(login_url='login')
def home(request):
    platform = Platform.objects.all()
    print('>>>>>>>>>>>>',Bid.objects.filter(property = platform[0]))
    for i in platform:


        sort_by = request.GET.get('sort_by', 'title')  # Default sort by 'title'
        sort_order = request.GET.get('sort_order', 'asc')  # Default sort order is ascending

        # Determining the sort order
        if sort_order == 'desc':
            sort_by = f'-{sort_by}'
        platform = Platform.objects.all().order_by(sort_by)

    return render(request, 'home.html', {
        "platform": platform, 'platform_bids': None,
    })


def signup(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        if not (username and email and password1 and password2):
            # return HttpResponse("Please fill in all the fields")
            return redirect("signup")
        if password1 != password2:
            # return HttpResponse("Password didn't matched!")
            return redirect("signup")

        else:
            my_user = User.objects.create_user(username, email, password1)
            my_user.save()
            return redirect("home")

    return render(request, 'signup.html')


def loginPage(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('pass')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return redirect('login')
    return render(request, 'login.html')


def logoutPage(request):
    logout(request)
    return redirect('login')


def search(request):
    form = SearchForm(request.GET or None)
    results = None

    if form.is_valid():
        query = form.cleaned_data['query']

        results = Platform.objects.filter(
            Q(title__icontains=query) |
            Q(property_type__icontains=query) |
            Q(city__icontains=query) |
            Q(country__icontains=query) |
            Q(location__icontains=query) |
            Q(price__icontains=query)
        )

    return render(request, 'search.html', {
        'form': form,
        'results': results,
    })




def details(request, property_id):
    platform = get_object_or_404(Platform, pk=property_id)
    bids = platform.bids.all().select_related('user')
    return render(request, 'details.html', {
    "platform": platform,  'bids': bids,
  })




def place_bid(request, platform_id):
    platform = get_object_or_404(Platform, id=platform_id)
    if request.method == 'POST':
        form = BidForm(request.POST)
        if form.is_valid():
            bid = form.save(commit=False)
            bid.user = request.user
            bid.property = platform
            bid.save()
            messages.success(request, f'Bid of ${bid.amount} placed successfully!')
            return redirect('home')  # Redirect to the home page or other view as needed
        else:
            messages.error(request, 'There was an issue with your bid.')
    else:
        form = BidForm()

    return render(request, 'forms.html', {'form': form, 'platform': platform})

