from django.shortcuts import render

# Create your views here.
# views.py in url_shortener app
from django.shortcuts import get_object_or_404, redirect
from .models import ShortenedURL
from django.contrib.auth.decorators import login_required,user_passes_test

@login_required
def Dashboard(request):
    print(request.user, " request")
    return render(request,'management/dashboard.html')

def redirect_view(request, short_key):
    shortened_url = get_object_or_404(ShortenedURL, short_key=short_key)
    shortened_url.click_count += 1
    shortened_url.save()
    return redirect(shortened_url.long_url)
