"""Tugas 1: Program penghitung BMI (Body Mass Index)."""


def hitung_bmi(berat, tinggi):
    """Menghitung nilai BMI.

    Parameter:
        berat (float): berat badan dalam kilogram.
        tinggi (float): tinggi badan dalam meter.

    Mengembalikan:
        float: nilai BMI = berat / (tinggi * tinggi).
    """
    return berat / (tinggi * tinggi)


def tentukan_kategori(bmi):
    """Menentukan kategori berat badan berdasarkan nilai BMI.

    Parameter:
        bmi (float): nilai BMI.

    Mengembalikan:
        str: kategori berat badan.
    """
    if bmi < 18.5:
        return "Berat badan kurang"
    elif bmi < 25:
        return "Berat badan normal"
    elif bmi < 30:
        return "Berat badan berlebih"
    else:
        return "Obesitas"


def baca_angka(pesan):
    """Meminta input angka positif dari pengguna sampai valid.

    Parameter:
        pesan (str): teks yang ditampilkan saat meminta input.

    Mengembalikan:
        float: angka positif yang dimasukkan pengguna.
    """
    while True:
        try:
            angka = float(input(pesan).replace(",", "."))
        except ValueError:
            print("Input harus berupa angka. Coba lagi.")
            continue
        if angka <= 0:
            print("Angka harus lebih besar dari 0. Coba lagi.")
            continue
        return angka


def main():
    """Menjalankan program: baca input, hitung BMI, tampilkan hasil."""
    print("=== Penghitung BMI ===")
    berat = baca_angka("Berat badan (kg)  : ")
    tinggi = baca_angka("Tinggi badan (m)  : ")

    bmi = hitung_bmi(berat, tinggi)
    kategori = tentukan_kategori(bmi)

    print("-" * 30)
    print(f"BMI      : {bmi:.2f}")
    print(f"Kategori : {kategori}")


if __name__ == "__main__":
    main()
