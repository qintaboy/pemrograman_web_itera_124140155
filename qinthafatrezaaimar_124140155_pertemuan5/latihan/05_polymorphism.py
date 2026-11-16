"""Hands-on 6: polymorphism, duck typing, dan operator overloading."""


def rupiah(jumlah):
    """Memformat angka menjadi teks rupiah, contoh "Rp 102.500".

    Parameter:
        jumlah (int): nominal dalam rupiah.

    Mengembalikan:
        str: teks rupiah dengan titik pemisah ribuan.
    """
    return "Rp " + f"{jumlah:,}".replace(",", ".")


class MetodePembayaran:
    """Kelas induk: semua metode pembayaran punya method bayar()."""

    def bayar(self, jumlah):
        """Memproses pembayaran (diisi oleh subclass).

        Parameter:
            jumlah (int): total yang dibayar.
        """
        raise NotImplementedError("Subclass harus mengimplementasikan bayar()")


class TransferBank(MetodePembayaran):
    """Pembayaran lewat transfer bank (biaya admin tetap)."""

    def bayar(self, jumlah):
        """Membayar via transfer dengan biaya admin Rp 2.500."""
        total = jumlah + 2500
        return f"Transfer bank   : {rupiah(total)} (termasuk admin 2.500)"


class EWallet(MetodePembayaran):
    """Pembayaran lewat dompet digital (cashback 5%)."""

    def bayar(self, jumlah):
        """Membayar via e-wallet dengan cashback 5%."""
        cashback = int(jumlah * 0.05)
        return (
            f"E-wallet        : {rupiah(jumlah)} "
            f"(cashback {rupiah(cashback)})"
        )


class KartuKredit(MetodePembayaran):
    """Pembayaran lewat kartu kredit (biaya layanan 2%)."""

    def bayar(self, jumlah):
        """Membayar via kartu kredit dengan biaya 2%."""
        total = int(jumlah * 1.02)
        return f"Kartu kredit    : {rupiah(total)} (biaya layanan 2%)"


class Tunai:
    """Tidak mewarisi MetodePembayaran, tetapi punya method bayar()."""

    def bayar(self, jumlah):
        """Membayar tunai tanpa biaya tambahan."""
        return f"Tunai           : {rupiah(jumlah)} (tanpa biaya)"


class Uang:
    """Nominal uang yang mendukung operator + dan ==."""

    def __init__(self, nominal):
        """Membuat uang.

        Parameter:
            nominal (int): jumlah rupiah.
        """
        self.nominal = nominal

    def __add__(self, lain):
        """Operator +: menjumlahkan dua objek Uang."""
        return Uang(self.nominal + lain.nominal)

    def __eq__(self, lain):
        """Operator ==: dua Uang sama jika nominalnya sama."""
        return self.nominal == lain.nominal

    def __str__(self):
        """Teks nominal berformat ribuan."""
        return rupiah(self.nominal)


def proses_pembayaran(daftar_opsi, total_belanja):
    """Memanggil bayar() pada setiap opsi tanpa if-elif-else.

    Parameter:
        daftar_opsi (list): objek apa pun yang punya method bayar().
        total_belanja (int): total yang dibayar.
    """
    for opsi in daftar_opsi:
        print(opsi.bayar(total_belanja))


opsi_pembayaran = [TransferBank(), EWallet(), KartuKredit(), Tunai()]

print("--- Polymorphism: bayar() yang sama, hasil berbeda ---")
proses_pembayaran(opsi_pembayaran, 100_000)

print()
print("--- Duck typing: Tunai tidak mewarisi, tetap bisa dipakai ---")
print("Tunai turunan MetodePembayaran?", isinstance(Tunai(), MetodePembayaran))

print()
print("--- Operator overloading ---")
a = Uang(50_000)
b = Uang(25_000)
print("a + b      :", a + b)
print("a == b     :", a == b)
print("a == Uang(50000):", a == Uang(50_000))
