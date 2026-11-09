from rest_framework.permissions import BasePermission, SAFE_METHODS

def is_editor_user(user):
    """
    Helper function untuk memeriksa apakah pengguna terautentikasi
    dan termasuk ke dalam grup 'Editor' atau memiliki izin edit keahlian.
    """
    return user.is_authenticated and (
        user.groups.filter(name="Editor").exists() or user.has_perm("main.change_skill")
    )


class IsPortfolioOwnerOrReadOnly(BasePermission):
    """
    Permission class:
    - Metode aman (GET, HEAD, OPTIONS): Diizinkan untuk semua orang (pengunjung, pengguna biasa).
    - Metode manipulasi (POST, PUT, PATCH, DELETE): Hanya diizinkan untuk superuser (pemilik portofolio).
    Digunakan terutama pada endpoint daftar (list/create).
    """
    message = "Hanya pemilik portofolio yang memiliki izin untuk melakukan aksi ini."

    def has_permission(self, request, view):
        # Izinkan jika request adalah metode baca yang aman
        if request.method in SAFE_METHODS:
            return True
        # Selain itu, hanya superuser (pemilik portofolio) yang diizinkan
        return bool(request.user and request.user.is_authenticated and request.user.is_superuser)


class IsPortfolioOwnerOrEditorOrReadOnly(BasePermission):
    """
    Permission class untuk endpoint detail objek:
    - GET, HEAD, OPTIONS: Bebas diakses siapapun (termasuk pengunjung).
    - PUT, PATCH: Diizinkan untuk Superuser ATAU Editor.
    - DELETE: Hanya diizinkan untuk Superuser (Editor dilarang menghapus).
    """
    message = "Anda tidak memiliki izin yang cukup untuk mengubah atau menghapus data ini."

    def has_permission(self, request, view):
        # Permintaan baca selalu diperbolehkan
        if request.method in SAFE_METHODS:
            return True

        # Pengguna belum login otomatis ditolak
        if not (request.user and request.user.is_authenticated):
            return False

        # Superuser memiliki izin penuh untuk semua method (PUT, PATCH, DELETE)
        if request.user.is_superuser:
            return True

        # Editor hanya boleh melakukan update (PUT/PATCH), tidak boleh DELETE
        if request.method in ["PUT", "PATCH"]:
            return is_editor_user(request.user)

        return False