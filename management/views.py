from django.shortcuts import render

# Create your views here.
# views.py in url_shortener app
from django.shortcuts import get_object_or_404, redirect
from .models import ShortenedURL
from django.contrib.auth.decorators import login_required,user_passes_test
from .url_forms import ShortenedURLForm
from django.contrib import messages
from .models import ShortenedURL

import hashlib
import string

@login_required
def Dashboard(request):
    # print(request.user, " request")
    print(ShortenedURL.objects.filter(user_id = request.user.id))
    context  = {
        'urls':ShortenedURL.objects.filter(user_id = request.user.id)
    }
    print(context)
    return render(request,'management/dashboard.html',context)

def create_url(request):
    if request.method == 'POST':
        form = ShortenedURLForm(request.POST)
        if form.is_valid():
            # Save the form data to the database
            form.instance.user = request.user
            form.instance.short_key = GenerateUrl(form.instance.long_url)
            form.save()
            messages.success(request,"save successfully ..")
        else:
            print(form.errors)
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = ShortenedURLForm()

    return redirect('user_dashboard')
    # return render(request,'management/dashboard.html',)
    # return render(request, 'your_template.html', {'form': form})


def redirect_view(request, short_key):
    shortened_url = get_object_or_404(ShortenedURL, short_key=short_key)
    shortened_url.click_count += 1
    shortened_url.save()
    return redirect(shortened_url.long_url)

def GenerateUrl(original_url):
    # Use SHA-256 hash function to generate a unique identifier
    hash_object = hashlib.sha256(original_url.encode())
    hashed_url = hash_object.hexdigest()

    # Convert the hashed URL to a numeric identifier
    numeric_identifier = int(hashed_url, 16)

    # Base62 encoding
    characters = string.digits + string.ascii_uppercase + string.ascii_lowercase
    base = len(characters)

    if numeric_identifier == 0:
        return characters[0]

    result = ''
    while numeric_identifier:
        numeric_identifier, remainder = divmod(numeric_identifier, base)
        result = characters[remainder] + result

    return result

