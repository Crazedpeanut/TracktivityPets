from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from tracktivityPetsWebsite.forms import RegisterForm
from tracktivityPetsWebsite import utils
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login

#from tracktivityPetsWebsite import utils #example of using utils

def register(request):
    if request.user.is_authenticated(): #if user is logged in
        return redirect('tracktivityPetsWebsite:dashboard') #go to dashboard
    
    if request.method == "GET":
        registerForm = RegisterForm()
        return render(request, 'tracktivityPetsWebsite/register.html', {'registerForm': registerForm} )
    
    if request.method == "POST":
        registerForm = RegisterForm(request.POST)
        
        if registerForm.is_valid() == False:
            return render(request, 'tracktivityPetsWebsite/register.html', {'error':'Form not valid','registerForm': registerForm} ) #Form not valid
        else:
            result = utils.register_user(registerForm=registerForm)
            if result is not None:
                return render(request, 'tracktivityPetsWebsite/register.html', {'error':result,'registerForm': registerForm} ) #Form not valid
            else:
                username = registerForm.cleaned_data['username'].lower()
                password = registerForm.cleaned_data['password'].lower()
                user = authenticate(username=username, password=password)
                login(request, user)
                return redirect('tracktivityPetsWebsite:fitbit_link')