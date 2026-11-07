"""Modul operasi matematika: luas, keliling, dan konversi suhu."""

# Konstanta
PI = 3.14159


# --- Persegi ---
def luas_persegi(sisi):
    """Menghitung luas persegi.

    Parameter:
        sisi (float): panjang sisi persegi.

    Mengembalikan:
        float: luas persegi (sisi * sisi).
    """
    return sisi * sisi


def keliling_persegi(sisi):
    """Menghitung keliling persegi.

    Parameter:
        sisi (float): panjang sisi persegi.

    Mengembalikan:
        float: keliling persegi (4 * sisi).
    """
    return 4 * sisi


# --- Persegi panjang ---
def luas_persegi_panjang(panjang, lebar):
    """Menghitung luas persegi panjang.

    Parameter:
        panjang (float): panjang persegi panjang.
        lebar (float): lebar persegi panjang.

    Mengembalikan:
        float: luas persegi panjang (panjang * lebar).
    """
    return panjang * lebar


def keliling_persegi_panjang(panjang, lebar):
    """Menghitung keliling persegi panjang.

    Parameter:
        panjang (float): panjang persegi panjang.
        lebar (float): lebar persegi panjang.

    Mengembalikan:
        float: keliling persegi panjang (2 * (panjang + lebar)).
    """
    return 2 * (panjang + lebar)


# --- Lingkaran ---
def luas_lingkaran(jari_jari):
    """Menghitung luas lingkaran.

    Parameter:
        jari_jari (float): jari-jari lingkaran.

    Mengembalikan:
        float: luas lingkaran (PI * jari_jari * jari_jari).
    """
    return PI * jari_jari * jari_jari


def keliling_lingkaran(jari_jari):
    """Menghitung keliling lingkaran.

    Parameter:
        jari_jari (float): jari-jari lingkaran.

    Mengembalikan:
        float: keliling lingkaran (2 * PI * jari_jari).
    """
    return 2 * PI * jari_jari


# --- Konversi suhu ---
def celsius_ke_fahrenheit(celsius):
    """Mengonversi suhu dari Celsius ke Fahrenheit.

    Parameter:
        celsius (float): suhu dalam derajat Celsius.

    Mengembalikan:
        float: suhu dalam derajat Fahrenheit.
    """
    return celsius * 9 / 5 + 32


def celsius_ke_kelvin(celsius):
    """Mengonversi suhu dari Celsius ke Kelvin.

    Parameter:
        celsius (float): suhu dalam derajat Celsius.

    Mengembalikan:
        float: suhu dalam Kelvin.
    """
    return celsius + 273.15
