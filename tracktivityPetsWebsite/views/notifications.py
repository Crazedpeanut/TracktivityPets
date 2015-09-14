from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponse
from tracktivityPetsWebsite.models import MicroChallenge, MicroChallengeGoal, MicroChallengeMedal, \
    UserMicroChallenge, UserMicroChallengeState, MicroChallengeState, UserMicroChallengeGoalStatus,\
    UserNotification

from django.core import serializers
import datetime

def get_acknowledged_notifications(request):
    notifications = UserNotification.objects.filter(userProfile=request.user.profile, acknowledged=False)
    return HttpResponse((serializers.serialize("json", notifications)), content_type="application/json")

def acknowledge_notification(request, notification_pk):
    notification = UserNotification.objects.filter(pk=notification_pk)
    notification.acknowledged = True
    notification.save()