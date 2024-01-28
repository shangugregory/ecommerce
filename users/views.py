from django.shortcuts import render, redirect 
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from . forms import UserRegistration

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit
# Create your views here.


def register(request):
    if request.method == 'POST':
        form = UserRegistration(request.POST)
        if form.is_valid():
            user = form.save()  # Save the user
            username = form.cleaned_data.get('username')
            messages.success(request, f'Your Account has been created, you can now log in')
            return redirect('login')
    else:
        form = UserRegistration()

    context = {'form': form}
    return render(request, 'users/register.html', context)
