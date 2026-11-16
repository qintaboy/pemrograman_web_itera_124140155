"""Hands-on 2: perbandingan pendekatan prosedural dan OOP."""

# ---------- Pendekatan prosedural ----------
# Data (dictionary) dan fungsi dipisah; fungsi harus diberi datanya.
mahasiswa_prosedural = {"nama": "Andi", "ipk": 3.20}


def update_ipk_prosedural(data, ipk_baru):
    """Mengubah IPK pada dictionary mahasiswa.

    Parameter:
        data (dict): data mahasiswa.
        ipk_baru (float): IPK baru.
    """
    data["ipk"] = ipk_baru


def tampilkan_prosedural(data):
    """Mencetak data mahasiswa dari dictionary.

    Parameter:
        data (dict): data mahasiswa.
    """
    print(f"{data['nama']} - IPK {data['ipk']:.2f}")


print("--- Prosedural ---")
tampilkan_prosedural(mahasiswa_prosedural)
update_ipk_prosedural(mahasiswa_prosedural, 3.55)
tampilkan_prosedural(mahasiswa_prosedural)


# ---------- Pendekatan OOP ----------
# Data dan perilaku digabung dalam satu class.
class Mahasiswa:
    """Mahasiswa dengan data dan perilakunya dalam satu tempat."""

    def __init__(self, nama, ipk):
        """Membuat mahasiswa.

        Parameter:
            nama (str): nama mahasiswa.
            ipk (float): IPK awal.
        """
        self.nama = nama
        self.ipk = ipk

    def update_ipk(self, ipk_baru: float):
        """Mengubah IPK mahasiswa ini.

        Parameter:
            ipk_baru (float): IPK baru.
        """
        self.ipk = ipk_baru

    def tampilkan(self):
        """Mencetak data mahasiswa ini."""
        print(f"{self.nama} - IPK {self.ipk:.2f}")


print()
print("--- OOP ---")
andi = Mahasiswa("Andi", 3.20)
andi.tampilkan()
andi.update_ipk(3.55)
andi.tampilkan()

print()
print("Perbedaan: pada OOP, data (nama, ipk) dan perilaku (update_ipk,")
print("tampilkan) menyatu dalam objek, sehingga tidak perlu mengoper data.")
