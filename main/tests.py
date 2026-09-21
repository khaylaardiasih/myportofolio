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

    def test_create_skill(self):
        """Memastikan new skill dapat ditambahkan lewat POST request"""
        response = self.client.post(reverse("main:create_skill"), {
            "name": "Django Framework",
            "category": "hard",
            "description": "Pengembangan web dengan Django",
            "proficiency": 85,
            "logo_url": "https://example.com/django.png",
        })
        # Berhasil redirect setelah simpan
        self.assertEqual(response.status_code, 302)
        # Berhasil tersimpan di database
        self.assertTrue(Skill.objects.filter(name="Django Framework").exists())

    def test_update_skill(self):
        """Memastikan data keahlian yang ada dapat di update"""
        response = self.client.post(
            reverse("main:update_skill", args=[self.hard_skill.id]),
            {
                "name": "Python Advanced",
                "category": "hard",
                "description": "Pemrograman Python tingkat lanjut",
                "proficiency": 95,
                "logo_url": "",
            }
        )
        # Berhasil redirect ke halaman skills
        self.assertEqual(response.status_code, 302)
        # Mengambil data terbaru dari database
        self.hard_skill.refresh_from_db()
        self.assertEqual(self.hard_skill.name, "Python Advanced")
        self.assertEqual(self.hard_skill.proficiency, 95)

    def test_delete_skill(self):
        """Memastikan data keahlian dapat dihapus dari database"""
        response = self.client.post(
            reverse("main:delete_skill", args=[self.hard_skill.id])
        )
        self.assertEqual(response.status_code, 302)
        # Objek sudah tidak ada lagi di database
        self.assertFalse(Skill.objects.filter(id=self.hard_skill.id).exists())

    def test_get_skills_json(self):
        """Memastikan endpoint API mengembalikan data dalam format JSON yang valid"""
        response = self.client.get(reverse("main:get_skills_json"))
        self.assertEqual(response.status_code, 200)
        # Header response harus berupa application/json
        self.assertEqual(response["Content-Type"], "application/json")
        # Memastikan data skill yang dibuat di setUp termuat di dalam payload JSON
        self.assertContains(response, "Python")