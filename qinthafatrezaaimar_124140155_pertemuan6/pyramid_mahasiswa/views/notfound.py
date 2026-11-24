"""View untuk alamat yang tidak dikenali (404)."""

from pyramid.view import notfound_view_config


@notfound_view_config(renderer='json')
def notfound_view(request):
    """Mengembalikan galat 404 dalam bentuk JSON.

    Mengembalikan:
        dict: {"error": "..."} dengan status HTTP 404.
    """
    request.response.status = 404
    return {'error': 'Alamat tidak ditemukan.'}
