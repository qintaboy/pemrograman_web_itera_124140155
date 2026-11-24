"""Paket views, berisi juga fungsi bantu yang dipakai oleh semua view API."""


def galat_json(kelas_http, pesan):
    """Membuat respons galat HTTP dengan isi JSON.

    Parameter:
        kelas_http: kelas galat Pyramid, misalnya HTTPBadRequest (400)
            atau HTTPNotFound (404).
        pesan (str): penjelasan galat untuk pemanggil API.

    Mengembalikan:
        Response: respons galat berisi {"error": pesan}.
    """
    return kelas_http(
        json_body={'error': pesan},
        content_type='application/json',
    )


def baca_body_json(request):
    """Membaca isi request sebagai JSON berbentuk objek.

    Parameter:
        request: objek request Pyramid.

    Mengembalikan:
        tuple: (data, pesan_galat). Jika berhasil, pesan_galat bernilai None.
            Jika gagal (bukan JSON atau bukan objek), data bernilai None.
    """
    try:
        data = request.json_body
    except ValueError:
        return None, 'Isi request harus berupa JSON yang valid.'
    if not isinstance(data, dict):
        return None, 'Isi request harus berupa objek JSON.'
    return data, None
