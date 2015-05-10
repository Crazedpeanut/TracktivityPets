from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.templatetags.static import static 
import fitapp
from tracktivityPetsWebsite import utils
from django.shortcuts import redirect
import fitapp.utils
import json

@login_required
def dashboard(request):
    
    if not utils.is_fitbit_linked(request.user) or not fitapp.utils.is_integrated(request.user):
        return redirect('/fitbit/login')
    
    elif request.user.profile.current_pet is None:#take them to the page to select a pet
        return redirect('tracktivityPetsWebsite:pet_selection')
        
    success, data = utils.update_user_fitbit(request)
    
    if not success and data == 103:# :103: Fitbit authentication credentials are invalid and have been removed.
        return redirect('/fitbit/login')
        
    start_url = static('tracktivityPetsWebsite/images')
    current_mood = request.user.profile.current_pet.get_current_mood()
    phrase = request.user.profile.current_pet.get_random_current_phrase_by_mood(current_mood).text
    mood = {"phrase": phrase, "image": '{url}/pets/{name}/{location}'.format(url=start_url, name=request.user.profile.current_pet.pet, location=current_mood.image_location)} 
    
    next_level = request.user.profile.current_pet.get_next_level()
    if next_level is None:
        experience_needed = 0
    else:
        experience_needed = next_level.experience_needed
    
    age = request.user.profile.current_pet.get_age_in_days()
    
    error = ""
    
    if not success:
        error = data
        
        data = {}
        data['experience_gained'] = -1
        data['levels_gained'] = -1
        
    happiness_data = request.user.profile.current_pet.get_happiness_last_seven_days()#[25, 50, 40, 70, 10, 80, 60]#temp data
    largest_experience, experience_data = request.user.profile.current_pet.get_experience_last_seven_days()#[2500, 5000, 4000, 7000, 1000, 8000, 6000]
    experience_progress = int(round(request.user.profile.current_pet.get_total_experience() / experience_needed * 100, 0))
    happiness_today = request.user.profile.current_pet.get_todays_happiness_value()
    level_data = {"current_experience": request.user.profile.current_pet.get_total_experience(), "experience_to_next_level": experience_needed, "current_level": request.user.profile.current_pet.level.level, "progress": experience_progress} #get_current_level()
    
    pet_name = request.user.profile.current_pet.name
    
    return render(request, 'tracktivityPetsWebsite/dashboard.html',  
                  {
                   "pet_name": pet_name,
                   "happiness_graph_data": happiness_data,
                   "experience_graph_data": experience_data,
                   "happiness_today": happiness_today,
                   "largest_experience": largest_experience,
                   "mood": mood,
                   "level_data": level_data,
                   "age": age,
                   "experience_gained": data['experience_gained'],
                   "levels_gained": data['levels_gained'],
                   "error": error
                   })