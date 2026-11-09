from django.urls import path
from main.api_views import (
    skill_list,
    skill_detail,
    skill_star,
    experience_list,
    experience_detail,
)

app_name = "api"

urlpatterns = [
    # Skill API Endpoints
    path("skills/", skill_list, name="skill_list"),
    path("skills/<uuid:skill_id>/", skill_detail, name="skill_detail"),
    path("skills/<uuid:skill_id>/star/", skill_star, name="skill_star"),

    # Experience API Endpoints 
    path("experiences/", experience_list, name="experience_list"),
    path("experiences/<uuid:experience_id>/", experience_detail, name="experience_detail"),
]