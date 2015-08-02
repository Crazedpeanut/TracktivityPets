from django.conf.urls import patterns, include, url
from django.contrib import admin
from tracktivityPetsWebsite import views

urlpatterns = patterns('',
    #url(r'^$', 'views.home', name='home'),
    url(r'^login/$', views.user_login, name='user_login'), #ie mysite.com/login/
    url(r'^logout/$', views.user_logout, name='user_logout'), #ie mysite.com/logout/
    url(r'^register/$', views.register, name='register'), #ie mysite.com/register/
    url(r'^$', views.dashboard, name='dashboard'), #ie mysite.com
    url(r'^feedback/$', views.feedback, name='feedback'), 
    url(r'^pet_selection/$', views.pet_selection, name='pet_selection'),
    url(r'^main_story$', views.main_story, name='main_story'),
    url(r'^fitbit_link', views.fitbit_link, name='fitbit_link'),
    url(r'^store/$', views.store, name='store'),
    url(r'^inventory/$', views.inventory, name='inventory'),
    url(r'^inventory/(?P<item_index>[0-9]+)/$', views.inventory, name='inventory'),
    url(r'^view_purchased_pet/$', views.view_purchased_pet, name='view_purchased_pet'),
    url(r'^view_purchased_pet/(?P<pet_index>[0-9]+)/$', views.view_purchased_pet, name='view_purchased_pet'),
    url(r'^view_unpurchased_pet/$', views.view_unpurchased_pet, name='view_unpurchased_pet'),
    url(r'^view_unpurchased_pet/(?P<pet_index>[0-9]+)/$', views.view_unpurchased_pet, name='view_unpurchased_pet'),
    url(r'^set_current_pet/$', views.set_current_pet, name='set_current_pet'),
    url(r'^set_current_pet/(?P<pet_index>[0-9]+)/$', views.set_current_pet, name='set_current_pet'),
)
