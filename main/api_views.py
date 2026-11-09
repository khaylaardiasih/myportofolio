from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

from main.models import Skill, Experience
from main.serializers import SkillSerializer, ExperienceSerializer
from main.permissions import (
    IsPortfolioOwnerOrReadOnly,
    IsPortfolioOwnerOrEditorOrReadOnly,
)


# --- SKILL API ENDPOINTS ---

@api_view(['GET', 'POST'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsPortfolioOwnerOrReadOnly])
def skill_list(request):
    """
    Endpoint koleksi keahlian (/api/v1/skills/):
    - GET: Mengembalikan daftar keahlian, mendukung pencarian nama via ?name=...
    - POST: Membuat keahlian baru (hanya diizinkan untuk superuser/pemilik).
    """
    if request.method == 'GET':
        search_query = request.GET.get('name', '').strip()
        skills = Skill.objects.all()

        if search_query:
            skills = skills.filter(name__icontains=search_query)

        # Lewatkan request ke serializer context agar get_is_starred berfungsi
        serializer = SkillSerializer(skills, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        serializer = SkillSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsPortfolioOwnerOrEditorOrReadOnly])
def skill_detail(request, skill_id):
    """
    Endpoint detail satu keahlian (/api/v1/skills/<uuid>/):
    - GET: Mengambil detail satu keahlian (Pengunjung & Pengguna).
    - PUT / PATCH: Memperbarui keahlian (Superuser & Editor).
    - DELETE: Menghapus keahlian (Hanya Superuser).
    """
    skill = get_object_or_404(Skill, pk=skill_id)

    if request.method == 'GET':
        serializer = SkillSerializer(skill, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method in ['PUT', 'PATCH']:
        # Jika metode PATCH, perbolehkan pembaruan data parsial
        partial = (request.method == 'PATCH')
        serializer = SkillSerializer(
            skill, data=request.data, partial=partial, context={'request': request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        skill_name = skill.name
        skill.delete()
        # Sesuai checklist rubrik: mengembalikan 204 No Content
        return Response(
            {"message": f"Keahlian '{skill_name}' berhasil dihapus."},
            status=status.HTTP_204_NO_CONTENT
        )


@api_view(['POST'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def skill_star(request, skill_id):
    """
    Endpoint toggle star keahlian (/api/v1/skills/<uuid>/star/):
    Hanya pengguna yang sudah login (IsAuthenticated) yang dapat memberikan atau membatalkan star.
    """
    skill = get_object_or_404(Skill, pk=skill_id)

    if skill.starred_by.filter(id=request.user.id).exists():
        skill.starred_by.remove(request.user)
        message = f"Batal menyukai keahlian '{skill.name}'."
    else:
        skill.starred_by.add(request.user)
        message = f"Berhasil memberikan star pada '{skill.name}'! ✦"

    serializer = SkillSerializer(skill, context={'request': request})
    response_data = serializer.data
    response_data['message'] = message
    return Response(response_data, status=status.HTTP_200_OK)


# --- EXPERIENCE API ENDPOINTS ---

@api_view(['GET'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
def experience_list(request):
    """Endpoint daftar pengalaman (/api/v1/experiences/)."""
    experiences = Experience.objects.all()
    serializer = ExperienceSerializer(experiences, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
def experience_detail(request, experience_id):
    """Endpoint detail pengalaman (/api/v1/experiences/<uuid>/)."""
    experience = get_object_or_404(Experience, pk=experience_id)
    serializer = ExperienceSerializer(experience)
    return Response(serializer.data, status=status.HTTP_200_OK)