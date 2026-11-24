"""Model ORM untuk tabel mahasiswa."""

from sqlalchemy import (
    Column,
    Date,
    Integer,
    Text,
)

from .meta import Base


class Mahasiswa(Base):
    """Data seorang mahasiswa.

    Kolom:
        id: kunci utama, bertambah otomatis.
        nim: nomor induk mahasiswa (unik, wajib).
        nama: nama lengkap (wajib).
        jurusan: program studi (wajib).
        tanggal_lahir: tanggal lahir (opsional).
        alamat: alamat tinggal (opsional).
    """

    __tablename__ = 'mahasiswa'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nim = Column(Text, unique=True, nullable=False)
    nama = Column(Text, nullable=False)
    jurusan = Column(Text, nullable=False)
    tanggal_lahir = Column(Date, nullable=True)
    alamat = Column(Text, nullable=True)

    def to_dict(self):
        """Mengubah objek menjadi dictionary agar bisa dikirim sebagai JSON.

        Mengembalikan:
            dict: data mahasiswa. Tanggal diubah ke teks format YYYY-MM-DD.
        """
        return {
            'id': self.id,
            'nim': self.nim,
            'nama': self.nama,
            'jurusan': self.jurusan,
            'tanggal_lahir': (
                self.tanggal_lahir.isoformat() if self.tanggal_lahir else None
            ),
            'alamat': self.alamat,
        }
