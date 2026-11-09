from rest_framework import serializers
from django.utils.html import strip_tags
from main.models import Skill, Experience


class SkillSerializer(serializers.ModelSerializer):
    """
    Serializer untuk model Skill (Keahlian Pribadi).
    Mengekspos field secara eksplisit, menghitung jumlah bintang dan status
    star dari pengguna yang sedang login secara dinamis, serta melakukan sanitasi input.
    """

    # Field kalkulasi: jumlah user yang membintangi keahlian
    star_count = serializers.SerializerMethodField()

    # Field kalkulasi: apakah user saat ini sudah memberi star ke keahlian ini
    is_starred = serializers.SerializerMethodField()

    class Meta:
        model = Skill
        # Field diekspos secara eksplisit (tidak menggunakan '__all__')
        fields = [
            'id',
            'name',
            'category',
            'description',
            'proficiency',
            'logo_url',
            'star_count',
            'is_starred',
        ]
        # Field yang tidak boleh dimanipulasi secara langsung oleh client
        read_only_fields = ['id', 'star_count', 'is_starred']

    def get_star_count(self, obj):
        """Mengembalikan total jumlah pengguna yang memberikan star."""
        return obj.starred_by.count()

    def get_is_starred(self, obj):
        """
        Mengembalikan status boolean True jika user yang login telah membintangi keahlian ini.
        User diambil secara aman dari context request serializer.
        """
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.starred_by.filter(id=request.user.id).exists()
        return False

    def validate_name(self, value):
        """
        Sanitasi input nama keahlian dengan membersihkan tag HTML (mencegah XSS).
        Menolak input jika setelah dibersihkan hasilnya kosong.
        """
        cleaned_value = strip_tags(value).strip()
        if not cleaned_value:
            raise serializers.ValidationError("Nama keahlian tidak boleh kosong atau hanya berisi tag HTML.")
        return cleaned_value

    def validate_description(self, value):
        """
        Sanitasi input deskripsi keahlian untuk menangkal XSS.
        """
        if value:
            return strip_tags(value).strip()
        return ""


class ExperienceSerializer(serializers.ModelSerializer):
    """
    Serializer untuk model Experience (Tutorial 07).
    """
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
        read_only_fields = ['id', 'started_at']