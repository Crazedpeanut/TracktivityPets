from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponse
from tracktivityPetsWebsite.models import MicroChallenge, MicroChallengeGoal, MicroChallengeMedal,\
    UserMicroChallenge, UserMicroChallengeState, MicroChallengeState, UserMicroChallengeGoalStatus
from django.core import serializers
import datetime
import json

@login_required
def challenges(request):
    '''
    The challenges method renders the challenges template and corresponding sub-templates
    then returns them to the user.
    '''
	
    return render(request, 'tracktivityPetsWebsite/challenges/challenges.html')

@login_required
def get_available_challenge_names(request):
    '''
    The get_available_challenge_names gets the names of the available challenges
    for the logged in user.
	
    This list is then returned in JSON format.
    '''

    challenges = list(MicroChallenge.objects.all())
    new_chal_list = []
    current_challenges = UserMicroChallenge.objects.filter(profile=request.user.profile)

    for c in challenges:
        for cc in current_challenges:
            if c is not cc.micro_challenge:
                new_chal_list.append(c)

    return HttpResponse((serializers.serialize("json", challenges)), content_type="application/json")

@login_required
def get_challenge_details(request, challenge_pk):
    '''
    The get_challenge_details method gets the details of a MicroChallenge 
    based on its primary key, passed in with the get request.
	
    The details are then returned in JSON format.
    '''
	
    challenge = MicroChallenge.objects.get(pk=challenge_pk)

    challenge_response = {
        'name':challenge.name,
        'overview':challenge.overview,
    }

    goals_list = []
    goals = list(MicroChallengeGoal.objects.filter(micro_challenge=challenge))

    for g in goals:
        goals_list.append({
            'description':g.description,
            'pet_pennies':g.pet_pennies_reward,
            'medal':g.medal.name
        })

    response = {
        'challenge':challenge_response,
        'goals':goals_list
    }

    response_json = json.dumps(response)

    return HttpResponse( response_json, content_type="application/json")

@login_required
def get_active_challenge_details(request, user_challenge_pk):
    '''
    The get_active_challenge_details method gets the details of an incomplete UserMicroChallenge 
    based on its primary key, passed in with the get request.
	
    The details are then returned in JSON format.
    '''

    uc = UserMicroChallenge.objects.get(pk=user_challenge_pk)

    challenge = uc.micro_challenge

    challenge_response = {
        'name':challenge.name,
        'overview':challenge.overview,
        'date_started':uc.date_started.strftime("%d-%m-%Y %H:%M:%S"),
        'date_end':uc.date_end.strftime("%d-%m-%Y %H:%M:%S")
    }

    goals_list = []
    goals = list(MicroChallengeGoal.objects.filter(micro_challenge=challenge))

    for g in goals:
        goals_list.append({
            'description':g.description,
            'pet_pennies':g.pet_pennies_reward,
            'medal':g.medal.name
        })

    response = {
        'challenge':challenge_response,
        'goals':goals_list,
        'current_steps':uc.state.state.steps
    }

    response_json = json.dumps(response)

    return HttpResponse( response_json, content_type="application/json")

@login_required
def get_complete_challenge_details(request, user_challenge_pk):
    '''
    The get_complete_challenge_details method gets the details of a complete UserMicroChallenge 
    based on its primary key, passed in with the get request.
	
    The details are then returned in JSON format.
    '''

    uc = UserMicroChallenge.objects.get(pk=user_challenge_pk)
    completed_goals = []

    challenge = uc.micro_challenge

    challenge_response = {
        'name':challenge.name,
        'overview':challenge.overview,
    }

    goals_list = []
    goals = list(MicroChallengeGoal.objects.filter(micro_challenge=challenge))

    for g in goals:
        chal_goal_stat = UserMicroChallengeGoalStatus.objects.get(micro_chal_goal=g, user_micro_chal=uc)
        if(chal_goal_stat.complete is True):
            completed_goals.append(g)

    for g in completed_goals:
        goals_list.append({
            'description':g.description,
            'pet_pennies':g.pet_pennies_reward,
            'medal':g.medal.name
        })

    response = {
        'challenge':challenge_response,
        'goals':goals_list,
        'steps_taken':uc.state.state.steps,
        'date_completed':uc.date_completed.strftime("%d-%m-%Y %H:%M:%S"),
    }

    response_json = json.dumps(response)

    return HttpResponse(response_json, content_type="application/json")

@login_required
def get_active_challenge_names(request):
    '''
    The get_active_challenge_names gets a list of all of the incomplete UserMicroChallenges
    for the logged in user.
	
    The list is then returned in JSON format.
    '''

    user_challenges = UserMicroChallenge.objects.filter(profile=request.user.profile, complete=False)
    challenge_names = []

    for uc in user_challenges:
        challenge_names.append({'pk':uc.pk, 'name':uc.micro_challenge.name})

    return HttpResponse(json.dumps(challenge_names), content_type="json/application")

@login_required
def get_completed_challenge_names(request):
    '''
    The get_completed_challenge_names gets a list of all of the complete UserMicroChallenges
    for the logged in user.
	
    The list is then returned in JSON format.
    '''
	
    user_challenges = UserMicroChallenge.objects.filter(profile=request.user.profile, complete=True)
    challenge_names = []

    for uc in user_challenges:
        challenge_names.append({'pk':uc.pk, 'name':uc.micro_challenge.name})

    return HttpResponse(json.dumps(challenge_names), content_type="json/application")

@login_required
def accept_challenge(request, challenge_pk):
    '''
    The accept_challenge method creates an incomplete UserMicroChallenge based on the challenge_pk passed in by the user in
    the GET request.
    '''
	
    micro_chal = MicroChallenge.objects.get(pk=challenge_pk)

    chal_state = MicroChallengeState(steps=0)
    chal_state.save()

    user_chal_state = UserMicroChallengeState()
    user_chal_state.state = chal_state
    user_chal_state.save()

    date_end = datetime.datetime.now() + datetime.timedelta(minutes=micro_chal.duration_mins)
    user_chal = UserMicroChallenge(state=user_chal_state, micro_challenge=micro_chal,profile=request.user.profile, date_end=date_end)
    user_chal.save()

    for g in MicroChallengeGoal.objects.filter(micro_challenge=micro_chal):
        user_micro_chal_goal_status = UserMicroChallengeGoalStatus(micro_chal_goal=g, user_micro_chal=user_chal, complete=False)
        user_micro_chal_goal_status.save()

    return HttpResponse()
