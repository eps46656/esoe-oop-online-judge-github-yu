from django.conf.urls import url

from . import views
from django.urls import path


app_name = 'judge'

urlpatterns = [
    path('',
         views.index,
         name='index'),

    path('login/',
         views.login,
         name='login'),

    path('logout/',
         views.logout,
         name='logout'),

    path('problems/',
         views.problem_list,
         name='problem_list'),

    path('problems/<str:pk>/',
         views.problem_detail,
         name='problem_detail'),

    path('profile/',
         views.profile,
         name='profile'),

    path('submissions/<str:pk>/',
         views.submission_detail,
         name='submission_detail'),
]
