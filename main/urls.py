from django.urls import path
from main.views import (
    # Views halaman web (sudah ada sebelumnya)
    show_main, show_experience, show_skills,
    create_skill, update_skill, get_skills_json,
    delete_skill, register, login_user, logout_user,
    toggle_star, create_skill_ajax,
    # Views API baru (Django REST Framework)
    api_skill_list, api_skill_detail,
    api_skill_create, api_skill_update, api_skill_delete,
    api_experience_list, api_experience_detail,
)

app_name = "main"

urlpatterns = [
    # Halaman Web (HTML) 
    path("", show_main, name="show_main"),
    path("experience/", show_experience, name="show_experience"),
    path("skills/", show_skills, name="show_skills"),
    path("skills/add/", create_skill, name="create_skill"),
    path("skills/<uuid:skill_id>/edit/", update_skill, name="update_skill"),
    path("skills/<uuid:skill_id>/delete/", delete_skill, name="delete_skill"),
    path("register/", register, name="register"),
    path("login/", login_user, name="login"),
    path("logout/", logout_user, name="logout"),
    path("skills/<uuid:skill_id>/star/", toggle_star, name="toggle_star"),

    # Endpoint AJAX lama (tetap dipertahankan)
    path("api/skills/", get_skills_json, name="get_skills_json"),
    path("skills/add-ajax/", create_skill_ajax, name="create_skill_ajax"),

    # REST API (Django REST Framework)
    # Skill endpoints
    path("api/v1/skills/", api_skill_list, name="api_skill_list"),
    path("api/v1/skills/create/", api_skill_create, name="api_skill_create"),
    path("api/v1/skills/<uuid:skill_id>/", api_skill_detail, name="api_skill_detail"),
    path("api/v1/skills/<uuid:skill_id>/update/", api_skill_update, name="api_skill_update"),
    path("api/v1/skills/<uuid:skill_id>/delete/", api_skill_delete, name="api_skill_delete"),

    # Experience endpoints
    path("api/v1/experiences/", api_experience_list, name="api_experience_list"),
    path("api/v1/experiences/<uuid:experience_id>/", api_experience_detail, name="api_experience_detail"),
]