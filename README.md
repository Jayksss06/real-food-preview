# Remboelan — Real Food Preview (WebAR Menu)

Website profil Restoran Remboelan (*Indonesian Soulfood*) yang dilengkapi fitur eksplorasi buku menu berbasis **Web Augmented Reality (WebAR)** dengan visualisasi hidangan 3D dan rincian komposisi mandiri (*Floating Paper Receipt*).

## Fitur Utama
- **Profil Restoran & Katalog Gallery+:** Mengadaptasi tata letak katalog digital 25 kategori menu Restoran Remboelan.
- **Pratinjau Hidangan 3D:** Visualisasi porsi makanan Nusantara secara 360 derajat berbasis Three.js WebGL untuk menu pilihan (*Nasi Bakar Roa*, *Nasi Langgi*, *Nasi Berkat*, dan *Nasi Bakar Ayam Asap*).
- **Pemindai Buku Menu (WebAR):** Akses kamera peramban (WebRTC) untuk memindai foto hidangan pada buku menu fisik secara langsung (*HTTPS* pada Vercel mendukung akses kamera di Android dan iOS).
- **Struk Komposisi Mandiri:** Menampilkan rincian bahan baku utama, racikan bumbu halus, tingkat kepedasan, dan peringatan alergen.

## Deployment di Vercel
Proyek ini merupakan situs statis (*Static HTML/JS/CSS*) yang siap di-deploy langsung di Vercel tanpa langkah build tambahan (*Framework Preset: Other*, *Output Directory: .*).
