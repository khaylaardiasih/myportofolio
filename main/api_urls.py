from django.urls import path
from rest_framework.authtoken import views as authtoken_views

from main.api_views import (
    skill_list,
    skill_detail,
    skill_star,
    experience_list,
    experience_detail,
    api_logout,
    project_list,
    project_detail,
)

app_name = "api"

urlpatterns = [
    # Auth Token Endpoints (Tutorial 10)
    path("auth/token/", authtoken_views.obtain_auth_token, name="api_token_auth"),
    path("auth/logout/", api_logout, name="api_logout"),

    # Project API Endpoints (Tutorial 10)
    path("projects/", project_list, name="project_list"),
    path("projects/<uuid:project_id>/", project_detail, name="project_detail"),

    # Skill API Endpoints
    path("skills/", skill_list, name="skill_list"),
    path("skills/<uuid:skill_id>/", skill_detail, name="skill_detail"),
    path("skills/<uuid:skill_id>/star/", skill_star, name="skill_star"),

    # Experience API Endpoints 
    path("experiences/", experience_list, name="experience_list"),
    path("experiences/<uuid:experience_id>/", experience_detail, name="experience_detail"),
]
