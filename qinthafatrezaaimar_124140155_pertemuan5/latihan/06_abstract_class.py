"""Hands-on 7: abstract class dan interface memakai modul abc."""

import math
from abc import ABC, abstractmethod


class Shape(ABC):
    """Bangun datar abstrak: kontrak untuk semua bentuk."""

    def __init__(self, nama):
        """Membuat bentuk.

        Parameter:
            nama (str): nama bentuk.
        """
        self.nama = nama

    @abstractmethod
    def luas(self):
        """Menghitung luas (wajib diimplementasikan subclass)."""

    @abstractmethod
    def keliling(self):
        """Menghitung keliling (wajib diimplementasikan subclass)."""

    def info(self):
        """Method biasa: boleh dipakai langsung oleh semua subclass."""
        return (
            f"{self.nama:<16} luas = {self.luas():>8.2f}, "
            f"keliling = {self.keliling():>7.2f}"
        )


class Lingkaran(Shape):
    """Lingkaran dengan jari-jari tertentu."""

    def __init__(self, jari_jari):
        """Membuat lingkaran.

        Parameter:
            jari_jari (float): jari-jari lingkaran.
        """
        super().__init__("Lingkaran")
        self.jari_jari = jari_jari

    def luas(self):
        """Luas lingkaran: pi * r * r."""
        return math.pi * self.jari_jari ** 2

    def keliling(self):
        """Keliling lingkaran: 2 * pi * r."""
        return 2 * math.pi * self.jari_jari


class PersegiPanjang(Shape):
    """Persegi panjang dengan panjang dan lebar."""

    def __init__(self, panjang, lebar):
        """Membuat persegi panjang.

        Parameter:
            panjang (float): panjang sisi.
            lebar (float): lebar sisi.
        """
        super().__init__("Persegi Panjang")
        self.panjang = panjang
        self.lebar = lebar

    def luas(self):
        """Luas persegi panjang: panjang * lebar."""
        return self.panjang * self.lebar

    def keliling(self):
        """Keliling persegi panjang: 2 * (panjang + lebar)."""
        return 2 * (self.panjang + self.lebar)


class DatabaseConnector(ABC):
    """Interface koneksi database: hanya berisi method abstract."""

    @abstractmethod
    def connect(self):
        """Membuka koneksi ke database."""

    @abstractmethod
    def query(self, perintah):
        """Menjalankan perintah ke database.

        Parameter:
            perintah (str): perintah yang dijalankan.
        """

    @abstractmethod
    def close(self):
        """Menutup koneksi database."""


class SQLiteConnector(DatabaseConnector):
    """Implementasi tiruan DatabaseConnector untuk SQLite."""

    def connect(self):
        """Membuka koneksi (tiruan)."""
        print("SQLite: koneksi dibuka")

    def query(self, perintah):
        """Menjalankan perintah (tiruan)."""
        print(f"SQLite: menjalankan -> {perintah}")

    def close(self):
        """Menutup koneksi (tiruan)."""
        print("SQLite: koneksi ditutup")


print("--- Class abstract tidak bisa dibuat objeknya ---")
try:
    Shape("Bentuk")
except TypeError as galat:
    print("Shape('Bentuk') ->", galat)

print()
print("--- Subclass yang mengimplementasikan semua abstract method ---")
for bentuk in (Lingkaran(7), PersegiPanjang(8, 5)):
    print(bentuk.info())

print()
print("--- Subclass yang belum lengkap tetap ditolak ---")


class SetengahJadi(Shape):
    """Hanya mengimplementasikan luas(), keliling() belum."""

    def luas(self):
        """Luas tetap (hanya untuk contoh)."""
        return 1


try:
    SetengahJadi("Belum Lengkap")
except TypeError as galat:
    print("SetengahJadi ->", galat)

print()
print("--- Interface DatabaseConnector ---")
db = SQLiteConnector()
db.connect()
db.query("SELECT * FROM mahasiswa")
db.close()
