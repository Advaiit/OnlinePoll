from django.urls import path
from django.urls import include
from django.urls import re_path
from BaseApp import views

app_name = 'base_app'

urlpatterns = [
    path('', views.HomeView.as_view()),
    path('home/', views.HomeView.as_view(), name='Home'),
    path('poll_search/', views.PollSearch.as_view(), name='poll_search'),
    path('poll_list/', views.PollList.as_view(), name='poll_list'),
    path('poll_list/<str:question_topic>', views.PollList.as_view(), name='poll_list'),
    path('poll/<int:question_id>/', views.PollView.as_view(), name='poll'),
    path('add_poll/', views.AddPollView.as_view(), name='add_poll'),
    path('profile/', views.Profile.as_view(), name='Profile'),
    path('user_login/', views.user_login, name="user_login"),
    path('user_logout/', views.user_logout, name="user_logout"),
    path('user_register/', views.register, name="user_register")
]
