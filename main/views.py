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
        # Simpan skill baru ke database
        skill = form.save()

        # Deteksi jenis kategori untuk notifikasi
        cat_label = "Hard Skill" if skill.category == "hard" else "Soft Skill"
        messages.success(request, f"{cat_label} '{skill.name}' berhasil ditambahkan!")
        return redirect("main:show_skills")

    context = {
        "name": "Khayla Syafira Ardiasih",
        "form": form,
    }
    return render(request, "skills_form.html", context)

# Tugas 3
def update_skill(request, skill_id):
    # Mengambil skill; jika ID tidak ditemukan, otomatis kembalikan error 404
    skill = get_object_or_404(Skill, pk=skill_id)

    # Jika request berupa POST, form diisi data baru (request.POST).
    # Jika request berupa GET, form otomatis menampilkan data lama dari 'instance=skill'.
    form = SkillForm(request.POST or None, instance=skill)

    # Validasi apakah metode request adalah POST dan seluruh field form memenuhi aturan validasi model
    if request.method == "POST" and form.is_valid():
        # Menyimpan perubahan data ke database
        skill = form.save()
        # Deteksi jenis kategori untuk notifikasi
        cat_label = "Hard Skill" if skill.category == "hard" else "Soft Skill"
        # Pesan sukses untuk memberi tahu pengguna bahwa skill berhasil di update
        messages.success(request, f"{cat_label} '{skill.name}' berhasil di-update!")
        return redirect("main:show_skills")

    context = {
        "name": "Khayla Syafira Ardiasih", 
        "form": form,                      
        "skill": skill,                    
        "is_edit": True,                    
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
        # Simpan nama & kategori sebelum dihapus dari database
        cat_label = "Hard Skill" if skill.category == "hard" else "Soft Skill"
        skill_name = skill.name
        skill.delete()
        messages.success(request, f"{cat_label} '{skill_name}' berhasil dihapus!")
        return redirect("main:show_skills")

    return redirect("main:show_skills")