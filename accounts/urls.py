from django.urls import path
from .views import (dashboard, 
                    team_members, 
                    profile, 
                    create_team, 
                    leave_team,
                    membership_request,
                    cancel_request,
                    accept_request,
                    remove_request,
                    search_users)

urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('team/', team_members, name='team-members'),
    path('<str:username>/profile/', profile, name='profile'),
    path('team/create', create_team, name='create-team'),
    path('team/leave', leave_team, name='leave-team'),
    path('team/membership', membership_request, name='membership-request'),
    path('team/cancel-request', cancel_request, name='cancel-request'),
    path('team/accept-request', accept_request, name='accept-request'),
    path('team/remove-request', remove_request, name='remove-request'),
    path('team/search-users', search_users, name='search-users'),
]