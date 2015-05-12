from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponse
from tracktivityPetsWebsite import utils
from django.shortcuts import redirect 
from django.core.urlresolvers import reverse


@login_required
def fitbit_link(request):
    fitbit_link_link = '/fitbit/login'
    if utils.is_fitbit_linked(request.user):
        return redirect('tracktivityPetsWebsite:dashboard')
    return render(request, 'tracktivityPetsWebsite/fitbit_link.html', {"fitbit_link_link": fitbit_link_link})