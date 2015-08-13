from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponse

@login_required
def challenges(request):
    return render(request, 'tracktivityPetsWebsite/challenges/challenges.html')