"""View CRUD untuk resource Mahasiswa (REST API)."""

from datetime import date

from pyramid.httpexceptions import HTTPBadRequest, HTTPNotFound
from pyramid.view import view_config

from ..models import Mahasiswa
from . import baca_body_json, galat_json

FIELD_WAJIB = ('nim', 'nama', 'jurusan')
FIELD_TEKS_OPSIONAL = ('alamat',)


def _cari_mahasiswa(request):
    """Mencari mahasiswa berdasarkan {id} pada alamat.

    Parameter:
        request: objek request Pyramid.

    Mengembalikan:
        Mahasiswa atau None: data yang cocok, None jika tidak ada.
    """
    id_mahasiswa = int(request.matchdict['id'])
    return request.dbsession.get(Mahasiswa, id_mahasiswa)


def _bersihkan(data, lengkap):
    """Memvalidasi dan merapikan data dari body request.

    Parameter:
        data (dict): isi JSON dari request.
        lengkap (bool): True untuk POST (field wajib harus ada),
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
        if not isinstance(nilai, str) or not nilai.strip():
            return None, f"Field '{field}' wajib diisi dan tidak boleh kosong."
        bersih[field] = nilai.strip()

    for field in FIELD_TEKS_OPSIONAL:
        if field in data:
            nilai = data[field]
            if nilai is not None and not isinstance(nilai, str):
                return None, f"Field '{field}' harus berupa teks."
            bersih[field] = nilai.strip() if nilai else None

    if 'tanggal_lahir' in data:
        nilai = data['tanggal_lahir']
        if nilai in (None, ''):
            bersih['tanggal_lahir'] = None
        else:
            try:
                bersih['tanggal_lahir'] = date.fromisoformat(str(nilai))
            except ValueError:
                return None, (
                    "Field 'tanggal_lahir' harus berformat YYYY-MM-DD."
                )

    if not lengkap and not bersih:
        return None, 'Tidak ada field yang diubah.'
    return bersih, None


def _nim_sudah_dipakai(request, nim, kecuali_id=None):
    """Memeriksa apakah NIM sudah dimiliki mahasiswa lain.

    Parameter:
        request: objek request Pyramid.
        nim (str): NIM yang diperiksa.
        kecuali_id (int): id mahasiswa yang diabaikan (untuk update).

    Mengembalikan:
        bool: True jika NIM sudah dipakai.
    """
    query = request.dbsession.query(Mahasiswa).filter(Mahasiswa.nim == nim)
    if kecuali_id is not None:
        query = query.filter(Mahasiswa.id != kecuali_id)
    return query.first() is not None


@view_config(route_name='mahasiswa_list', request_method='GET',
             renderer='json')
def mahasiswa_list(request):
    """GET /api/mahasiswa: daftar seluruh mahasiswa."""
    daftar = request.dbsession.query(Mahasiswa).order_by(Mahasiswa.id).all()
    return {'mahasiswa': [mhs.to_dict() for mhs in daftar]}


@view_config(route_name='mahasiswa_detail', request_method='GET',
             renderer='json')
def mahasiswa_detail(request):
    """GET /api/mahasiswa/{id}: detail satu mahasiswa (404 jika tidak ada)."""
    mhs = _cari_mahasiswa(request)
    if mhs is None:
        return galat_json(HTTPNotFound, 'Mahasiswa tidak ditemukan.')
    return {'mahasiswa': mhs.to_dict()}


@view_config(route_name='mahasiswa_add', request_method='POST',
             renderer='json')
def mahasiswa_add(request):
    """POST /api/mahasiswa: menambah mahasiswa baru (400 jika tidak valid)."""
    data, galat = baca_body_json(request)
    if galat:
        return galat_json(HTTPBadRequest, galat)

    bersih, galat = _bersihkan(data, lengkap=True)
    if galat:
        return galat_json(HTTPBadRequest, galat)
    if _nim_sudah_dipakai(request, bersih['nim']):
        return galat_json(HTTPBadRequest, 'NIM sudah terdaftar.')

    mhs = Mahasiswa(**bersih)
    request.dbsession.add(mhs)
    request.dbsession.flush()  # supaya id langsung terisi
    return {'success': True, 'mahasiswa': mhs.to_dict()}


@view_config(route_name='mahasiswa_update', request_method='PUT',
             renderer='json')
def mahasiswa_update(request):
    """PUT /api/mahasiswa/{id}: mengubah data (404 jika id tidak ada)."""
    mhs = _cari_mahasiswa(request)
    if mhs is None:
        return galat_json(HTTPNotFound, 'Mahasiswa tidak ditemukan.')

    data, galat = baca_body_json(request)
    if galat:
        return galat_json(HTTPBadRequest, galat)

    bersih, galat = _bersihkan(data, lengkap=False)
    if galat:
        return galat_json(HTTPBadRequest, galat)
    if 'nim' in bersih and _nim_sudah_dipakai(request, bersih['nim'], mhs.id):
        return galat_json(HTTPBadRequest, 'NIM sudah terdaftar.')

    for field, nilai in bersih.items():
        setattr(mhs, field, nilai)
    request.dbsession.flush()
    return {'success': True, 'mahasiswa': mhs.to_dict()}


@view_config(route_name='mahasiswa_delete', request_method='DELETE',
             renderer='json')
def mahasiswa_delete(request):
    """DELETE /api/mahasiswa/{id}: menghapus data (404 jika id tidak ada)."""
    mhs = _cari_mahasiswa(request)
    if mhs is None:
        return galat_json(HTTPNotFound, 'Mahasiswa tidak ditemukan.')

    request.dbsession.delete(mhs)
    return {
        'success': True,
        'message': f'Mahasiswa dengan id {mhs.id} berhasil dihapus.',
    }
