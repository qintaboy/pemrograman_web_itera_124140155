"""Class Member: anggota perpustakaan yang meminjam item."""


class Member:
    """Anggota perpustakaan.

    Data penting (nama dan daftar pinjaman) disimpan sebagai atribut private
    sehingga hanya bisa diubah lewat method milik kelas ini.
    """

    BATAS_PINJAM = 3  # maksimal item yang boleh dipinjam bersamaan

    def __init__(self, id_member, nama):
        """Membuat anggota.

        Parameter:
            id_member (str): kode unik anggota.
            nama (str): nama anggota (tidak boleh kosong).
        """
        self._id_member = id_member
        self.__nama = ""
        self.__daftar_pinjam = []
        self.nama = nama  # lewat setter, jadi divalidasi

    @property
    def id_member(self):
        """str: kode anggota (hanya bisa dibaca)."""
        return self._id_member

    @property
    def nama(self):
        """str: nama anggota."""
        return self.__nama

    @nama.setter
    def nama(self, nilai):
        """Mengubah nama, menolak nama kosong."""
        if not str(nilai).strip():
            raise ValueError("Nama anggota tidak boleh kosong.")
        self.__nama = str(nilai).strip()

    @property
    def jumlah_pinjaman(self):
        """int: jumlah item yang sedang dipinjam."""
        return len(self.__daftar_pinjam)

    def pinjam_item(self, item):
        """Meminjam sebuah item.

        Parameter:
            item (LibraryItem): item yang ingin dipinjam.

        Mengembalikan:
            tuple: (berhasil, pesan) dengan berhasil bertipe bool.
        """
        if self.jumlah_pinjaman >= self.BATAS_PINJAM:
            return False, (
                f"{self.nama} sudah mencapai batas "
                f"{self.BATAS_PINJAM} pinjaman."
            )
        if not item.pinjam():
            return False, f"'{item.judul}' sedang dipinjam orang lain."
        self.__daftar_pinjam.append(item)
        return True, (
            f"{self.nama} meminjam '{item.judul}' "
            f"(batas {item.masa_pinjam} hari)."
        )

    def kembalikan_item(self, item, hari_terlambat=0):
        """Mengembalikan sebuah item dan menghitung dendanya.

        Parameter:
            item (LibraryItem): item yang dikembalikan.
            hari_terlambat (int): jumlah hari terlambat (0 jika tepat waktu).

        Mengembalikan:
            tuple: (berhasil, pesan, denda) dengan denda dalam rupiah.
        """
        if item not in self.__daftar_pinjam:
            return False, f"{self.nama} tidak meminjam '{item.judul}'.", 0
        item.kembalikan()
        self.__daftar_pinjam.remove(item)
        denda = item.hitung_denda(hari_terlambat)
        return True, f"'{item.judul}' dikembalikan oleh {self.nama}.", denda

    def tampilkan_pinjaman(self):
        """Menampilkan daftar item yang sedang dipinjam anggota ini."""
        print(f"Pinjaman {self.nama} ({self.jumlah_pinjaman} item):")
        if not self.__daftar_pinjam:
            print("  (tidak ada)")
        for item in self.__daftar_pinjam:
            print(f"  - {item.judul}")

    def __str__(self):
        """Ringkasan anggota: [id] nama."""
        return f"[{self._id_member}] {self.__nama}"
