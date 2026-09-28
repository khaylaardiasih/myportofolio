from django.contrib import messages
from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from main.forms import SkillForm
from main.models import Experience, Skill
import datetime

def show_main(request):
    last_login = request.COOKIES.get('last_login', 'Belum ada sesi login / Cookie tidak ditemukan')
    context = {
        "name": "Khayla Syafira Ardiasih",
        "npm": "2506656910",
        "study_program": "S1 Sistem Informasi",
        "bio": (
            "IS Student at Universitas Indonesia. Driven by curiosity and ambition to shape the future through technology. "
            "A relentless lifelong learner, always seeking to grow, create, and turn ideas into meaningful impact."
        ),
        "last_login": last_login,  # <- Tambahkan ini
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

     # Periksa status editor pengguna untuk pengaturan tampilan UI di template
    is_editor = is_editor_user(request.user)

    context = {
        "name": "Khayla Syafira Ardiasih",
        "skill_list": skills,
        "hard_skills": [s for s in skills if s.category == "hard"],
        "soft_skills": [s for s in skills if s.category == "soft"],
        "search_query": search_query,
        "is_editor": is_editor,
    }
    return render(request, "skills.html", context)

@login_required(login_url="/login/")
def create_skill(request):
    if not request.user.is_superuser:
        raise PermissionDenied

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
@login_required(login_url="/login/")
def update_skill(request, skill_id):
    if not request.user.is_superuser:
        raise PermissionDenied

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

    skills_json = serializers.serialize(
        "json", skills, use_natural_foreign_keys=True
    )
    return HttpResponse(skills_json, content_type="application/json")

@login_required(login_url="/login/")
def delete_skill(request, skill_id):
    if not request.user.is_superuser:
        raise PermissionDenied
    skill = get_object_or_404(Skill, pk=skill_id)

    if request.method == "POST":
        # Simpan nama & kategori sebelum dihapus dari database
        cat_label = "Hard Skill" if skill.category == "hard" else "Soft Skill"
        skill_name = skill.name
        skill.delete()
        messages.success(request, f"{cat_label} '{skill_name}' berhasil dihapus!")
        return redirect("main:show_skills")

    return redirect("main:show_skills")

def register(request):
    form = UserCreationForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Akun berhasil dibuat. Silakan login.")
        return redirect("main:login")

    context = {
        "name": "Khayla Syafira Ardiasih",
        "form": form,
    }
    return render(request, "register.html", context)

def login_user(request):
    form = AuthenticationForm(request, data=request.POST or None)

    if request.method == "POST" and form.is_valid():
        user = form.get_user()
        login(request, user)
        response = redirect("main:show_main")
        # Simpan cookie last_login dengan format waktu YYYY-MM-DD HH:MM:SS
        response.set_cookie('last_login', datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        return response

    context = {
        "name": "Khayla Syafira Ardiasih",
        "form": form,
    }
    return render(request, "login.html", context)

def logout_user(request):
    logout(request)
    response = redirect("main:show_main")
    response.delete_cookie('last_login')
    return response

@login_required(login_url="/login/")
def toggle_star(request, skill_id):
    skill = get_object_or_404(Skill, pk=skill_id)

    if request.method == "POST":
        if request.user in skill.starred_by.all():
            skill.starred_by.remove(request.user)
        else:
            skill.starred_by.add(request.user)

    return redirect("main:show_skills")

def is_editor_user(user):
    # Cek apakah user sudah login dan terdaftar di grup 'Editor' atau punya izin edit skill
    return user.is_authenticated and (
        user.groups.filter(name="Editor").exists() or user.has_perm("main.change_skill")
    )