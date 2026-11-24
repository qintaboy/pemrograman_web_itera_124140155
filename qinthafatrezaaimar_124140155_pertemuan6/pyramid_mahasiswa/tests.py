"""Tes API Mahasiswa dan Matakuliah memakai WebTest + SQLite sementara.

Jalankan dari folder proyek:  pytest
Tes tidak menyentuh database PostgreSQL: tiap tes memakai berkas SQLite
sementara yang dibuat ulang dari model.
"""
import os
import tempfile
import unittest

from webtest import TestApp

from pyramid_mahasiswa import main
from pyramid_mahasiswa.models.meta import Base


class ApiTest(unittest.TestCase):
    """Dasar semua tes: membuat aplikasi dengan database kosong."""

    def setUp(self):
        self.berkas = tempfile.NamedTemporaryFile(suffix='.sqlite',
                                                  delete=False)
        self.berkas.close()
        app = main({}, **{
            'sqlalchemy.url': 'sqlite:///' + self.berkas.name,
            'retry.attempts': '3',
            'pyramid.includes': 'pyramid_tm',
        })
        engine = app.registry['dbsession_factory'].kw['bind']
        Base.metadata.create_all(engine)
        self.engine = engine
        self.app = TestApp(app)

    def tearDown(self):
        self.engine.dispose()
        os.unlink(self.berkas.name)


class TestMatakuliah(ApiTest):
    """Tes endpoint /api/matakuliah."""

    DATA = {'kode_mk': 'IF2110', 'nama_mk': 'Pemrograman Web',
            'sks': 3, 'semester': 3}

    def tambah(self, **ubah):
        data = dict(self.DATA, **ubah)
        return self.app.post_json('/api/matakuliah', data, expect_errors=True)

    def test_daftar_kosong(self):
        res = self.app.get('/api/matakuliah')
        self.assertEqual(res.status_int, 200)
        self.assertEqual(res.json['matakuliah'], [])

    def test_tambah_valid(self):
        res = self.tambah()
        self.assertEqual(res.status_int, 200)
        self.assertTrue(res.json['success'])
        self.assertEqual(res.json['matakuliah']['kode_mk'], 'IF2110')

    def test_tambah_field_wajib_kosong(self):
        for kosong in ('kode_mk', 'nama_mk'):
            self.assertEqual(self.tambah(**{kosong: ''}).status_int, 400)
        self.assertEqual(self.tambah(kode_mk='   ').status_int, 400)

    def test_tambah_field_hilang(self):
        data = {'kode_mk': 'IF1', 'nama_mk': 'X', 'semester': 1}
        res = self.app.post_json('/api/matakuliah', data, expect_errors=True)
        self.assertEqual(res.status_int, 400)

    def test_tambah_sks_semester_tidak_valid(self):
        for nilai in (0, -1, 'tiga', 3.5, True):
            self.assertEqual(self.tambah(sks=nilai).status_int, 400)
            self.assertEqual(self.tambah(semester=nilai).status_int, 400)

    def test_tambah_kode_kembar(self):
        self.assertEqual(self.tambah().status_int, 200)
        self.assertEqual(self.tambah().status_int, 400)

    def test_detail_ada_dan_tidak_ada(self):
        self.tambah()
        self.assertEqual(self.app.get('/api/matakuliah/1').status_int, 200)
        res = self.app.get('/api/matakuliah/99', expect_errors=True)
        self.assertEqual(res.status_int, 404)
        self.assertIn('error', res.json)

    def test_ubah(self):
        self.tambah()
        res = self.app.put_json('/api/matakuliah/1', {'sks': 4})
        self.assertEqual(res.json['matakuliah']['sks'], 4)
        res = self.app.put_json('/api/matakuliah/1', {'sks': 0},
                                expect_errors=True)
        self.assertEqual(res.status_int, 400)
        res = self.app.put_json('/api/matakuliah/99', {'sks': 4},
                                expect_errors=True)
        self.assertEqual(res.status_int, 404)

    def test_hapus(self):
        self.tambah()
        self.assertEqual(self.app.delete('/api/matakuliah/1').status_int, 200)
        res = self.app.delete('/api/matakuliah/1', expect_errors=True)
        self.assertEqual(res.status_int, 404)


class TestMahasiswa(ApiTest):
    """Tes endpoint /api/mahasiswa."""

    DATA = {'nim': '121140155', 'nama': 'Qinthafa', 'jurusan': 'TI',
            'tanggal_lahir': '2004-03-12', 'alamat': 'Lampung'}

    def tambah(self, **ubah):
        data = dict(self.DATA, **ubah)
        return self.app.post_json('/api/mahasiswa', data, expect_errors=True)

    def test_crud_lengkap(self):
        self.assertEqual(self.tambah().status_int, 200)
        self.assertEqual(self.app.get('/api/mahasiswa').status_int, 200)
        res = self.app.put_json('/api/mahasiswa/1', {'alamat': 'Bandar'})
        self.assertEqual(res.json['mahasiswa']['alamat'], 'Bandar')
        self.assertEqual(self.app.delete('/api/mahasiswa/1').status_int, 200)

    def test_tidak_ada_404(self):
        for metode in (self.app.get, self.app.delete):
            res = metode('/api/mahasiswa/99', expect_errors=True)
            self.assertEqual(res.status_int, 404)
        res = self.app.put_json('/api/mahasiswa/99', {'nama': 'X'},
                                expect_errors=True)
        self.assertEqual(res.status_int, 404)

    def test_validasi(self):
        self.assertEqual(self.tambah(nama='').status_int, 400)
        self.assertEqual(self.tambah(tanggal_lahir='12-03-2004').status_int,
                         400)
        self.assertEqual(self.tambah().status_int, 200)
        self.assertEqual(self.tambah().status_int, 400)  # NIM kembar
