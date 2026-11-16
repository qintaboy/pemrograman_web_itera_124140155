"""Hands-on 5: encapsulation (public, protected, private) dan property."""


class RekeningBank:
    """Rekening bank dengan saldo yang dilindungi."""

    def __init__(self, pemilik, nomor, saldo_awal=0.0):
        """Membuat rekening.

        Parameter:
            pemilik (str): nama pemilik rekening (public).
            nomor (str): nomor rekening (protected).
            saldo_awal (float): saldo awal, negatif dianggap 0 (private).
        """
        self.pemilik = pemilik                         # public
        self._nomor = nomor                            # protected
        self.__saldo = max(0.0, float(saldo_awal))     # private

    @property
    def saldo(self):
        """float: saldo saat ini (hanya bisa dibaca dari luar)."""
        return self.__saldo

    @property
    def nomor(self):
        """str: nomor rekening yang disamarkan sebagian."""
        return "*" * (len(self._nomor) - 3) + self._nomor[-3:]

    def setor(self, jumlah):
        """Menambah saldo.

        Parameter:
            jumlah (float): nominal setoran, harus lebih dari 0.

        Raises:
            ValueError: jika jumlah tidak positif.
        """
        if jumlah <= 0:
            raise ValueError("Jumlah setoran harus lebih dari 0.")
        self.__saldo += jumlah

    def tarik(self, jumlah):
        """Mengurangi saldo.

        Parameter:
            jumlah (float): nominal penarikan, harus lebih dari 0.

        Raises:
            ValueError: jika jumlah tidak positif atau melebihi saldo.
        """
        if jumlah <= 0:
            raise ValueError("Jumlah penarikan harus lebih dari 0.")
        if jumlah > self.__saldo:
            raise ValueError("Saldo tidak mencukupi.")
        self.__saldo -= jumlah


rek = RekeningBank("Andi", "1234567890", 500_000)

print("--- Akses lewat property dan method ---")
print("Pemilik :", rek.pemilik)
print("Nomor   :", rek.nomor)
print("Saldo   :", rek.saldo)
rek.setor(250_000)
rek.tarik(100_000)
print("Saldo setelah setor 250.000 dan tarik 100.000 :", rek.saldo)

print()
print("--- Percobaan melanggar perlindungan ---")
try:
    print(rek.__saldo)
except AttributeError as galat:
    print("rek.__saldo       ->", galat)

try:
    rek.saldo = 999_999_999
except AttributeError as galat:
    print("rek.saldo = ...   ->", galat)

try:
    rek.tarik(5_000_000)
except ValueError as galat:
    print("tarik 5.000.000   ->", galat)

print()
print("--- Name mangling: private sebenarnya hanya diganti namanya ---")
print("Nama asli atribut private :", "_RekeningBank__saldo")
print("Nilainya                  :", rek._RekeningBank__saldo)
print("(Ini tidak dianjurkan: pengguna class seharusnya memakai method.)")
