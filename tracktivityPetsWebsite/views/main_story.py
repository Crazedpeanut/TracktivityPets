from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse

@login_required
def main_story(request):
    pet_selection_link = reverse('tracktivityPetsWebsite:pet_selection')
    has_pet = request.user.profile.current_pet is not None
    return render(request, 'tracktivityPetsWebsite/main_story.html', { "pet_selection_link": pet_selection_link, "has_pet": has_pet})