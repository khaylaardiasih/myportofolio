from django.contrib import messages
from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_POST
from main.forms import SkillForm
from main.models import Experience, Skill
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from main.serializers import SkillSerializer, ExperienceSerializer
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
    search_query = request.GET.get("name", "").strip()
    is_editor = is_editor_user(request.user)

    context = {
        "name": "Khayla Syafira Ardiasih",
        "search_query": search_query,
        "is_editor": is_editor,
        "form": SkillForm(),  # Dipersiapkan untuk modal tambah skill di Langkah 4
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
    # Izinkan jika superuser atau editor
    if not (request.user.is_superuser or is_editor_user(request.user)):
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
    skills = Skill.objects.prefetch_related('starred_by').all()

    if search_query:
        skills = skills.filter(name__icontains=search_query)

    data = []
    for skill in skills:
        starred_users = skill.starred_by.all()
        is_starred = request.user in starred_users if request.user.is_authenticated else False
        starred_by_names = ", ".join([u.username for u in starred_users])

        data.append({
            "pk": str(skill.id),
            "fields": {
                "name": skill.name,
                "category": skill.category,
                "description": skill.description or "",
                "proficiency": skill.proficiency,
                "logo_url": skill.logo_url or "",
                "star_count": starred_users.count(),
                "is_starred": is_starred,
                "starred_by_names": starred_by_names,
            }
        })

    return JsonResponse(data, safe=False)

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
        # Toggle status bintang keahlian untuk user saat ini
        if request.user in skill.starred_by.all():
            skill.starred_by.remove(request.user)
            is_starred = False
            msg = f"Batal menyukai keahlian '{skill.name}'."
            messages.info(request, msg)
        else:
            skill.starred_by.add(request.user)
            is_starred = True
            msg = f"Berhasil memberikan star pada '{skill.name}'! ✦"
            messages.success(request, msg)

        # FITUR EKSTRA: Respons JSON untuk AJAX Star Toggle
        # Kembalikan JSON jika request dikirim lewat Fetch / AJAX
        if request.headers.get("x-requested-with") == "XMLHttpRequest" or request.headers.get("Accept") == "application/json":
            return JsonResponse({
                "status": "success",
                "is_starred": is_starred,
                "star_count": skill.starred_by.count(),
                "message": msg,
            })

    # Fallback redirect untuk form submit standar
    return redirect("main:show_skills")

def is_editor_user(user):
    # Cek apakah user sudah login dan terdaftar di grup 'Editor' atau punya izin edit skill
    return user.is_authenticated and (
        user.groups.filter(name="Editor").exists() or user.has_perm("main.change_skill")
    )

@require_POST
def create_skill_ajax(request):
    if not request.user.is_superuser:
        return JsonResponse(
            {"message": "Hanya pemilik portofolio yang dapat menambahkan keahlian."},
            status=403,
        )

    form = SkillForm(request.POST)
    if form.is_valid():
        skill = form.save()
        return JsonResponse(
            {"message": "Keahlian berhasil ditambahkan.", "pk": str(skill.id)},
            status=201,
        )

    return JsonResponse({"errors": form.errors.get_json_data()}, status=400)

# Tutorial 7 Django REST Framework (DRF) API Views

@api_view(['GET'])
def api_skill_list(request):
    """
    Mengembalikan daftar semua keahlian dalam format JSON.
    Mendukung filter pencarian via query param ?name=...
    """
    # Ambil query parameter 'name' untuk filter pencarian
    search_query = request.GET.get('name', '').strip()
    skills = Skill.objects.all()

    # Filter berdasarkan nama jika query param 'name' disertakan
    if search_query:
        skills = skills.filter(name__icontains=search_query)

    # Serialisasi queryset; many=True karena lebih dari satu objek
    serializer = SkillSerializer(skills, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def api_skill_detail(request, skill_id):
    """
    Mengembalikan detail satu keahlian berdasarkan UUID.
    """
    # get_object_or_404 otomatis mengembalikan 404 jika tidak ditemukan
    skill = get_object_or_404(Skill, pk=skill_id)
    serializer = SkillSerializer(skill)
    return Response(serializer.data)


@api_view(['POST'])
def api_skill_create(request):
    """
    Membuat keahlian baru. Hanya bisa dilakukan oleh superuser.
    Request body: JSON dengan field name, category, description, proficiency, logo_url
    """
    # Pastikan hanya superuser yang bisa membuat skill via API
    if not request.user.is_authenticated or not request.user.is_superuser:
        return Response(
            {'message': 'Hanya pemilik portofolio yang dapat menambahkan keahlian.'},
            status=status.HTTP_403_FORBIDDEN
        )

    # Deserialisasi data dari request; DRF otomatis membaca JSON body
    serializer = SkillSerializer(data=request.data)
    if serializer.is_valid():
        # Simpan objek baru ke database
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    # Jika validasi gagal, kembalikan error detail
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT', 'PATCH'])
def api_skill_update(request, skill_id):
    """
    Mengubah data keahlian. Superuser atau Editor bisa mengakses endpoint ini.
    - PUT: update semua field (partial=False)
    - PATCH: update sebagian field saja (partial=True)
    """
    # Cek izin: hanya superuser atau editor yang boleh update
    if not request.user.is_authenticated or not (
        request.user.is_superuser or is_editor_user(request.user)
    ):
        return Response(
            {'message': 'Anda tidak memiliki izin untuk mengubah keahlian.'},
            status=status.HTTP_403_FORBIDDEN
        )

    skill = get_object_or_404(Skill, pk=skill_id)

    # partial=True jika method PATCH (update sebagian field saja)
    is_partial = request.method == 'PATCH'
    serializer = SkillSerializer(skill, data=request.data, partial=is_partial)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
def api_skill_delete(request, skill_id):
    """
    Menghapus keahlian. Hanya superuser yang diizinkan.
    """
    # Hanya superuser yang bisa menghapus skill
    if not request.user.is_authenticated or not request.user.is_superuser:
        return Response(
            {'message': 'Hanya pemilik portofolio yang dapat menghapus keahlian.'},
            status=status.HTTP_403_FORBIDDEN
        )

    skill = get_object_or_404(Skill, pk=skill_id)
    skill_name = skill.name  # Simpan nama sebelum dihapus untuk pesan konfirmasi
    skill.delete()

    # 204 No Content: berhasil dihapus, tidak ada response body
    return Response(
        {'message': f"Keahlian '{skill_name}' berhasil dihapus."},
        status=status.HTTP_200_OK
    )


@api_view(['GET'])
def api_experience_list(request):
    """
    Mengembalikan daftar semua pengalaman dalam format JSON.
    """
    experiences = Experience.objects.all()

    # Serialisasi queryset pengalaman
    serializer = ExperienceSerializer(experiences, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def api_experience_detail(request, experience_id):
    """
    Mengembalikan detail satu pengalaman berdasarkan UUID.
    """
    experience = get_object_or_404(Experience, pk=experience_id)
    serializer = ExperienceSerializer(experience)
    return Response(serializer.data)