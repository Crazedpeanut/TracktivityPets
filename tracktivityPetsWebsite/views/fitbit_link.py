from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponse
from tracktivityPetsWebsite import utils
from django.shortcuts import redirect 
from django.core.urlresolvers import reverse


@login_required
def fitbit_link(request):
	'''
	The fitbit_link method renders the fitbit_link template and returns it to the user.
	This page is to direct the user to the Fitbit authorisation page so Tracktivity Pets
	can access their Fitbit Data.
	'''

    fitbit_link_link = '/fitbit/login'
    if utils.is_fitbit_linked(request.user):
        return redirect('tracktivityPetsWebsite:dashboard')
    
    if request.user.profile.current_pet is not None:
        redirect_to = reverse('tracktivityPetsWebsite:dashboard')
    else:
        redirect_to = reverse('tracktivityPetsWebsite:main_story')
    
    return render(request, 'tracktivityPetsWebsite/fitbit/fitbit_link.html', {"fitbit_link_link": fitbit_link_link, 'redirect_to': redirect_to})