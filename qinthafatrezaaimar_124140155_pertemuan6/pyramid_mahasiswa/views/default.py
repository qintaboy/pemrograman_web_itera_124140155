"""View halaman utama: ringkasan endpoint yang tersedia."""

from pyramid.view import view_config


@view_config(route_name='home', renderer='json')
def home(request):
    """Menampilkan nama API dan daftar endpoint.

    Mengembalikan:
        dict: informasi API dalam bentuk JSON.
    """
    return {
        'project': 'pyramid_mahasiswa',
        'deskripsi': 'REST API CRUD Mahasiswa dan Matakuliah',
        'endpoint': {
            'mahasiswa': '/api/mahasiswa',
            'matakuliah': '/api/matakuliah',
        },
    }
