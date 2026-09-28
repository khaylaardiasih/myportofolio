from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import Group, User

from main.models import Experience, Skill


class MainTest(TestCase):
    def setUp(self):
        # Buat admin user untuk menjalankan test CRUD yang membutuhkan hak superuser
        self.admin = User.objects.create_superuser(
            username="admin_test", password="password123", email="admin@test.com"
        )

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
        # Login sebagai admin sebelum create skill
        self.client.login(username="admin_test", password="password123")
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
        # Login sebagai admin sebelum update skill
        self.client.login(username="admin_test", password="password123")
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
        # Login sebagai admin sebelum delete skill
        self.client.login(username="admin_test", password="password123")
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

        # Tugas 4

    def test_anonymous_cannot_create_or_update_or_delete(self):
        """Memastikan pengunjung tanpa login dialihkan ke halaman login saat mencoba aksi CUD"""
        # Coba tambah keahlian tanpa login -> redirect ke login
        create_res = self.client.post(reverse("main:create_skill"), {"name": "Test"})
        self.assertEqual(create_res.status_code, 302)
        self.assertIn("/login/", create_res.url)

        # Coba ubah keahlian tanpa login -> redirect ke login
        update_res = self.client.post(reverse("main:update_skill", args=[self.hard_skill.id]), {"name": "Test"})
        self.assertEqual(update_res.status_code, 302)
        self.assertIn("/login/", update_res.url)

        # Coba hapus keahlian tanpa login -> redirect ke login
        delete_res = self.client.post(reverse("main:delete_skill", args=[self.hard_skill.id]))
        self.assertEqual(delete_res.status_code, 302)
        self.assertIn("/login/", delete_res.url)

    def test_regular_user_forbidden_from_modifications(self):
        """Memastikan pengguna biasa mendapat respon HTTP 403 Forbidden untuk aksi CUD"""
        # Buat user biasa dan lakukan login
        regular_user = User.objects.create_user(username="regular", password="password123")
        self.client.login(username="regular", password="password123")

        # Create ditolak dengan 403 Forbidden
        create_res = self.client.post(reverse("main:create_skill"), {"name": "Test"})
        self.assertEqual(create_res.status_code, 403)

        # Update ditolak dengan 403 Forbidden
        update_res = self.client.post(reverse("main:update_skill", args=[self.hard_skill.id]), {"name": "Test"})
        self.assertEqual(update_res.status_code, 403)

        # Delete ditolak dengan 403 Forbidden
        delete_res = self.client.post(reverse("main:delete_skill", args=[self.hard_skill.id]))
        self.assertEqual(delete_res.status_code, 403)

    def test_editor_can_update_but_cannot_create_or_delete(self):
        """Memastikan peran Editor hanya diizinkan melakukan update (tidak bisa create & delete)"""
        # Buat user dan daftarkan ke dalam grup Editor
        editor_group, _ = Group.objects.get_or_create(name="Editor")
        editor_user = User.objects.create_user(username="editor", password="password123")
        editor_user.groups.add(editor_group)

        self.client.login(username="editor", password="password123")

        # Create tetap ditolak 403 Forbidden bagi Editor
        create_res = self.client.post(reverse("main:create_skill"), {"name": "Test"})
        self.assertEqual(create_res.status_code, 403)

        # Update BERHASIL bagi Editor (redirect 302 setelah berhasil)
        update_res = self.client.post(
            reverse("main:update_skill", args=[self.hard_skill.id]),
            {
                "name": "Python Edited by Editor",
                "category": "hard",
                "description": "Diperbarui oleh editor",
                "proficiency": 90,
            }
        )
        self.assertEqual(update_res.status_code, 302)
        self.hard_skill.refresh_from_db()
        self.assertEqual(self.hard_skill.name, "Python Edited by Editor")

        # Delete tetap ditolak 403 Forbidden bagi Editor
        delete_res = self.client.post(reverse("main:delete_skill", args=[self.hard_skill.id]))
        self.assertEqual(delete_res.status_code, 403)

    def test_superuser_has_full_crud_access(self):
        """Memastikan Pemilik Portofolio (superuser) dapat melakukan Create, Update, dan Delete"""
        # Buat superuser dan login
        admin_user = User.objects.create_superuser(username="admin", password="password123", email="admin@test.com")
        self.client.login(username="admin", password="password123")

        # Create berhasil
        create_res = self.client.post(reverse("main:create_skill"), {
            "name": "Django",
            "category": "hard",
            "proficiency": 80,
        })
        self.assertEqual(create_res.status_code, 302)
        self.assertTrue(Skill.objects.filter(name="Django").exists())

        # Delete berhasil
        delete_res = self.client.post(reverse("main:delete_skill", args=[self.hard_skill.id]))
        self.assertEqual(delete_res.status_code, 302)
        self.assertFalse(Skill.objects.filter(id=self.hard_skill.id).exists())

    def test_toggle_star_functionality(self):
        """Memastikan pengguna terautentikasi dapat memberi dan membatalkan star"""
        user = User.objects.create_user(username="stargazer", password="password123")
        self.client.login(username="stargazer", password="password123")

        # Memberi star pertama kali (jumlah bertambah 1)
        res_star = self.client.post(reverse("main:toggle_star", args=[self.hard_skill.id]))
        self.assertEqual(res_star.status_code, 302)
        self.assertEqual(self.hard_skill.starred_by.count(), 1)
        self.assertTrue(self.hard_skill.starred_by.filter(id=user.id).exists())

        # Menekan tombol star lagi untuk unstar (jumlah kembali menjadi 0)
        res_unstar = self.client.post(reverse("main:toggle_star", args=[self.hard_skill.id]))
        self.assertEqual(res_unstar.status_code, 302)
        self.assertEqual(self.hard_skill.starred_by.count(), 0)