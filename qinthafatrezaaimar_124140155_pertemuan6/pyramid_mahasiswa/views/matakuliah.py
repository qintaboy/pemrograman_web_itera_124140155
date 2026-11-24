"""View CRUD untuk resource Matakuliah (REST API)."""

from pyramid.httpexceptions import HTTPBadRequest, HTTPNotFound
from pyramid.view import view_config

from ..models import Matakuliah
from . import baca_body_json, galat_json

FIELD_TEKS = ('kode_mk', 'nama_mk')
FIELD_ANGKA = ('sks', 'semester')
FIELD_WAJIB = FIELD_TEKS + FIELD_ANGKA


def _cari_matakuliah(request):
    """Mencari matakuliah berdasarkan {id} pada alamat.

    Parameter:
        request: objek request Pyramid.

    Mengembalikan:
        Matakuliah atau None: data yang cocok, None jika tidak ada.
    """
    id_mk = int(request.matchdict['id'])
    return request.dbsession.get(Matakuliah, id_mk)


def _ke_bilangan_bulat(nilai):
    """Mengubah nilai menjadi bilangan bulat jika memungkinkan.

    Angka bulat dan teks angka ("3") diterima. Boolean, pecahan, dan teks
    biasa ditolak.

    Parameter:
        nilai: nilai dari body JSON.

    Mengembalikan:
        int atau None: bilangan bulat hasil konversi, None jika tidak valid.
    """
    if isinstance(nilai, bool):
        return None
    if isinstance(nilai, int):
        return nilai
    if isinstance(nilai, str):
        teks = nilai.strip()
        if teks.lstrip('-').isdigit():
            return int(teks)
    return None


def _bersihkan(data, lengkap):
    """Memvalidasi dan merapikan data dari body request.

    Aturan:
        - kode_mk dan nama_mk: teks tidak boleh kosong.
        - sks dan semester: bilangan bulat lebih besar dari 0.

    Parameter:
        data (dict): isi JSON dari request.
        lengkap (bool): True untuk POST (keempat field wajib ada),
            False untuk PUT (boleh sebagian field saja).

    Mengembalikan:
        tuple: (data_bersih, pesan_galat). Jika valid, pesan_galat None.
    """
    bersih = {}

    for field in FIELD_WAJIB:
        if field not in data:
            if lengkap:
                return None, f"Field '{field}' wajib diisi."
            continue

        nilai = data[field]
        if field in FIELD_TEKS:
            if not isinstance(nilai, str) or not nilai.strip():
                return None, (
                    f"Field '{field}' wajib diisi dan tidak boleh kosong."
                )
            bersih[field] = nilai.strip()
        else:
            angka = _ke_bilangan_bulat(nilai)
            if angka is None:
                return None, f"Field '{field}' harus berupa bilangan bulat."
            if angka <= 0:
                return None, f"Field '{field}' harus lebih besar dari 0."
            bersih[field] = angka

    if not lengkap and not bersih:
        return None, 'Tidak ada field yang diubah.'
    return bersih, None


def _kode_sudah_dipakai(request, kode_mk, kecuali_id=None):
    """Memeriksa apakah kode matakuliah sudah dipakai matakuliah lain.

    Parameter:
        request: objek request Pyramid.
        kode_mk (str): kode yang diperiksa.
        kecuali_id (int): id matakuliah yang diabaikan (untuk update).

    Mengembalikan:
        bool: True jika kode sudah dipakai.
    """
    query = request.dbsession.query(Matakuliah).filter(
        Matakuliah.kode_mk == kode_mk)
    if kecuali_id is not None:
        query = query.filter(Matakuliah.id != kecuali_id)
    return query.first() is not None


@view_config(route_name='matakuliah_list', request_method='GET',
             renderer='json')
def matakuliah_list(request):
    """GET /api/matakuliah: daftar seluruh matakuliah."""
    daftar = request.dbsession.query(Matakuliah).order_by(Matakuliah.id).all()
    return {'matakuliah': [mk.to_dict() for mk in daftar]}


@view_config(route_name='matakuliah_detail', request_method='GET',
             renderer='json')
def matakuliah_detail(request):
    """GET /api/matakuliah/{id}: detail satu matakuliah, 404 jika tak ada."""
    mk = _cari_matakuliah(request)
    if mk is None:
        return galat_json(HTTPNotFound, 'Matakuliah tidak ditemukan.')
    return {'matakuliah': mk.to_dict()}


@view_config(route_name='matakuliah_add', request_method='POST',
             renderer='json')
def matakuliah_add(request):
    """POST /api/matakuliah: menambah matakuliah (400 jika tidak valid)."""
    data, galat = baca_body_json(request)
    if galat:
        return galat_json(HTTPBadRequest, galat)

    bersih, galat = _bersihkan(data, lengkap=True)
    if galat:
        return galat_json(HTTPBadRequest, galat)
    if _kode_sudah_dipakai(request, bersih['kode_mk']):
        return galat_json(HTTPBadRequest, 'Kode matakuliah sudah terdaftar.')

    mk = Matakuliah(**bersih)
    request.dbsession.add(mk)
    request.dbsession.flush()  # supaya id langsung terisi
    return {'success': True, 'matakuliah': mk.to_dict()}


@view_config(route_name='matakuliah_update', request_method='PUT',
             renderer='json')
def matakuliah_update(request):
    """PUT /api/matakuliah/{id}: mengubah data (404 jika id tidak ada)."""
    mk = _cari_matakuliah(request)
    if mk is None:
        return galat_json(HTTPNotFound, 'Matakuliah tidak ditemukan.')

    data, galat = baca_body_json(request)
    if galat:
        return galat_json(HTTPBadRequest, galat)

    bersih, galat = _bersihkan(data, lengkap=False)
    if galat:
        return galat_json(HTTPBadRequest, galat)
    if ('kode_mk' in bersih
            and _kode_sudah_dipakai(request, bersih['kode_mk'], mk.id)):
        return galat_json(HTTPBadRequest, 'Kode matakuliah sudah terdaftar.')

    for field, nilai in bersih.items():
        setattr(mk, field, nilai)
    request.dbsession.flush()
    return {'success': True, 'matakuliah': mk.to_dict()}


@view_config(route_name='matakuliah_delete', request_method='DELETE',
             renderer='json')
def matakuliah_delete(request):
    """DELETE /api/matakuliah/{id}: menghapus data (404 jika id tidak ada)."""
    mk = _cari_matakuliah(request)
    if mk is None:
        return galat_json(HTTPNotFound, 'Matakuliah tidak ditemukan.')

    request.dbsession.delete(mk)
    return {
        'success': True,
        'message': f'Matakuliah dengan id {mk.id} berhasil dihapus.',
    }
