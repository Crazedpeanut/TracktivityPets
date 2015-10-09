from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.templatetags.static import static 
import fitapp
from tracktivityPetsWebsite import utils
from tracktivityPetsWebsite.models import Pet, Item, CollectedItem, Level
from django.shortcuts import redirect
import fitapp.utils
from django.core import serializers
import json


@login_required
def view_purchased_pet(request, pet_index=""):
    '''
    The view_purchased_pet method finds the purchased pet that corresponds with the pet_index parameter.
    The details for the purchased pet are then returned back to the users browser in JSON format.
    '''
        
    if pet_index is "":
        owned_pet = request.user.profile.current_pet
        owns_pet = True
        name = owned_pet.name
    else:
        try:
            pet = Pet.objects.get(id=pet_index) #get the pet in the url
            name = pet.default_name
        except: #pet not found
            return redirect('tracktivityPetsWebsite:dashboard') #should probably reverse to take them back to page they were on?
    
        try:
            owned_pet = request.user.profile.inventory.collectedpet_set.get(pet=pet) #if user has that pet in inventory
            owns_pet = True
        except Exception as e:
            owns_pet = False

    
    if owns_pet:
        #use owned_pet, and they are unlocked
        experience = owned_pet.get_total_experience()
        level = owned_pet.level.level
        levelOne = Level.objects.get(level=1)
        current_mood = owned_pet.get_current_mood()
        image_location = current_mood.image_location
        
        details = {}
        details['name'] = owned_pet.name
        details['experience'] = experience
        details['level'] = level
        details['story'] = owned_pet.pet.story_set.filter(level_unlocked=levelOne)[0].text
        details['image'] = utils.generate_pet_image_url(owned_pet.pet, image_location)
        details['age'] = owned_pet.get_age_in_days()
        
        
        return HttpResponse(json.dumps(details))
    else:
        #use pet, and they are locked
        cost = pet.cost
        return render(request, 'tracktivityPetsWebsite/view_pet.html',  
        {
           "owns_pet": owns_pet,
           "cost": cost,
        })
