"""Class Library: menyimpan dan mengelola koleksi item perpustakaan."""

from library_item import LibraryItem


class Library:
    """Perpustakaan yang menyimpan koleksi item.

    Koleksi disimpan di atribut private __koleksi (dictionary id -> item),
    jadi kode di luar kelas tidak bisa mengubahnya langsung.
    """

    def __init__(self, nama):
        """Membuat perpustakaan kosong.

        Parameter:
            nama (str): nama perpustakaan.
        """
        self.nama = nama
        self.__koleksi = {}

    @property
    def jumlah_item(self):
        """int: jumlah seluruh item di perpustakaan."""
        return len(self.__koleksi)

    def tambah_item(self, item):
        """Menambahkan item ke koleksi.

        Parameter:
            item (LibraryItem): item yang akan ditambahkan.

        Mengembalikan:
            bool: True jika berhasil, False jika id item sudah dipakai.

        Raises:
            TypeError: jika item bukan turunan LibraryItem.
        """
        if not isinstance(item, LibraryItem):
            raise TypeError("Item harus berupa turunan LibraryItem.")
        if item.id_item in self.__koleksi:
            return False
        self.__koleksi[item.id_item] = item
        return True

    def daftar_item(self, hanya_tersedia=True):
        """Mengambil daftar item.

        Parameter:
            hanya_tersedia (bool): True untuk item yang belum dipinjam saja,
                False untuk seluruh item.

        Mengembalikan:
            list: daftar item sesuai pilihan.
        """
        semua = list(self.__koleksi.values())
        if hanya_tersedia:
            return [item for item in semua if not item.is_dipinjam]
        return semua

    def tampilkan_katalog(self, hanya_tersedia=True):
        """Mencetak katalog item.

        Parameter:
            hanya_tersedia (bool): True untuk item yang tersedia saja.
        """
        judul = "tersedia" if hanya_tersedia else "seluruh koleksi"
        daftar = self.daftar_item(hanya_tersedia)
        print(f"Katalog {self.nama} ({judul}): {len(daftar)} item")
        if not daftar:
            print("  (kosong)")
        for item in daftar:
            print(f"  {item}")

    def cari_judul(self, kata_kunci):
        """Mencari item yang judulnya mengandung kata kunci.

        Pencarian tidak membedakan huruf besar dan kecil.

        Parameter:
            kata_kunci (str): kata yang dicari di judul.

        Mengembalikan:
            list: daftar item yang cocok (bisa kosong).
        """
        kata = kata_kunci.strip().lower()
        return [
            item for item in self.__koleksi.values()
            if kata in item.judul.lower()
        ]

    def cari_id(self, id_item):
        """Mencari satu item berdasarkan id.

        Parameter:
            id_item (str): kode item.

        Mengembalikan:
            LibraryItem atau None: item yang cocok, None jika tidak ada.
        """
        return self.__koleksi.get(id_item)
