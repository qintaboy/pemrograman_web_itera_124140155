"""Hands-on 3: class dan object (atribut class, atribut instance, dunder)."""


class Mahasiswa:
    """Mahasiswa dengan penghitung jumlah objek yang pernah dibuat."""

    # Atribut class: dimiliki bersama oleh semua objek
    universitas = "Institut Teknologi Sumatera"
    total_mahasiswa_terdaftar = 0

    def __init__(self, nama, nim, ipk=0.0):
        """Constructor: dipanggil otomatis saat objek dibuat.

        Parameter:
            nama (str): nama mahasiswa.
            nim (str): NIM mahasiswa.
            ipk (float): IPK awal.
        """
        # Atribut instance: milik masing-masing objek
        self.nama = nama
        self.nim = nim
        self.ipk = ipk
        Mahasiswa.total_mahasiswa_terdaftar += 1

    def perkenalan(self):
        """Mengembalikan kalimat perkenalan."""
        return f"Halo, saya {self.nama} dari {self.universitas}."

    def __str__(self):
        """Teks ramah pengguna, dipakai oleh print()."""
        return f"{self.nama} ({self.nim}) - IPK {self.ipk:.2f}"

    def __repr__(self):
        """Teks untuk debugging, menampilkan cara membuat objeknya."""
        return f"Mahasiswa({self.nama!r}, {self.nim!r}, {self.ipk})"


print("Terdaftar awal :", Mahasiswa.total_mahasiswa_terdaftar)

mhs1 = Mahasiswa("Andi", "124140101", 3.50)
mhs2 = Mahasiswa("Bunga", "124140102", 3.75)

print("Terdaftar kini :", Mahasiswa.total_mahasiswa_terdaftar)
print()
print(mhs1.perkenalan())
print(mhs2.perkenalan())
print()
print("str() :", str(mhs1))
print("repr():", repr(mhs1))
print()

# Mengubah atribut instance hanya memengaruhi objek itu sendiri
mhs1.ipk = 3.90
print("IPK mhs1:", mhs1.ipk, "| IPK mhs2:", mhs2.ipk)

# Atribut class bisa dibaca lewat class maupun objek
print("Universitas lewat class :", Mahasiswa.universitas)
print("Universitas lewat objek :", mhs2.universitas)
