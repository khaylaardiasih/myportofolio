from rest_framework import serializers
from main.models import Skill, Experience


class SkillSerializer(serializers.ModelSerializer):
    """
    Serializer untuk model Skill.
    Mengekspos semua field yang relevan ke API, termasuk jumlah bintang
    """

    # Field tambahan: hitung jumlah user yang memberi star
    # SerializerMethodField = field yang nilainya dihitung dari sebuah method
    star_count = serializers.SerializerMethodField()

    class Meta:
        model = Skill
        # Field yang akan diekspos ke response JSON
        fields = [
            'id',
            'name',
            'category',
            'description',
            'proficiency',
            'logo_url',
            'star_count',
        ]
        # Field 'id' hanya boleh dibaca, tidak bisa diubah lewat API
        read_only_fields = ['id']

    def get_star_count(self, obj):
        """Mengembalikan jumlah user yang memberi bintang pada skill ini."""
        return obj.starred_by.count()


class ExperienceSerializer(serializers.ModelSerializer):
    """
    Serializer untuk model Experience.
    Menyertakan property 'is_ongoing' agar user tahu apakah
    pengalaman ini masih berlangsung atau sudah selesai.
    """

    # is_ongoing adalah @property di model, bukan field database
    # Tambahkan sebagai read-only field agar ikut tampil di JSON
    is_ongoing = serializers.BooleanField(read_only=True)

    class Meta:
        model = Experience
        fields = [
            'id',
            'title',
            'description',
            'category',
            'thumbnail',
            'started_at',
            'ended_at',
            'is_ongoing',
        ]
        # id dan timestamp tidak boleh diubah lewat API
        read_only_fields = ['id', 'started_at']