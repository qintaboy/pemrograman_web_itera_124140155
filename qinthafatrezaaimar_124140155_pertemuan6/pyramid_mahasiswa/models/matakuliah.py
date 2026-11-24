"""Model ORM untuk tabel matakuliah."""

from sqlalchemy import (
    Column,
    Integer,
    Text,
)

from .meta import Base


class Matakuliah(Base):
    """Data satu matakuliah.

    Kolom:
        id: kunci utama, bertambah otomatis.
        kode_mk: kode matakuliah, unik dan wajib (contoh: IF2110).
        nama_mk: nama matakuliah, wajib (contoh: Pemrograman Web).
        sks: jumlah SKS, wajib (contoh: 3).
        semester: semester penyelenggaraan, wajib (contoh: 5).
    """

    __tablename__ = 'matakuliah'

    id = Column(Integer, primary_key=True, autoincrement=True)
    kode_mk = Column(Text, unique=True, nullable=False)
    nama_mk = Column(Text, nullable=False)
    sks = Column(Integer, nullable=False)
    semester = Column(Integer, nullable=False)

    def to_dict(self):
        """Mengubah objek menjadi dictionary agar bisa dikirim sebagai JSON.

        Mengembalikan:
            dict: data matakuliah.
        """
        return {
            'id': self.id,
            'kode_mk': self.kode_mk,
            'nama_mk': self.nama_mk,
            'sks': self.sks,
            'semester': self.semester,
        }
