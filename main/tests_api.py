from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.contrib.auth.models import Group, User
from main.models import Skill


class SkillAPITestCase(APITestCase):
    """
    Rangkaian pengujian terotomatisasi untuk REST API Keahlian (Tugas 6).
    Memverifikasi hak akses 4 peran (Visitor, Regular User, Editor, Portfolio Owner)
    serta memastikan integritas basis data.
    """

    def setUp(self):
        self.client = APIClient()

        # 1. Superuser / Pemilik Portofolio
        self.owner = User.objects.create_superuser(
            username="owner_user", password="password123", email="owner@test.com"
        )

        # 2. Pengguna Biasa
        self.regular_user = User.objects.create_user(
            username="regular_user", password="password123"
        )

        # 3. Editor (Anggota grup 'Editor')
        self.editor_user = User.objects.create_user(
            username="editor_user", password="password123"
        )
        editor_group, _ = Group.objects.get_or_create(name="Editor")
        self.editor_user.groups.add(editor_group)

        # Objek data awal untuk pengujian
        self.skill = Skill.objects.create(
            name="Django REST Framework",
            category="hard",
            description="Membangun REST API yang tangguh dan aman.",
            proficiency=90,
            logo_url="https://example.com/drf.png",
        )

    # --- PENGUJIAN PERAN 1: PENGUNJUNG TANPA LOGIN (VISITOR) ---

    def test_visitor_can_read_skill_list_and_detail(self):
        """Pengunjung anonim dapat membaca daftar dan detail keahlian (GET 200)."""
        res_list = self.client.get("/api/v1/skills/")
        self.assertEqual(res_list.status_code, status.HTTP_200_OK)

        res_detail = self.client.get(f"/api/v1/skills/{self.skill.id}/")
        self.assertEqual(res_detail.status_code, status.HTTP_200_OK)
        self.assertFalse(res_detail.data["is_starred"])

    def test_visitor_cannot_create_skill(self):
        """Pengunjung ditolak saat membuat keahlian (401/403) dan database tidak bertambah."""
        initial_count = Skill.objects.count()
        response = self.client.post("/api/v1/skills/", {
            "name": "Docker", "category": "hard", "proficiency": 80
        })
        self.assertIn(response.status_code, [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])
        self.assertEqual(Skill.objects.count(), initial_count)

    def test_visitor_cannot_modify_or_delete_skill(self):
        """Pengunjung ditolak saat memodifikasi atau menghapus keahlian."""
        res_update = self.client.patch(f"/api/v1/skills/{self.skill.id}/", {"proficiency": 95})
        self.assertIn(res_update.status_code, [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])

        res_delete = self.client.delete(f"/api/v1/skills/{self.skill.id}/")
        self.assertIn(res_delete.status_code, [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])
        self.assertTrue(Skill.objects.filter(id=self.skill.id).exists())

    # --- PENGUJIAN PERAN 2: PENGGUNA BIASA (REGULAR USER) ---

    def test_regular_user_can_star_and_unstar(self):
        """Pengguna biasa dapat memberi dan membatalkan star (POST 200)."""
        self.client.force_authenticate(user=self.regular_user)
        star_url = f"/api/v1/skills/{self.skill.id}/star/"

        # Star pertama kali
        res_star = self.client.post(star_url)
        self.assertEqual(res_star.status_code, status.HTTP_200_OK)
        self.assertTrue(res_star.data["is_starred"])
        self.assertEqual(res_star.data["star_count"], 1)

        # Star kedua kali (Unstar)
        res_unstar = self.client.post(star_url)
        self.assertEqual(res_unstar.status_code, status.HTTP_200_OK)
        self.assertFalse(res_unstar.data["is_starred"])
        self.assertEqual(res_unstar.data["star_count"], 0)

    def test_regular_user_cannot_create_update_or_delete_skill(self):
        """Pengguna biasa dilarang melakukan aksi CUD pada keahlian (403 Forbidden)."""
        self.client.force_authenticate(user=self.regular_user)
        initial_count = Skill.objects.count()

        # Ditolak Create
        res_create = self.client.post("/api/v1/skills/", {"name": "Kubernetes", "category": "hard", "proficiency": 75})
        self.assertEqual(res_create.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Skill.objects.count(), initial_count)

        # Ditolak Update
        res_update = self.client.patch(f"/api/v1/skills/{self.skill.id}/", {"name": "Hacked Name"})
        self.assertEqual(res_update.status_code, status.HTTP_403_FORBIDDEN)
        self.skill.refresh_from_db()
        self.assertEqual(self.skill.name, "Django REST Framework")

        # Ditolak Delete
        res_del = self.client.delete(f"/api/v1/skills/{self.skill.id}/")
        self.assertEqual(res_del.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(Skill.objects.filter(id=self.skill.id).exists())

    # --- PENGUJIAN PERAN 3: EDITOR ---

    def test_editor_can_update_skill_via_patch(self):
        """Editor diizinkan melakukan pembaruan keahlian via PATCH (200 OK)."""
        self.client.force_authenticate(user=self.editor_user)
        response = self.client.patch(f"/api/v1/skills/{self.skill.id}/", {
            "proficiency": 99,
            "description": "Diperbarui oleh editor"
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.skill.refresh_from_db()
        self.assertEqual(self.skill.proficiency, 99)
        self.assertEqual(self.skill.description, "Diperbarui oleh editor")

    def test_editor_cannot_create_or_delete_skill(self):
        """Editor dilarang membuat data baru atau menghapus data (403 Forbidden)."""
        self.client.force_authenticate(user=self.editor_user)
        initial_count = Skill.objects.count()

        # Ditolak Create
        res_create = self.client.post("/api/v1/skills/", {"name": "Golang", "category": "hard", "proficiency": 80})
        self.assertEqual(res_create.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Skill.objects.count(), initial_count)

        # Ditolak Delete
        res_del = self.client.delete(f"/api/v1/skills/{self.skill.id}/")
        self.assertEqual(res_del.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(Skill.objects.filter(id=self.skill.id).exists())

    # --- PENGUJIAN PERAN 4: PEMILIK PORTOFOLIO / SUPERUSER ---

    def test_owner_can_create_and_delete_skill(self):
        """Pemilik portofolio memiliki hak penuh untuk menambah dan menghapus data."""
        self.client.force_authenticate(user=self.owner)

        # Berhasil Create (201 Created)
        res_create = self.client.post("/api/v1/skills/", {
            "name": "PostgreSQL",
            "category": "hard",
            "proficiency": 88,
            "description": "Database relasional yang handal"
        })
        self.assertEqual(res_create.status_code, status.HTTP_201_CREATED)
        new_id = res_create.data["id"]
        self.assertTrue(Skill.objects.filter(id=new_id).exists())

        # Berhasil Delete (204 No Content)
        res_del = self.client.delete(f"/api/v1/skills/{new_id}/")
        self.assertEqual(res_del.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Skill.objects.filter(id=new_id).exists())

    # --- PENGUJIAN VALIDASI & SANITASI XSS SERIALIZER ---

    def test_serializer_rejects_empty_name_or_only_html(self):
        """Serializer mengembalikan 400 Bad Request jika nama kosong atau hanya tag HTML."""
        self.client.force_authenticate(user=self.owner)
        response = self.client.post("/api/v1/skills/", {
            "name": "<b></b>",
            "category": "hard",
            "proficiency": 80
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("name", response.data)

    def test_serializer_strips_html_tags_from_input(self):
        """Serializer membersihkan tag HTML berbahaya untuk mencegah XSS."""
        self.client.force_authenticate(user=self.owner)
        response = self.client.post("/api/v1/skills/", {
            "name": "<script>alert('hack')</script>C++ Programming",
            "category": "hard",
            "description": "<img src=x onerror=alert('xss')>Deskripsi aman",
            "proficiency": 85
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        created_skill = Skill.objects.get(id=response.data["id"])
        self.assertEqual(created_skill.name, "alert('hack')C++ Programming")
        self.assertEqual(created_skill.description, "Deskripsi aman")
    
    def test_visitor_cannot_star_skill(self):
        """Pengunjung tanpa login ditolak saat mencoba memberi star (401/403)."""
        response = self.client.post(f"/api/v1/skills/{self.skill.id}/star/")
        self.assertIn(response.status_code, [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])
        self.assertEqual(self.skill.starred_by.count(), 0)

    def test_csrf_protection_enforced_without_token(self):
        """
        Sesuai checklist: Menguji dengan APIClient(enforce_csrf_checks=True) dan .login()
        untuk membuktikan bahwa request modifikasi data tanpa header X-CSRFToken ditolak (403 Forbidden).
        """
        csrf_client = APIClient(enforce_csrf_checks=True)
        csrf_client.login(username="owner_user", password="password123")

        # Request POST tanpa menyertakan token CSRF
        response = csrf_client.post("/api/v1/skills/", {
            "name": "Rust Programming",
            "category": "hard",
            "proficiency": 80,
        })
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)