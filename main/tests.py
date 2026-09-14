from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from main.models import Experience, Skill


class MainTest(TestCase):
    def setUp(self):
        self.experience = Experience.objects.create(
            title="Asisten Dosen PBP",
            description="Membantu mahasiswa memahami pengembangan web.",
            category="part-time",
        )

        self.hard_skill = Skill.objects.create(
            name="Python",
            category="hard",
            description="Pemrograman Python untuk web development",
            proficiency=85,
        )
        self.soft_skill = Skill.objects.create(
            name="Problem Solving",
            category="soft",
            description="Menganalisis dan memecahkan masalah logika",
            proficiency=90,
        )

    def test_main_url_is_accessible(self):
        response = self.client.get(reverse("main:show_main"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "index.html")
        self.assertNotContains(response, self.experience.title)
        self.assertContains(response, f'href="{reverse("main:show_experience")}"')

    def test_nonexistent_page_returns_404(self):
        response = self.client.get("/halaman-yang-tidak-ada/")

        self.assertEqual(response.status_code, 404)

    def test_experience_model(self):
        self.assertEqual(str(self.experience), "Asisten Dosen PBP")
        self.assertEqual(self.experience.category, "part-time")
        self.assertTrue(self.experience.is_ongoing)

    def test_experience_page(self):
        response = self.client.get(reverse("main:show_experience"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "experience.html")
        self.assertContains(response, self.experience.title)
        self.assertContains(response, self.experience.description)
        self.assertContains(response, "Part-Time")
        self.assertContains(response, "Sedang berlangsung")
        self.assertContains(response, f'href="{reverse("main:show_main")}"')

    def test_empty_experience_page(self):
        Experience.objects.all().delete()
        response = self.client.get(reverse("main:show_experience"))

        self.assertContains(response, "Belum ada pengalaman yang ditambahkan.")

    def test_completed_experience(self):
        self.experience.ended_at = timezone.now()
        self.experience.save()
        response = self.client.get(reverse("main:show_experience"))

        self.assertFalse(self.experience.is_ongoing)
        self.assertContains(response, "Selesai")
        self.assertNotContains(response, "Sedang berlangsung")
        
     # --- TEST FITUR SKILL BARU ---

    def test_skill_model(self):
        self.assertEqual(str(self.hard_skill), "Python (Hard Skills)")
        self.assertEqual(self.hard_skill.category, "hard")
        self.assertEqual(self.soft_skill.category, "soft")
    
    def test_skills_page(self):
        response = self.client.get(reverse("main:show_skills"))
        # 1. URL dapat diakses dan menggunakan template yang tepat
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "skills.html")
        # 2. Data model muncul di halaman HTML ketika ada data
        self.assertContains(response, self.hard_skill.name)
        self.assertContains(response, self.soft_skill.name)
        self.assertContains(response, "Hard Skills")
        self.assertContains(response, "Soft Skills")
        self.assertContains(response, f'href="{reverse("main:show_main")}"')
    
    def test_empty_skills_page(self):
        # 3. Menampilkan pesan kondisi kosong ketika belum ada data
        Skill.objects.all().delete()
        response = self.client.get(reverse("main:show_skills"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Belum ada keahlian yang ditambahkan.")