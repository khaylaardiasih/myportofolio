from django.forms import ModelForm, TextInput, Textarea, URLInput, Select, NumberInput
from main.models import Skill

class SkillForm(ModelForm):
    class Meta:
        model = Skill
        fields = [
            "name",
            "category",
            "description",
            "proficiency",
            "logo_url",
        ]

        labels = {
            "name": "Nama Keahlian",
            "category": "Kategori Keahlian",
            "description": "Deskripsi Keahlian",
            "proficiency": "Tingkat Kemahiran (%)",
            "logo_url": "URL Logo / Ikon",
        }

        widgets = {
            "name": TextInput(
                attrs={
                    "placeholder": "Contoh: Python, Figma, Public Speaking",
                    "maxlength": 100,
                }
            ),
            "category": Select(),
            "description": Textarea(
                attrs={
                    "placeholder": "Jelaskan pengalaman atau hal yang kamu kuasai...",
                    "rows": 3,
                }
            ),
            "proficiency": NumberInput(
                attrs={
                    "placeholder": "Contoh: 85",
                    "min": 0,
                    "max": 100,
                }
            ),
            "logo_url": URLInput(
                attrs={
                    "placeholder": "https://example.com/logo.png",
                }
            ),
        }