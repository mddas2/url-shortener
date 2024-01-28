from django.shortcuts import render

# Create your views here.
# views.py in url_shortener app
from django.shortcuts import get_object_or_404, redirect
from .models import ShortenedURL
from django.contrib.auth.decorators import login_required,user_passes_test
from .url_forms import ShortenedURLForm
from django.contrib import messages
from .models import ShortenedURL
from django.utils import timezone
import hashlib
import string
import random

@login_required
def Dashboard(request):
    # print(request.user, " request")

    context  = {
        'urls':ShortenedURL.objects.filter(user_id = request.user.id).order_by('-created_at')
    }
    print(context)
    return render(request,'management/dashboard.html',context)

@login_required
def create_url(request,item_id=None):
    instance = None

    # If item_id is provided, attempt to get the object from the database
    if item_id:
        instance = get_object_or_404(ShortenedURL, id=item_id)

    if request.method == 'POST':
        form = ShortenedURLForm(request.POST,instance=instance)
        if form.is_valid():
            # Save the form data to the database
            form.instance.user = request.user
           
            if request.POST.get('short_key') == '':
                form.instance.short_key = GenerateUrl(form.instance.long_url)
            else:
                if ShortenedURL.objects.filter(short_key = request.POST.get('short_key')) and item_id==None:
                    messages.error(request,"Error: custom url already exists.")
                    return redirect('user_dashboard')
                form.instance.short_key = request.POST.get('short_key')
            
            form.save()
            messages.success(request,"save successfully ..")
        else:
            print(form.errors)
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        if item_id:
            print("item id \n ",instance)
            return render(request,'management/url_update.html',{'instance':instance})
        form = ShortenedURLForm()

    return redirect('user_dashboard')
    # return render(request,'management/dashboard.html',)
    # return render(request, 'your_template.html', {'form': form})

def redirect_view(request, short_key):
    shortened_url = get_object_or_404(ShortenedURL, short_key=short_key)

    # Check if the URL has expired
    if shortened_url.expired_date and shortened_url.expired_date < timezone.now().date():
        messages.error(request," Expired Url ")
        return redirect('user_dashboard') # Customize as needed for an expired URL page

    # Update click count and redirect
    shortened_url.click_count += 1
    shortened_url.save()
    return redirect(shortened_url.long_url)


def GenerateUrl(original_url):
    # Use SHA-256 hash function to generate a unique identifier
    letters_and_digits = string.ascii_letters + string.digits
    random_string = ''.join(random.choice(letters_and_digits) for _ in range(4))
    return random_string

@login_required
def delete_url(request,id):
    obj = get_object_or_404(ShortenedURL,user = request.user, id=id)
    obj.delete()
    return redirect('user_dashboard')


