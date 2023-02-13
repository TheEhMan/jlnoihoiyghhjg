from django.contrib import admin
from django.urls import path
from . import views 
from django.contrib.auth import views as auth_views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home_page, name = "home"),
    path('funding/', views.about_page, name = "about"),
    path('collaborators/', views.collaborators_page, name = "collaborators"),
    path('research/', views.projects_page, name = "projects"),
    path('publications/', views.publications_page, name = "publications"),
    path('teaching/', views.teaching_page, name = "teaching"),
    path('team-members/', views.teammembers_page, name = "team-members"),

#################################### Heart Page ###################################

    path('heart_home/', views.heart_home, name = "heart_home"),
    path('heart_login/', views.heart_login, name = "heart_login"),
    path('heart_register/',views.heart_register, name="heart_register"),
    path('heart_logout/',views.heart_logout, name="heart_logout"),
    path('heart_form/', views.heart_form, name = "heart_form"),
    path('heart_result/',views.heart_result, name="heart_result"),

    path('reset_password/', auth_views.PasswordResetView.as_view() , name="reset_password"),
    path('reset_password_sent/',auth_views.PasswordResetDoneView.as_view() , name="reset_password_sent"),
    path('reset/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view, name="reset/<uidb64>/<token>"),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view , name="reset_password_complet"),
    
#################################### Stroke Page ###################################

    path('stroke_home/', views.stroke_home, name = "stroke_home"),
    path('stroke_login/', views.stroke_login, name = "stroke_login"),
    path('stroke_logout/', views.stroke_logout, name = "stroke_logout"),
    path('stroke_register/', views.stroke_register, name = "stroke_register"),
    path('stroke_form/', views.stroke_form, name = "stroke_form"),
    path('stroke_result/', views.stroke_result, name = "stroke_result"),


    ]

