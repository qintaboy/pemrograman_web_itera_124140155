"""Program utama: memakai modul math_operations."""

# Cara impor 1: impor seluruh modul, fungsinya dipanggil lewat nama modul
import math_operations

# Cara impor 2: impor langsung nama tertentu dari modul
from math_operations import PI, celsius_ke_fahrenheit, celsius_ke_kelvin


def tampilkan_persegi():
    """Menguji fungsi luas dan keliling persegi dengan beberapa nilai."""
    print("--- Persegi ---")
    for sisi in (4, 7.5, 10):
        luas = math_operations.luas_persegi(sisi)
        keliling = math_operations.keliling_persegi(sisi)
        print(
            f"Sisi {sisi:<5} -> "
            f"luas = {luas:>7.2f}, keliling = {keliling:>6.2f}"
        )


def tampilkan_persegi_panjang():
    """Menguji fungsi luas dan keliling persegi panjang."""
    print("--- Persegi Panjang ---")
    for panjang, lebar in ((5, 3), (8, 2.5), (12, 6)):
        luas = math_operations.luas_persegi_panjang(panjang, lebar)
        keliling = math_operations.keliling_persegi_panjang(panjang, lebar)
        print(
            f"{panjang:>2} x {lebar:<4} -> "
            f"luas = {luas:>7.2f}, keliling = {keliling:>6.2f}"
        )


def tampilkan_lingkaran():
    """Menguji fungsi luas dan keliling lingkaran."""
    print("--- Lingkaran ---")
    for jari_jari in (3, 7, 10.5):
        luas = math_operations.luas_lingkaran(jari_jari)
        keliling = math_operations.keliling_lingkaran(jari_jari)
        print(
            f"r = {jari_jari:<5} -> "
            f"luas = {luas:>7.2f}, keliling = {keliling:>6.2f}"
        )


def tampilkan_suhu():
    """Menguji fungsi konversi suhu (memakai impor langsung)."""
    print("--- Konversi Suhu ---")
    for celsius in (0, 37, 100):
        fahrenheit = celsius_ke_fahrenheit(celsius)
        kelvin = celsius_ke_kelvin(celsius)
        print(
            f"{celsius:>3} C -> {fahrenheit:>6.2f} F, {kelvin:>6.2f} K"
        )


def main():
    """Menjalankan seluruh pengujian fungsi modul."""
    print("=== Uji Modul math_operations ===")
    print(f"Konstanta PI = {PI}")
    print()
    tampilkan_persegi()
    print()
    tampilkan_persegi_panjang()
    print()
    tampilkan_lingkaran()
    print()
    tampilkan_suhu()


if __name__ == "__main__":
    main()
