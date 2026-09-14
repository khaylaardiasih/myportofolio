from django.shortcuts import render
from main.models import Experience, Skill

def show_main(request):
    context = {
        "name": "Khayla Syafira Ardiasih",
        "npm": "2506656910",
        "study_program": "S1 Sistem Informasi",  
        "bio": (
            "IS Student at Universitas Indonesia. Driven by curiosity and ambition to shape the future through technology. "
            "A relentless lifelong learner, always seeking to grow, create, and turn ideas into meaningful impact."
        ),
    }
    return render(request, "index.html", context)

def show_experience(request):
    context = {
        "name": "Khayla Syafira Ardiasih",
        "experience_list": Experience.objects.all(),
    }
    return render(request, "experience.html", context)

def show_skills(request):
    context = {
        "name": "Khayla Syafira Ardiasih",
        "hard_skills": Skill.objects.filter(category="hard"),
        "soft_skills": Skill.objects.filter(category="soft"),
        "skill_list": Skill.objects.all(),
    }
    return render(request, "skills.html", context)