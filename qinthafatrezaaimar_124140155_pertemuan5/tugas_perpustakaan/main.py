"""Program utama: menguji sistem manajemen perpustakaan sederhana."""

from library import Library
from library_item import Book, LibraryItem, Magazine
from member import Member


def format_rupiah(jumlah):
    """Memformat angka menjadi teks rupiah dengan titik pemisah ribuan.

    Parameter:
        jumlah (int): nominal dalam rupiah.

    Mengembalikan:
        str: contoh "Rp 5.000".
    """
    return "Rp " + f"{jumlah:,}".replace(",", ".")


def judul_bagian(nomor, teks):
    """Mencetak judul bagian agar output mudah dibaca.

    Parameter:
        nomor (int): nomor bagian.
        teks (str): judul bagian.
    """
    print()
    print(f"=== {nomor}. {teks} ===")


def buat_perpustakaan():
    """Membuat perpustakaan berisi dua buku dan dua majalah.

    Mengembalikan:
        Library: perpustakaan yang sudah terisi.
    """
    perpus = Library("Perpustakaan ITERA")
    daftar = [
        Book("B001", "Pemrograman Python Dasar", 2022,
             "Budiono Siregar", 320),
        Book("B002", "Algoritma dan Struktur Data", 2020,
             "My Bini Yujin", 450),
        Magazine("M001", "Majalah Teknologi Python", 2024, 12,
                 "My Bini Gaeul"),
        Magazine("M002", "Majalah Sains Populer", 2023, 5,
                 "Pustaka Ilmu"),
    ]
    for item in daftar:
        berhasil = perpus.tambah_item(item)
        print(f"Tambah  {item.id_item} {item.judul:<30} -> "
              f"{'berhasil' if berhasil else 'gagal'}")
    return perpus


def uji_penambahan_dan_katalog():
    """Bagian 1 dan 2: menambah item lalu menampilkan katalog.

    Mengembalikan:
        Library: perpustakaan yang dipakai bagian berikutnya.
    """
    judul_bagian(1, "MENAMBAH ITEM")
    perpus = buat_perpustakaan()

    duplikat = Book("B001", "Buku Dengan Id Kembar", 2021, "Anonim", 100)
    berhasil = perpus.tambah_item(duplikat)
    print(f"Tambah  {duplikat.id_item} {'(id kembar)':<30} -> "
          f"{'berhasil' if berhasil else 'gagal (id sudah dipakai)'}")

    judul_bagian(2, "MENAMPILKAN KATALOG")
    perpus.tampilkan_katalog()
    return perpus


def uji_pencarian(perpus):
    """Bagian 3: mencari item berdasarkan judul dan id.

    Parameter:
        perpus (Library): perpustakaan yang dicari.
    """
    judul_bagian(3, "MENCARI ITEM")

    print("Cari judul 'python':")
    for item in perpus.cari_judul("python"):
        print(f"  {item}")

    print("Cari judul 'matematika':")
    hasil = perpus.cari_judul("matematika")
    print("  (tidak ada)" if not hasil else f"  {hasil}")

    print("Cari id 'M002':")
    item = perpus.cari_id("M002")
    print(f"  {item}" if item else "  (tidak ditemukan)")

    print("Cari id 'X999':")
    item = perpus.cari_id("X999")
    print(f"  {item}" if item else "  (tidak ditemukan)")


def uji_peminjaman(perpus):
    """Bagian 4: meminjam dan mengembalikan item beserta dendanya.

    Parameter:
        perpus (Library): perpustakaan tempat item dipinjam.
    """
    judul_bagian(4, "PEMINJAMAN DAN DENDA")
    anggota = Member("A001", "Qintaboy")
    buku = perpus.cari_id("B001")
    majalah = perpus.cari_id("M001")

    for item in (buku, majalah, buku):
        _, pesan = anggota.pinjam_item(item)
        print(pesan)

    print()
    anggota.tampilkan_pinjaman()
    print()
    perpus.tampilkan_katalog()

    print()
    for item, terlambat in ((buku, 5), (majalah, 0)):
        _, pesan, denda = anggota.kembalikan_item(item, terlambat)
        print(f"{pesan} Terlambat {terlambat} hari, "
              f"denda {format_rupiah(denda)}")


def uji_polimorfisme(perpus):
    """Bagian 5: method yang sama memberi hasil berbeda tiap subclass.

    Parameter:
        perpus (Library): perpustakaan yang itemnya dipakai.
    """
    judul_bagian(5, "POLIMORFISME")
    for item in perpus.daftar_item(hanya_tersedia=False):
        print(item.get_detail())
        print(f"Denda 3 hari: {format_rupiah(item.hitung_denda(3))}")
        print("-" * 40)


def uji_enkapsulasi(perpus):
    """Bagian 6: membuktikan data dilindungi dan class abstract terkunci.

    Parameter:
        perpus (Library): perpustakaan yang diuji.
    """
    judul_bagian(6, "ENKAPSULASI DAN ABSTRACT CLASS")

    try:
        print(perpus.__koleksi)
    except AttributeError as galat:
        print(f"Akses __koleksi langsung ditolak : {galat}")

    try:
        perpus.cari_id("B001").judul = "   "
    except ValueError as galat:
        print(f"Judul kosong ditolak              : {galat}")

    try:
        perpus.cari_id("B001").is_dipinjam = True
    except AttributeError as galat:
        print(f"is_dipinjam hanya bisa dibaca     : {galat}")

    try:
        LibraryItem("X001", "Item Abstrak", 2024)
    except TypeError as galat:
        print(f"LibraryItem tidak bisa dibuat     : {galat}")


def main():
    """Menjalankan seluruh pengujian sistem perpustakaan."""
    perpus = uji_penambahan_dan_katalog()
    uji_pencarian(perpus)
    uji_peminjaman(perpus)
    uji_polimorfisme(perpus)
    uji_enkapsulasi(perpus)


if __name__ == "__main__":
    main()
