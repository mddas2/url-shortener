from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, HttpResponse,redirect,get_list_or_404, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required,user_passes_test
from django.contrib import messages
from django.contrib.auth.views import PasswordResetView
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import CustomUser
from .decorators import is_admin,is_superadmin,is_user
from .forms import SignupForm
from .validation import handle_signup_validation
# from .generate_token import generate_unique_four_digit_number
# from membership.tasks import send_token_mail


def signup(request):
    """For creating regular users."""
    form = SignupForm(request.POST or None)
    if request.method=='POST':
        if form.is_valid():
            email = form.cleaned_data['email'].lower()
            phone = str(form.cleaned_data['phone_number'])
            if not handle_signup_validation(request, email, phone):
                return redirect('account:signup')
            User = get_user_model()
            # new_user=User.objects.create_user(token=str(generate_unique_four_digit_number()),
                                    #  **form.cleaned_data)
            subject="Verify your account."
            # message=f"Your pin is {new_user.token}. Login with your new account and enter this pin to verify."
            # send_token_mail(new_user.email,subject,message)s
            messages.success(request,"Account created Successfully. Login Now.")
            return redirect(reverse('account:login_user'))  
        else:
            #messages.error(request, 'User not created! Please fill the form with correct data!')
            pass
    else:
        pass
    context={
        'form':form
    }
    return render(request, 'account/signup.html',context)

#Activate user Email Verification
# def activate(request):

def login_user(request):
    if(request.method == 'POST'):
        email=request.POST['email']
        password=request.POST['password']
        user=authenticate(request,username=email, password=password)
        if user is not None:
            login(request,user)
            return redirect(reverse('user_dashboard'))
        else:
            messages.error(request, 'Incorrect Username or Password!')
            return redirect('account:login_user')
    else:
        return render(request,'account/login.html')

@login_required
def logout_user(request):
    logout(request)
    return redirect(reverse('user_dashboard'))

class CustomPasswordResetView(PasswordResetView):
    """
    Customizing the django default passwordresetview to check if users email exist in
    database before sending mail
    """
    def form_valid(self, form):
        email = form.cleaned_data["email"]
        # Check if the email exists in the database
        if not CustomUser.objects.filter(email=email).exists():
            messages.error(self.request, "Email does not exist.")
            return self.form_invalid(form)
        return super().form_valid(form) 



