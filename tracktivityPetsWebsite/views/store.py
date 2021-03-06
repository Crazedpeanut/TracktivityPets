from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponse
from tracktivityPetsWebsite.models import Pet, Item, Scenery, Level
import json
from tracktivityPetsWebsite import utils
from django.templatetags.static import static
from django.shortcuts import redirect

@login_required
def store(request):
    '''
    The store function renders and fills in, the store templates. Once rendered, these templates are then
    returned to the user.
    '''

    if request.user.profile.current_pet is None:#take them to the page to select a pet
        return redirect('tracktivityPetsWebsite:pet_selection')

    #pet specific
    total_xp = request.user.profile.get_total_xp()
    collected_pets = request.user.profile.inventory.get_owned_pets()
    uncollected_pets = Pet.objects.exclude(id__in=[p.pet.id for p in collected_pets]) #every pet not in collected_pets
    
    unlocked_pets = {}
    locked_pets = {}
    
    default_pet_set = False
    
    for pet in uncollected_pets:
        if total_xp >= pet.experience_to_unlock:
            unlocked_pets[pet.default_name] = {}
            unlocked_pets[pet.default_name]['image'] = utils.generate_pet_image_url(pet, pet.mood_set.filter(happiness_needed=-1)[0].image_location)
            unlocked_pets[pet.default_name]['id'] = pet.id
            unlocked_pets[pet.default_name]['cost'] = pet.cost
            if not default_pet_set:
                default_pet = pet
                default_pet_set = True
        else:
            locked_pets[pet.default_name] = {}
            locked_pets[pet.default_name]['image'] = utils.generate_pet_image_url(pet, pet.mood_set.filter(happiness_needed=-1)[0].image_location) 
            locked_pets[pet.default_name]['id'] = pet.id
            if not default_pet_set:
                default_pet = pet
                default_pet_set = True
                
    details_pet = {}
    try:   
        levelOne = Level.objects.get(level=1)
        own_all_pets = False
        details_pet['name'] = default_pet.default_name
        details_pet['experience'] = default_pet.experience_to_unlock
        details_pet['story'] = default_pet.story_set.filter(level_unlocked=levelOne)[0].text
        details_pet['image'] = utils.generate_pet_image_url(default_pet, default_pet.mood_set.filter(happiness_needed=-1)[0].image_location)
        details_pet['id'] = default_pet.pk
        details_pet['cost'] = default_pet.cost
        if default_pet.experience_to_unlock > request.user.profile.get_total_xp():
            details_pet['locked'] = True
            details_pet['story'] = "This pet is locked, to unlock you need another " + str(default_pet.experience_to_unlock - request.user.profile.get_total_xp()) + " experience."
    except:
        own_all_pets = True
            
    #item specific
    current_pet_xp = request.user.profile.current_pet.get_total_experience()
    collected_items = request.user.profile.inventory.get_collected_items_for_pet(request.user.profile.current_pet.pet)
    all_other_items = Item.objects.exclude(id__in=[i.item.id for i in collected_items]) #every item not in collected_items
    uncollected_items = all_other_items.filter(belongs_to=request.user.profile.current_pet.pet)
    
    unlocked_items = {}
    locked_items = {}
    
    default_item_set = False
    
    for item in uncollected_items:
        if current_pet_xp >= item.experience_to_unlock:
            unlocked_items[item.name] = {}
            unlocked_items[item.name]['image'] = item.get_image_path()
            unlocked_items[item.name]['id'] = item.id
            unlocked_items[item.name]['cost'] = item.cost
            if not default_item_set:
                default_item = item
                default_item_set = True
        else:
            locked_items[item.name] = {}
            locked_items[item.name]['image'] = item.get_image_path() 
            locked_items[item.name]['id'] = item.id
            if not default_item_set:
                default_item = item
                default_item_set = True
       
    details_item = {}     
    try:    
        own_all_items = False
        details_item['name'] = default_item.name
        details_item['experience'] = default_item.experience_to_unlock
        details_item['description'] = default_item.description
        details_item['image'] = default_item.get_image_path()
        details_item['id'] = default_item.pk 
        details_item['cost'] = default_item.cost
        if default_item.experience_to_unlock > request.user.profile.get_total_xp():
            details_item['locked'] = True
            details_item['description'] = "This item is locked, to unlock you need another " + str(default_item.experience_to_unlock - request.user.profile.get_total_xp()) + " experience."
    except:
        own_all_items = True
        
  
    #scenery specific
    collected_scenery = request.user.profile.inventory.get_owned_scenery()
    uncollected_scenery = Scenery.objects.exclude(id__in=[s.scenery.id for s in collected_scenery]) #every scenery not in collected_scenery
    
    unlocked_scenery = {}
    locked_scenery = {}
    
    default_scenery_set = False
    for scenery in uncollected_scenery:
        if total_xp >= scenery.experience_to_unlock:
            unlocked_scenery[scenery.name] = {}
            unlocked_scenery[scenery.name]['image'] = scenery.get_image_path()
            unlocked_scenery[scenery.name]['id'] = scenery.id
            unlocked_scenery[scenery.name]['cost'] = scenery.cost
            if not default_scenery_set:
                default_scenery = scenery
                default_scenery_set = True
            
        else:
            locked_scenery[scenery.name] = {}
            locked_scenery[scenery.name]['image'] = scenery.get_image_path() 
            locked_scenery[scenery.name]['id'] = scenery.id
            locked_scenery[scenery.name]['cost'] = scenery.cost
            if not default_scenery_set:
                default_scenery = scenery
                default_scenery_set = True
                
                
    details_scenery = {}     
    try:    
        own_all_scenerys = False
        details_scenery['name'] = default_scenery.name
        details_scenery['experience'] = default_scenery.experience_to_unlock
        details_scenery['description'] = default_scenery.description
        details_scenery['image'] = default_scenery.get_image_path()
        details_scenery['id'] = default_scenery.pk
        details_scenery['cost'] = default_scenery.cost
        if default_scenery.experience_to_unlock > request.user.profile.get_total_xp():
            details_scenery['locked'] = True
            details_scenery['description'] = "This scenery is locked, to unlock you need another " + str(default_scenery.experience_to_unlock - request.user.profile.get_total_xp()) + " experience."
        
    except:
        own_all_scenerys = True
        
    current_balance = request.user.profile.total_pet_pennies
    
    
    current_mood = request.user.profile.current_pet.get_current_mood()
    start_url = static('tracktivityPetsWebsite/images')
    preview_pet_image = '{url}/pets/{name}/{location}'.format(url=start_url, name= request.user.profile.current_pet.pet, location=current_mood.image_location)
            
        
    #return HttpResponse(json.dumps(locked_scenery)) #json.dumps(locked_pets)
    #return HttpResponse(own_all_items)

    return render(request, 'tracktivityPetsWebsite/store/store.html', 
    {
        "unlocked_pets": unlocked_pets,
        "locked_pets": locked_pets,
        "unlocked_items": unlocked_items,
        "locked_items": locked_items,
        "unlocked_scenery": unlocked_scenery,
        "locked_scenery": locked_scenery,
        "own_all_pets": own_all_pets,
        "default_pet": details_pet,
        "owns_all_items": own_all_items,
        "default_item": details_item,
        "own_all_scenerys": own_all_scenerys, 
        "default_scenery": details_scenery,
        "current_balance": current_balance,
        "preview_pet_image": preview_pet_image
    })