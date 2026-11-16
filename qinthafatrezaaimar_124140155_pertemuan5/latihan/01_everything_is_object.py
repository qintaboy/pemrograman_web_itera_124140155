"""Hands-on 1: di Python, semua nilai adalah objek."""


def sapa():
    """Fungsi sederhana (fungsi pun adalah objek)."""
    return "Halo"


class Contoh:
    """Class kosong (class pun adalah objek)."""


angka = 42
teks = "Python"
daftar = [1, 2, 3]

objek_objek = {
    "angka": angka,
    "teks": teks,
    "daftar": daftar,
    "sapa": sapa,
    "Contoh": Contoh,
}

print("--- Tipe dan identitas objek ---")
for nama, objek in objek_objek.items():
    print(f"{nama:<8} tipe: {type(objek).__name__:<9} id: {id(objek)}")

print()
print("--- Objek punya method dan atribut ---")
print("Tipe objek 'angka'        :", type(angka), "| Class:", angka.__class__)
print("angka.bit_length()        :", angka.bit_length())
print("teks.upper()              :", teks.upper())
print("daftar setelah append(4)  :", end=" ")
daftar.append(4)
print(daftar)

print()
print("--- Semuanya turunan dari object ---")
for nama, objek in objek_objek.items():
    print(f"{nama:<8} isinstance(object)? {isinstance(objek, object)}")
