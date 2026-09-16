from django.contrib import messages
from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from main.forms import SkillForm
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
    json_response = get_skills_json(request)

    skills = serializers.deserialize(
        "json",
        json_response.content.decode("utf-8"),
    )
    skills = [skill.object for skill in skills]
    search_query = request.GET.get("name", "").strip()

    context = {
        "name": "Khayla Syafira Ardiasih",
        "skill_list": skills,
        "hard_skills": [s for s in skills if s.category == "hard"],
        "soft_skills": [s for s in skills if s.category == "soft"],
        "search_query": search_query,
    }
    return render(request, "skills.html", context)

def create_skill(request):
    form = SkillForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Keahlian baru berhasil ditambahkan!")
        return redirect("main:show_skills")

    context = {
        "name": "Khayla Syafira Ardiasih",
        "form": form,
    }
    return render(request, "skills_form.html", context)

def get_skills_json(request):
    search_query = request.GET.get("name", "").strip()
    skills = Skill.objects.all()

    if search_query:
        skills = skills.filter(name__icontains=search_query)

    skills_json = serializers.serialize("json", skills)
    return HttpResponse(skills_json, content_type="application/json")

def delete_skill(request, skill_id):
    skill = get_object_or_404(Skill, pk=skill_id)

    if request.method == "POST":
        skill.delete()
        messages.success(request, f"Keahlian {skill.name} berhasil dihapus!")
        return redirect("main:show_skills")

    return redirect("main:show_skills")