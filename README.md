Name : Khayla Syafira Ardiasih

NPM : 2506656910

Class : PBP Kelas A

### Tugas 1

1. Ya, saya menggunakan beberapa elemen semantik HTML5 seperti <header>, <nav>, <main>, <section>, dan <article>. Penggunaan elemen tersebut membantu saya membuat struktur HTML lebih terorganisir dan mudah dipahami. Contohnya, saya menggunakan <section> untuk membagi bagian Profile dan Experiences, sedangkan <article> digunakan untuk setiap pengalaman. Dengan begitu, kode juga lebih mudah dikelola dibandingkan jika semuanya menggunakan <div>. Selain itu, elemen seperti <nav> dan <article> membantu sya membuat fungsi dari setiap bagian website menjadi lebih jelas.

2. Tantangan utama yang saya temui adalah menyesuaikan layout dari tampilan desktop ke mobile. Pada desktop, empat kotak pengalaman masih bisa ditampilkan dalam grid 2 kolom. Namun, ketika ukuran layar mengecil, dua kolom membuat isi setiap kotak menjadi terlalu sempit. Karena itu, saya mengutamakan keterbacaan dengan mengubah layout menjadi satu kolom menggunakan @media (max-width: 600px). Saya juga menyesuaikan ukuran font dan padding agar tampilannya tetap bagus dilihat di layar hp.

3. Karena website yang dibuat masih berupa static web, seluruh informasi masih ditulis langsung di dalam HTML. Jadi, ketika ingin menambahkan atau mengubah pengalaman, saya harus mengedit kode secara manual lalu melakukan commit dan deploy kembali. Untuk pengembangan selanjutnya, saya ingin membuat fitur yang lebih dinamis menggunakan database, misalnya dengan Django agar data pengalaman dapat dikelola tanpa harus mengubah HTML secara langsung. 

## AI Disclosure & Analisis Kritis Keterbatasan AI

Dalam pengerjaan tugas ini, saya menggunakan bantuan AI untuk membantu mencari ide dan membantu membuat kerangka awal kode.

Tools yang Digunakan: Google Antigravity

Bagian yang Dibantu AI:
1. Memberikan referensi untuk implementasi layout CSS Grid 2x2 serta penggunaan custom properties pada CSS.
2. Membantu melakukan brainstorming untuk mencari beberapa alternatif sintaks navigasi antar-section.

Analisis Kritis Keterbatasan AI & Perbaikan Manual:

1. Kesalahan konseptual pada halaman
Awalnya, AI mengartikan permintaan "halaman baru" sebagai slider horizontal dengan ukuran 200vw. Setelah saya cek lagi dengan ketentuan Tugas 1, cara ini ternyata tidak sesuai karena section harus tetap berada dalam satu halaman (single-page layout). Jadi, saya menggantinya menjadi layout vertikal dengan scroll-behavior: smooth dan navigasi anchor #experiences.

2. Penyesuaian Estetika dan Ketepatan Desain
Tampilan awal dari AI masih cukup umum, seperti kotak dengan background putih dan box shadow hitam. Saya kemudian mengubah CSS nya secara manual supaya lebih sesuai dengan desain yang saya mau. Saya membuat background kotak menjadi transparan, menggunakan border pink, menambahkan animasi hover, dan menyesuaikan ukuran font untuk judul, tahun, dan deskripsi.



### Tugas 2

1. Ketika pengguna membuka halaman `/skills/`, Django pertama menerima permintaan itu
di `urls.py`. Di sini, Django melihat bahwa path tersebut perlu diteruskan ke aplikasi `main`. Di sini, path `skills/` dicocokkan dengan nama route `show_skills` dan
Django memanggil fungsi view yang sesuai di `views.py`. View inilah yang bertugas
"mengambilkan" data dari model (`Skill`) menggunakan Django ORM, lalu memasukkan hasilnya ke dalam `context`. Context tersebut dikirim ke template `skills.html`, yang kemudian memproses data itu menggunakan Django Template Language (perulangan `{% for %}`, kondisi `{% if %}`) dan menghasilkan halaman HTML utuh yang ditampilkan di browser.

2. Kalau data skill saya tulis langsung di HTML, setiap kali saya ingin menambah atau
mengubah satu skill, saya harus membuka file template dan mengedit kodenya secara manual.
Ini tidak efisien dan rawan salah, apalagi kalau datanya sudah banyak. Dengan menyimpan
data di model dan database, saya bisa mengelola skill lewat Django shell atau admin panel
tanpa harus menyentuh kode HTML sama sekali. Ini juga berarti kalau suatu saat saya mau
menampilkan data skill di halaman lain atau dalam format yang berbeda, saya tinggal
panggil model yang sama tanpa perlu menyalin-tempel data secara manual.

3. `makemigrations` bertugas membaca perubahan yang saya buat di `models.py` dan
menghasilkan file instruksi migrasi (misalnya `0002_skill.py`), tapi belum mengubah
databasenya. Sedangkan `migrate` yang benar-benar menerapkan instruksi itu ke database.
Jadi keduanya harus dijalankan secara berurutan. Contoh yang saya alami sendiri di tugas
ini: saya awalnya membuat model `Skill` tanpa field `logo_url`, lalu menjalankan
`makemigrations` dan `migrate`. Setelah itu saya menambahkan field `logo_url` ke model,
sehingga saya harus menjalankan `makemigrations` lagi (menghasilkan `0003_skill_logo_url.py`)
dan `migrate` lagi agar kolom `logo_url` benar-benar terbentuk di database.

## AI Disclosure & Analisis Kritis Keterbatasan AI 
Dalam pengerjaan tugas ini, saya menggunakan bantuan AI untuk membantu merancang struktur
halaman Skills dan menerjemahkan sketsa visual yang saya buat ke dalam kode.

Tools yang Digunakan: Google Antigravity

Bagian yang Dibantu AI:
1. Membantu merancang struktur model `Skill` dengan pemisahan kategori hard dan soft skills.
2. Memberikan referensi kode CSS untuk efek 3D, animasi melayang (`@keyframes`), dan swipe pada deretan ikon aplikasi.
3. Membantu menyusun kerangka unit test untuk menguji URL, template, data, dan kondisi kosong.

Analisis Kritis Keterbatasan AI & Perbaikan Manual:
1. Penerjemahan Desain dari Sketsa
Ketika saya mengunggah sketsa halaman Skills, AI awalnya menyarankan layout kartu biasa seperti halaman Experience. Padahal maksud saya berbeda. Saya mengarahkan ulang AI secara spesifik dan akhirnya mendapat kode CSS dengan `border-radius` squircle, multi-layer `box-shadow`, dan `@keyframes floatingApp` yang sesuai dengan visi saya.

2. Penyesuaian Scroll dan Layout Responsif
Saat jumlah ikon Hard Skills bertambah (Java, Python, Canva, CapCut, HTML & CSS, Word, Excel), tampilan sempat berantakan karena ikon meluber ke bawah. AI tidak langsung menyarankan solusi yang tepat. Saya akhirnya menambahkan `flex-wrap: nowrap`,`overflow-x: auto`, dan `flex-shrink: 0` sendiri setelah memahami masalahnya, lalu juga menambahkan custom scrollbar pink agar tampilannya tetap konsisten dengan portofolio saya.


### Tugas 3

1.  
    - `ModelForm` vs Form Manual:
    - Prinsip DRY: `ModelForm` otomatis membuat elemen input dan validasi berdasarkan definisi model (`Skill`) tanpa perlu menulis tag HTML berulang.
    - Validasi & Keamanan: Menyediakan validasi tipe data dan sanitasi input otomatis melalui `form.is_valid()`.
    - Penyimpanan Cepat: Data langsung tersimpan ke database cukup dengan memanggil `form.save()`.
    
    Mengapa diwajibkan untuk menambahkan `{% csrf_token %}`?
    Melindungi aplikasi dari serangan Cross-Site Request Forgery (CSRF) dengan memastikan request POST benar-benar berasal dari pengguna di form situs kita, bukan manipulasi dari situs berbahaya pihak ketiga. Tanpa token ini, Django otomatis menolak request dengan error 403 Forbidden.

2. 
   - Lebih Ringkas & Cepat: Format JSON tidak memiliki tag penutup redundan seperti XML, sehingga ukuran data (payload) lebih kecil dan hemat bandwidth jaringan.
   - Dukungan Natif JavaScript: JSON berbasis sintaks JavaScript sehingga dapat di-parse langsung oleh browser (`JSON.parse()`) tanpa memerlukan XML DOM parser yang berat.
   - Pemetaan Data Intuitif: Struktur key-value dan array pada JSON selaras langsung dengan struktur data umum pemrograman modern (seperti `dict` dan `list` pada python).

3. 
   - Alur View Mengembalikan JSON:
     1. Klien mengirim HTTP GET request ke URL endpoint `/api/skills/`.
     2. Django memanggil fungsi view `get_skills_json(request)`.
     3. View mengambil data dari database via Django ORM (`Skill.objects.all()`), menghasilkan QuerySet objek Python.
     4. QuerySet diubah menjadi string JSON melalui `serializers.serialize("json", skills)`.
     5. View mengembalikan response berupa `HttpResponse(skills_json, content_type="application/json")`.

   - Pentingnya Serialisasi:
     Objek model Django adalah objek Python internal yang tidak bisa langsung ditransfer melalui protokol HTTP atau dibaca oleh browser. Serialisasi berfungsi menerjemahkan objek Python tersebut menjadi format teks standar (JSON) yang universal agar dapat dimengerti dan diproses oleh klien apa pun.

## AI Disclosure & Analisis Kritis Keterbatasan AI

Dalam pengerjaan tugas ini, sebagian besar implementasi logika, perancangan template, penataan gaya CSS, dan alur CRUD (sekitar 80%) saya kerjakan secara mandiri. AI hanya saya gunakan sebagai asisten referensi untuk verifikasi sintaks dan konsultasi teknis.

Tools yang Digunakan: ChatGPT

Bagian yang Dibantu AI:
1. Memberikan referensi sintaks penggunaan parameter `instance` pada `ModelForm` untuk fungsi update di `views.py`.
2. Memberikan referensi metode assertion standar pada Django TestCase untuk pengujian view dan endpoint JSON.

1. Kesalahan Layout dan Penataan Tombol CSS:
   AI memberi saran yang menyebabkan tombol edit dan hapus bertumpukan di pojok kotak Hard Skills karena properti 'position: absolute'. Saya menganalisis masalah CSS tersebut dan merombak ulang penataan tombolnya secara mandiri agar rapi, sejajar, dan selaras dengan estetika portofolio saya.
   
2. Pencegahan Redundansi Kode Template (Prinsip DRY):
   AI sempat mengusulkan pembuatan file HTML terpisah untuk form edit. Saya menolak pendekatan tersebut karena tidak efisien, lalu saya merancang sendiri template `skills_form.html` agar bersifat modular dan dinamis sehingga dapat menangani proses Create maupun Update dalam satu berkas.