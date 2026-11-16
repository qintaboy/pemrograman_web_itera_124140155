"""Hands-on 4: inheritance (pewarisan), override, super(), dan MRO."""


class Kendaraan:
    """Kelas induk untuk semua kendaraan."""

    def __init__(self, merek, model, tahun):
        """Membuat kendaraan.

        Parameter:
            merek (str): merek kendaraan.
            model (str): model kendaraan.
            tahun (int): tahun produksi.
        """
        self.merek = merek
        self.model = model
        self.tahun = tahun

    def deskripsi(self):
        """Mengembalikan deskripsi umum kendaraan."""
        return f"{self.merek} {self.model} ({self.tahun})"

    def bunyi(self):
        """Mengembalikan bunyi umum kendaraan."""
        return "Brum..."


class Mobil(Kendaraan):
    """Mobil: kendaraan dengan jumlah pintu."""

    def __init__(self, merek, model, tahun, jumlah_pintu):
        """Membuat mobil.

        Parameter:
            merek (str): merek mobil.
            model (str): model mobil.
            tahun (int): tahun produksi.
            jumlah_pintu (int): jumlah pintu.
        """
        super().__init__(merek, model, tahun)  # memanggil constructor induk
        self.jumlah_pintu = jumlah_pintu

    def deskripsi(self):
        """Override: menambahkan jumlah pintu pada deskripsi."""
        return f"{super().deskripsi()}, {self.jumlah_pintu} pintu"

    def bunyi(self):
        """Override: bunyi khas mobil."""
        return "Tin tin!"


class Motor(Kendaraan):
    """Motor: kendaraan dengan jenis mesin."""

    def __init__(self, merek, model, tahun, jenis):
        """Membuat motor.

        Parameter:
            merek (str): merek motor.
            model (str): model motor.
            tahun (int): tahun produksi.
            jenis (str): jenis motor, misalnya "matic".
        """
        super().__init__(merek, model, tahun)
        self.jenis = jenis

    def bunyi(self):
        """Override: bunyi khas motor."""
        return "Brmm brmm!"


class MobilListrik(Mobil):
    """Mobil listrik: turunan dari Mobil (pewarisan bertingkat)."""

    def __init__(self, merek, model, tahun, jumlah_pintu, kapasitas_baterai):
        """Membuat mobil listrik.

        Parameter:
            merek (str): merek mobil.
            model (str): model mobil.
            tahun (int): tahun produksi.
            jumlah_pintu (int): jumlah pintu.
            kapasitas_baterai (int): kapasitas baterai dalam kWh.
        """
        super().__init__(merek, model, tahun, jumlah_pintu)
        self.kapasitas_baterai = kapasitas_baterai

    def deskripsi(self):
        """Override: menambahkan kapasitas baterai."""
        return f"{super().deskripsi()}, baterai {self.kapasitas_baterai} kWh"

    def bunyi(self):
        """Override: mobil listrik nyaris tanpa suara."""
        return "Ssshhh..."


kendaraan_list = [
    Kendaraan("Generik", "Umum", 2000),
    Mobil("Toyota", "Avanza", 2022, 5),
    Motor("Honda", "Vario", 2023, "matic"),
    MobilListrik("Hyundai", "Ioniq 5", 2024, 5, 72),
]

print("--- Deskripsi dan bunyi tiap kendaraan ---")
for kendaraan in kendaraan_list:
    print(f"{kendaraan.deskripsi()}")
    print(f"   bunyi: {kendaraan.bunyi()}")

print()
print("--- MRO (urutan pencarian method) ---")
for kelas in MobilListrik.__mro__:
    print(" ->", kelas.__name__)

print()
print("--- isinstance dan issubclass ---")
listrik = kendaraan_list[3]
print("listrik adalah MobilListrik? :", isinstance(listrik, MobilListrik))
print("listrik adalah Mobil?        :", isinstance(listrik, Mobil))
print("listrik adalah Motor?        :", isinstance(listrik, Motor))
print("MobilListrik turunan Kendaraan?:", issubclass(MobilListrik, Kendaraan))
