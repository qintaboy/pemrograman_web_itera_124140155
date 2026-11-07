"""Tugas 2: Program pengelolaan data nilai mahasiswa."""

# Bobot penilaian (jumlahnya 100%)
BOBOT_UTS = 0.30
BOBOT_UAS = 0.40
BOBOT_TUGAS = 0.30

# Data mahasiswa: list berisi dictionary
DATA_MAHASISWA = [
    {"nama": "Sahal", "nim": "123123123",
     "nilai_uts": 85, "nilai_uas": 90, "nilai_tugas": 88},
    {"nama": "Grista", "nim": "123123120",
     "nilai_uts": 72, "nilai_uas": 68, "nilai_tugas": 80},
    {"nama": "Nopal", "nim": "123123122",
     "nilai_uts": 60, "nilai_uas": 55, "nilai_tugas": 65},
    {"nama": "Bit", "nim": "123123121",
     "nilai_uts": 45, "nilai_uas": 50, "nilai_tugas": 40},
    {"nama": "Utara", "nim": "123123124",
     "nilai_uts": 78, "nilai_uas": 82, "nilai_tugas": 75},
    {"nama": "Farhan Kebab", "nim": "123123069",
     "nilai_uts": 30, "nilai_uas": 42, "nilai_tugas": 48},
]


def hitung_nilai_akhir(mahasiswa):
    """Menghitung nilai akhir seorang mahasiswa.

    Rumus: 30% UTS + 40% UAS + 30% Tugas.

    Parameter:
        mahasiswa (dict): data mahasiswa dengan kunci nilai_uts,
            nilai_uas, dan nilai_tugas.

    Mengembalikan:
        float: nilai akhir.
    """
    return (
        BOBOT_UTS * mahasiswa["nilai_uts"]
        + BOBOT_UAS * mahasiswa["nilai_uas"]
        + BOBOT_TUGAS * mahasiswa["nilai_tugas"]
    )


def tentukan_grade(nilai_akhir):
    """Menentukan grade huruf dari nilai akhir.

    Parameter:
        nilai_akhir (float): nilai akhir mahasiswa.

    Mengembalikan:
        str: grade A, B, C, D, atau E.
    """
    if nilai_akhir >= 80:
        return "A"
    elif nilai_akhir >= 70:
        return "B"
    elif nilai_akhir >= 60:
        return "C"
    elif nilai_akhir >= 50:
        return "D"
    else:
        return "E"


def proses_data(daftar):
    """Menambahkan kunci nilai_akhir dan grade ke setiap mahasiswa.

    Parameter:
        daftar (list): list dictionary mahasiswa.

    Mengembalikan:
        list: list dictionary baru yang sudah berisi nilai_akhir dan grade.
    """
    hasil = []
    for mhs in daftar:
        nilai_akhir = hitung_nilai_akhir(mhs)
        # {**mhs, ...} menyalin dictionary lama lalu menambah kunci baru
        hasil.append({
            **mhs,
            "nilai_akhir": nilai_akhir,
            "grade": tentukan_grade(nilai_akhir),
        })
    return hasil


def tampilkan_tabel(daftar):
    """Menampilkan tabel Nama, NIM, Nilai Akhir, dan Grade.

    Parameter:
        daftar (list): list dictionary yang sudah memiliki nilai_akhir
            dan grade.
    """
    garis = "-" * 56
    print(garis)
    print(f"{'No':<4}{'Nama':<20}{'NIM':<12}{'Nilai Akhir':>12}{'Grade':>8}")
    print(garis)
    for nomor, mhs in enumerate(daftar, start=1):
        print(
            f"{nomor:<4}{mhs['nama']:<20}{mhs['nim']:<12}"
            f"{mhs['nilai_akhir']:>12.2f}{mhs['grade']:>8}"
        )
    print(garis)


def tampilkan_ekstrem(daftar):
    """Menampilkan mahasiswa dengan nilai akhir tertinggi dan terendah.

    Parameter:
        daftar (list): list dictionary yang sudah memiliki nilai_akhir.
    """
    tertinggi = max(daftar, key=lambda mhs: mhs["nilai_akhir"])
    terendah = min(daftar, key=lambda mhs: mhs["nilai_akhir"])

    print(
        f"Nilai tertinggi : {tertinggi['nama']} ({tertinggi['nim']}) "
        f"- {tertinggi['nilai_akhir']:.2f} [{tertinggi['grade']}]"
    )
    print(
        f"Nilai terendah  : {terendah['nama']} ({terendah['nim']}) "
        f"- {terendah['nilai_akhir']:.2f} [{terendah['grade']}]"
    )


def main():
    """Menjalankan program pengelolaan nilai mahasiswa."""
    print("=== Data Nilai Mahasiswa ===")
    daftar = proses_data(DATA_MAHASISWA)
    tampilkan_tabel(daftar)
    tampilkan_ekstrem(daftar)


if __name__ == "__main__":
    main()
