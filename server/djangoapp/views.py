# server/djangoapp/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.contrib.auth.decorators import login_required

import json

# models & forms
from .models import CarDealer, CarReview
from .forms import ReviewForm

# ---- page views ----
def home(request):
    # uses djangoapp/templates/Home.html
    return render(request, 'Home.html')


def get_dealerships(request):
    """
    Render list of dealers. Accepts optional ?state=<state> to filter.
    Uses template 'dealers.html'.
    """
    state = request.GET.get('state', '').strip()
    qs = CarDealer.objects.all().order_by('name')
    if state:
        qs = qs.filter(state__iexact=state)

    # distinct states for filter drop-down (order alphabetically)
    states = CarDealer.objects.order_by('state').values_list('state', flat=True).distinct()

    return render(request, 'dealers.html', {
        'dealers': qs,
        'states': states,
        'selected_state': state,
    })


def about(request):
    return render(request, 'about.html')


def contact(request):
    return render(request, 'contact.html')


# ---- standard login/register pages (browser forms) ----
def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username') or request.POST.get('userName')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('djangoapp:home')
        else:
            messages.error(request, 'Invalid credentials')
            return render(request, 'login.html', {})
    else:
        return render(request, 'login.html', {})


def register_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email') or ''
        first_name = request.POST.get('first_name') or ''
        last_name = request.POST.get('last_name') or ''

        if not username or not password:
            messages.error(request, 'Provide username and password')
            return render(request, 'register.html')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
            return render(request, 'register.html')

        user = User.objects.create_user(username=username, password=password, email=email)
        # save first and last name
        user.first_name = first_name
        user.last_name = last_name
        user.save()

        login(request, user)
        return redirect('djangoapp:home')

    return render(request, 'register.html')


def logout_page(request):
    logout(request)
    return redirect('djangoapp:home')


# ---- API endpoints (JSON) ----
@csrf_exempt
def login_user(request):
    """
    POST JSON { "userName": "...", "password": "..." }
    Returns JSON { "userName": "...", "status": "Authenticated" } on success
    """
    if request.method != 'POST':
        return JsonResponse({'error': 'POST required'}, status=400)
    try:
        data = json.loads(request.body)
    except Exception:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    username = data.get('userName') or data.get('username')
    password = data.get('password')
    if not username or not password:
        return JsonResponse({'error': 'username and password required'}, status=400)
    user = authenticate(username=username, password=password)
    if user is not None:
        login(request, user)
        return JsonResponse({'userName': username, 'status': 'Authenticated'})
    else:
        return JsonResponse({'userName': username, 'status': 'Failed'}, status=401)


def api_logout(request):
    logout(request)
    return JsonResponse({'status': 'logged out'})


def api_get_dealers(request):
    """
    Simple JSON API: returns a list of dealers as JSON.
    """
    dealers = CarDealer.objects.all().order_by('name')
    data = []
    for d in dealers:
        data.append({
            'id': d.id,
            'name': d.name,
            'address': d.address,
            'city': d.city,
            'state': d.state,
            'zip_code': d.zip_code,
            'phone': d.phone,
            'website': d.website,
            'created_at': getattr(d, 'created_at', None),
        })
    return JsonResponse({'dealers': data})


# ---- dealer detail + reviews ----
def dealer_detail(request, dealer_id):
    """
    Render a single dealer detail page including reviews.
    Template: dealer_detail.html
    """
    dealer = get_object_or_404(CarDealer, id=dealer_id)
    reviews = CarReview.objects.filter(dealer_id=dealer_id).order_by('-created_at')
    context = {
        'dealer': dealer,
        'reviews': reviews,
    }
    return render(request, 'dealer_detail.html', context)


@login_required
def review_dealer(request, dealer_id):
    """
    GET -> render review form (template: review.html)
    POST -> validate & save review, then redirect back to dealer detail
    """
    dealer = get_object_or_404(CarDealer, id=dealer_id)

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review_obj = form.save(commit=False)
            review_obj.dealer_id = dealer_id
            review_obj.user = request.user
            # optional sentiment analysis hook:
            # review_obj.sentiment = analyze_sentiment(review_obj.review)
            review_obj.save()
            messages.success(request, "Review posted successfully.")
            return redirect('djangoapp:dealer-detail', dealer_id=dealer_id)
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = ReviewForm()

    return render(request, 'review.html', {'form': form, 'dealer': dealer})
