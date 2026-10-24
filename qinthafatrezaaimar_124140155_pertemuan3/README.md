# Rak Buku Pribadi - Aplikasi Manajemen Buku

Tugas Praktikum Pengembangan Aplikasi Web - Pertemuan 3: React Basics

## Identitas

| | |
|---|---|
| **Nama Lengkap** | Qinthafa Treza Aimar |
| **NIM** | 124140155 |
| **Kelas Praktikum** | RA |

## Deskripsi Aplikasi

Rak Buku Pribadi adalah aplikasi web untuk mencatat koleksi buku pribadi. Setiap buku dicatat dengan judul, penulis, dan salah satu dari tiga status:

- **Dimiliki**: buku yang sudah dipunya
- **Sedang Dibaca**: buku yang sedang dibaca
- **Ingin Dibeli**: buku yang masuk daftar keinginan

Pengguna dapat menambah, mengedit, menghapus, mencari, dan memfilter buku. Halaman Statistik menampilkan ringkasan isi rak. Semua data tersimpan di `localStorage`, sehingga tidak hilang saat browser ditutup.

Dibuat dengan **React 18** dan **Vite**.

## Cara Menjalankan

Prasyarat: [Node.js](https://nodejs.org) versi **22.13 atau lebih baru** (versi LTS). Cek dengan `node -v`.

1. Clone repository, lalu buka folder `qinthafatrezaaimar_124140155_pertemuan3` di VS Code.
   ```bash
   git clone https://github.com/qintaboy/pemrograman_web_itera_124140155.git
   cd pemrograman_web_itera_124140155/qinthafatrezaaimar_124140155_pertemuan3
   ```
2. Buka terminal VS Code (**Ctrl + `**), lalu pasang dependensi:
   ```bash
   npm install
   ```
3. Jalankan aplikasi:
   ```bash
   npm run dev
   ```
4. Buka alamat yang muncul di terminal (biasanya `http://localhost:5173`).

### Menjalankan unit test

```bash
npm test           # mode watch (otomatis jalan ulang saat file berubah)
npm run test:run   # jalan sekali lalu selesai
```


## Fitur Aplikasi

- [x] Menambah buku (judul, penulis, status)
- [x] Mengedit buku: data dimuat ke form, buku yang sedang diedit ditandai di daftar
- [x] Menghapus buku dengan konfirmasi
- [x] Filter berdasarkan status, lengkap dengan jumlah buku per status
- [x] Pencarian berdasarkan judul atau nama penulis (tidak membedakan huruf besar/kecil)
- [x] Validasi form: judul dan penulis wajib diisi, judul minimal 2 karakter, kolom yang salah diberi garis dan pesan merah
- [x] Data tersimpan di `localStorage`
- [x] Halaman Statistik: jumlah per status, komposisi rak, dan penulis terbanyak
- [x] Halaman 404 untuk alamat yang tidak dikenal
- [x] Tampilan responsif untuk layar HP

## Struktur Folder

```
src/
├── components/            # Komponen reusable
│   ├── BookFilter/        # Kolom pencarian + tombol filter status
│   ├── BookForm/          # Form tambah/edit buku dengan validasi
│   ├── BookItem/          # Satu baris buku (judul, penulis, status, tombol aksi)
│   ├── BookList/          # Daftar buku + pesan kosong
│   ├── Navbar/            # Navigasi antarhalaman
│   ├── StatCard/          # Kartu angka ringkasan
│   └── StatusBadge/       # Label status berwarna
├── pages/
│   ├── Home/              # Halaman Koleksi (/)
│   ├── Stats/             # Halaman Statistik (/statistik)
│   └── NotFound/          # Halaman 404
├── hooks/
│   ├── useLocalStorage.js # Custom hook: state yang tersimpan ke localStorage
│   └── useBookStats.js    # Custom hook: menghitung statistik buku
├── context/
│   ├── BookContext.jsx    # BookProvider: state buku + fungsi CRUD
│   └── useBooks.js        # Objek context + hook useBooks()
├── constants/             # Daftar status buku dan bentuk PropTypes buku
├── utils/                 # Fungsi validasi form
├── __tests__/             # Unit test
├── App.jsx                # Daftar route
└── main.jsx               # Titik masuk: BrowserRouter + BookProvider
```

## Penjelasan Fitur React yang Digunakan

### Functional Component dan Hooks

Semua komponen ditulis sebagai function component.

- **`useState`**: menyimpan isi form dan pesan error (`BookForm`), serta kata kunci pencarian, filter status, dan buku yang sedang diedit (`Home`).
- **`useEffect`**: mengubah judul tab browser sesuai halaman dan jumlah buku (`Home`, `Stats`), serta menyimpan data ke `localStorage` setiap kali berubah (`useLocalStorage`).
- **`useMemo`**: menghitung ulang hasil pencarian/filter (`Home`) dan statistik (`useBookStats`) hanya saat datanya berubah.
- **`useContext`**: dipakai di dalam `useBooks()` untuk mengambil data dari Context.

### Komponen Reusable

Aplikasi memiliki 7 komponen reusable. Contohnya:
- `BookForm` dipakai untuk **dua mode**: tambah dan edit, dibedakan lewat props `initialData`, `onCancel`, dan `submitLabel`.
- `StatusBadge` dipakai di daftar buku dan halaman Statistik.
- `StatCard` dipakai 4 kali di halaman Statistik dengan props berbeda.

### Context API

`BookProvider` (di `context/BookContext.jsx`) membungkus seluruh aplikasi dan menyediakan `books`, `addBook`, `updateBook`, dan `deleteBook`. Komponen mana pun cukup memanggil `useBooks()` tanpa perlu mengoper props berlapis-lapis. Contohnya `Navbar` menampilkan jumlah buku, dan halaman Statistik membaca data yang sama dengan halaman Koleksi.

Semua perubahan data dilakukan secara *immutable*: `[bukuBaru, ...lama]` untuk menambah, `map()` untuk mengedit, dan `filter()` untuk menghapus.

### React Router

`App.jsx` mendefinisikan tiga route: `/` (Koleksi), `/statistik` (Statistik), dan `*` (404). `Navbar` memakai `NavLink` sehingga menu halaman yang aktif otomatis disorot.

### Custom Hooks

- **`useLocalStorage(key, nilaiAwal)`**: dipakai seperti `useState`, tetapi nilainya dibaca dari `localStorage` saat pertama kali dibuat (lazy initialization) dan disimpan kembali dengan `useEffect` setiap kali berubah. Pembacaan dibungkus `try...catch` agar aplikasi tidak rusak jika datanya korup.
- **`useBookStats(books)`**: menghitung total buku, jumlah per status, persentase buku yang sudah dimiliki, dan 5 penulis terbanyak.

### PropTypes

Semua komponen yang menerima props memiliki `propTypes`. Bentuk data buku didefinisikan sekali di `constants/propTypes.js` (`bookShape`) lalu dipakai ulang di `BookItem` dan `BookList`. Status buku divalidasi dengan `PropTypes.oneOf(['milik', 'baca', 'beli'])`.

Project ini sengaja memakai **React 18**, karena React 19 sudah tidak lagi menjalankan pengecekan PropTypes.

### Error Handling Form

`BookForm` memanggil `validasiBuku()` (di `utils/validasiBuku.js`) saat tombol simpan ditekan. Jika ada kolom yang salah:
- data tidak dikirim,
- input diberi class `input-salah` (garis dan latar merah) serta `aria-invalid`,
- pesan error merah muncul di bawah input.

Pesan error langsung hilang begitu kolom tersebut diketik ulang.

## Unit Testing

Test ditulis dengan **Vitest** dan **React Testing Library**, berjumlah **13 test** di 4 file:

| File | Yang diuji |
|---|---|
| `BookForm.test.jsx` | Validasi form kosong, kirim data valid + reset form, pesan error hilang saat diperbaiki, mode edit + tombol Batal |
| `BookListFilter.test.jsx` | Pesan daftar kosong, render daftar + tombol hapus, callback filter dan pencarian |
| `hooks.test.js` | `useLocalStorage` menyimpan dan membaca data, `useBookStats` menghitung statistik |
| `App.test.jsx` | Integrasi: tambah + cari buku, edit + hapus buku, navigasi ke halaman Statistik |

### Laporan hasil test

![Hasil unit test](screenshots/hasil-test.png)
