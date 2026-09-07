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
