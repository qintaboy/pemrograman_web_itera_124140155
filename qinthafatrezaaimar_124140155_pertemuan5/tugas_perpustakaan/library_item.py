"""Abstract class LibraryItem beserta subclass Book dan Magazine."""

from abc import ABC, abstractmethod


class LibraryItem(ABC):
    """Kelas dasar (abstract) untuk semua item perpustakaan.

    Kelas ini tidak bisa dibuat objeknya secara langsung. Subclass wajib
    mengimplementasikan get_detail(), hitung_denda(), dan masa_pinjam.
    """

    def __init__(self, id_item, judul, tahun_terbit):
        """Membuat item perpustakaan.

        Parameter:
            id_item (str): kode unik item, misalnya "B001".
            judul (str): judul item (tidak boleh kosong).
            tahun_terbit (int): tahun terbit item.
        """
        self._id_item = id_item          # protected: untuk kelas turunan
        self._tahun_terbit = tahun_terbit
        self.__dipinjam = False          # private: hanya diubah lewat method
        self._judul = ""
        self.judul = judul               # lewat setter, jadi divalidasi

    # --- Property (encapsulation) ---
    @property
    def id_item(self):
        """str: kode unik item (hanya bisa dibaca)."""
        return self._id_item

    @property
    def judul(self):
        """str: judul item."""
        return self._judul

    @judul.setter
    def judul(self, nilai):
        """Mengubah judul, menolak judul kosong."""
        if not str(nilai).strip():
            raise ValueError("Judul tidak boleh kosong.")
        self._judul = str(nilai).strip()

    @property
    def tahun_terbit(self):
        """int: tahun terbit item (hanya bisa dibaca)."""
        return self._tahun_terbit

    @property
    def is_dipinjam(self):
        """bool: True jika item sedang dipinjam (hanya bisa dibaca)."""
        return self.__dipinjam

    @property
    def status(self):
        """str: teks status ketersediaan item."""
        return "Dipinjam" if self.__dipinjam else "Tersedia"

    # --- Perilaku yang sama untuk semua item ---
    def pinjam(self):
        """Menandai item sebagai dipinjam.

        Mengembalikan:
            bool: True jika berhasil, False jika sudah dipinjam.
        """
        if self.__dipinjam:
            return False
        self.__dipinjam = True
        return True

    def kembalikan(self):
        """Menandai item sebagai sudah dikembalikan.

        Mengembalikan:
            bool: True jika berhasil, False jika item memang tidak dipinjam.
        """
        if not self.__dipinjam:
            return False
        self.__dipinjam = False
        return True

    # --- Kontrak untuk subclass (abstract) ---
    @property
    @abstractmethod
    def masa_pinjam(self):
        """int: lama peminjaman dalam hari (ditentukan tiap subclass)."""

    @abstractmethod
    def get_detail(self):
        """Mengembalikan rincian lengkap item dalam bentuk teks."""

    @abstractmethod
    def hitung_denda(self, hari_terlambat):
        """Menghitung denda keterlambatan.

        Parameter:
            hari_terlambat (int): jumlah hari terlambat.

        Mengembalikan:
            int: besar denda dalam rupiah.
        """

    # --- Representasi teks ---
    def __str__(self):
        """Ringkasan satu baris: [id] judul - status."""
        return f"[{self._id_item}] {self._judul} - {self.status}"

    def __repr__(self):
        """Representasi untuk debugging."""
        return f"{type(self).__name__}({self._id_item!r}, {self._judul!r})"


class Book(LibraryItem):
    """Buku: item perpustakaan dengan penulis dan jumlah halaman."""

    DENDA_PER_HARI = 1000

    def __init__(self, id_item, judul, tahun_terbit, penulis, jumlah_halaman):
        """Membuat buku.

        Parameter:
            id_item (str): kode unik buku.
            judul (str): judul buku.
            tahun_terbit (int): tahun terbit.
            penulis (str): nama penulis.
            jumlah_halaman (int): jumlah halaman.
        """
        super().__init__(id_item, judul, tahun_terbit)
        self._penulis = penulis
        self._jumlah_halaman = jumlah_halaman

    @property
    def penulis(self):
        """str: nama penulis (hanya bisa dibaca)."""
        return self._penulis

    @property
    def masa_pinjam(self):
        """int: buku boleh dipinjam 14 hari."""
        return 14

    def get_detail(self):
        """Rincian buku: judul, penulis, tahun, halaman, status."""
        return (
            f"Buku     : {self.judul}\n"
            f"Penulis  : {self._penulis}\n"
            f"Terbit   : {self._tahun_terbit} ({self._jumlah_halaman} hlm)\n"
            f"Status   : {self.status} (masa pinjam {self.masa_pinjam} hari)"
        )

    def hitung_denda(self, hari_terlambat):
        """Denda buku: Rp 1.000 per hari keterlambatan."""
        return max(0, hari_terlambat) * self.DENDA_PER_HARI


class Magazine(LibraryItem):
    """Majalah: item perpustakaan dengan nomor edisi dan penerbit."""

    DENDA_PER_HARI = 500

    def __init__(self, id_item, judul, tahun_terbit, nomor_edisi, penerbit):
        """Membuat majalah.

        Parameter:
            id_item (str): kode unik majalah.
            judul (str): judul majalah.
            tahun_terbit (int): tahun terbit.
            nomor_edisi (int): nomor edisi.
            penerbit (str): nama penerbit.
        """
        super().__init__(id_item, judul, tahun_terbit)
        self._nomor_edisi = nomor_edisi
        self._penerbit = penerbit

    @property
    def masa_pinjam(self):
        """int: majalah boleh dipinjam 7 hari."""
        return 7

    def get_detail(self):
        """Rincian majalah: judul, edisi, penerbit, tahun, status."""
        return (
            f"Majalah  : {self.judul}\n"
            f"Edisi    : {self._nomor_edisi} ({self._penerbit})\n"
            f"Terbit   : {self._tahun_terbit}\n"
            f"Status   : {self.status} (masa pinjam {self.masa_pinjam} hari)"
        )

    def hitung_denda(self, hari_terlambat):
        """Denda majalah: Rp 500 per hari keterlambatan."""
        return max(0, hari_terlambat) * self.DENDA_PER_HARI
