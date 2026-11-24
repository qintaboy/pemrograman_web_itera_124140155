"""Mengisi database dengan data awal (seeding)."""

import argparse
import sys
from datetime import date

from pyramid.paster import bootstrap, setup_logging
from sqlalchemy.exc import OperationalError

from .. import models

DATA_MAHASISWA = [
    {
        'nim': '121140001',
        'nama': 'Ahmad Fadhil',
        'jurusan': 'Teknik Informatika',
        'tanggal_lahir': date(2003, 5, 14),
        'alamat': 'Bandar Lampung',
    },
    {
        'nim': '121140002',
        'nama': 'Siti Rahma',
        'jurusan': 'Sistem Informasi',
        'tanggal_lahir': date(2003, 8, 21),
        'alamat': 'Metro',
    },
]

DATA_MATAKULIAH = [
    {
        'kode_mk': 'IF2110',
        'nama_mk': 'Pemrograman Web',
        'sks': 3,
        'semester': 3,
    },
    {
        'kode_mk': 'IF3140',
        'nama_mk': 'Basis Data',
        'sks': 4,
        'semester': 5,
    },
    {
        'kode_mk': 'IF2210',
        'nama_mk': 'Struktur Data',
        'sks': 3,
        'semester': 3,
    },
]


def setup_models(dbsession):
    """Menambahkan data awal bila belum ada.

    Pengecekan per NIM membuat skrip ini aman dijalankan berulang kali
    tanpa menghasilkan data ganda.

    Parameter:
        dbsession: session SQLAlchemy yang sedang aktif.
    """
    for data in DATA_MAHASISWA:
        sudah_ada = dbsession.query(models.Mahasiswa).filter(
            models.Mahasiswa.nim == data['nim']).first()
        if sudah_ada is None:
            dbsession.add(models.Mahasiswa(**data))

    for data in DATA_MATAKULIAH:
        sudah_ada = dbsession.query(models.Matakuliah).filter(
            models.Matakuliah.kode_mk == data['kode_mk']).first()
        if sudah_ada is None:
            dbsession.add(models.Matakuliah(**data))


def parse_args(argv):
    """Membaca argumen baris perintah.

    Parameter:
        argv (list): daftar argumen, argv[1] adalah berkas konfigurasi.

    Mengembalikan:
        Namespace: hasil parsing dengan atribut config_uri.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'config_uri',
        help='Configuration file, e.g., development.ini',
    )
    return parser.parse_args(argv[1:])


def main(argv=sys.argv):
    """Titik masuk skrip: membuka koneksi lalu mengisi data awal."""
    args = parse_args(argv)
    setup_logging(args.config_uri)
    env = bootstrap(args.config_uri)

    try:
        with env['request'].tm:
            dbsession = env['request'].dbsession
            setup_models(dbsession)
        print('Seeding selesai.')
    except OperationalError:
        print('''
Pyramid is having a problem using your SQL database.  The problem
might be caused by one of the following things:

1.  You may need to initialize your database tables with `alembic`.
    Run: alembic -c development.ini upgrade head

2.  Your database server may not be running.  Check that the
    database server referred to by the "sqlalchemy.url" setting in
    your "development.ini" file is running.
            ''')


if __name__ == "__main__":
    main()
