def includeme(config):
    """Mendaftarkan seluruh route aplikasi.

    request_method dipakai agar path yang sama bisa dibedakan menurut
    metode HTTP-nya (GET, POST, PUT, DELETE). Nama route di sini harus sama
    persis dengan route_name pada @view_config.
    """
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')

    # --- Mahasiswa ---
    config.add_route('mahasiswa_list', '/api/mahasiswa',
                     request_method='GET')
    config.add_route('mahasiswa_add', '/api/mahasiswa',
                     request_method='POST')
    config.add_route('mahasiswa_detail', '/api/mahasiswa/{id:\\d+}',
                     request_method='GET')
    config.add_route('mahasiswa_update', '/api/mahasiswa/{id:\\d+}',
                     request_method='PUT')
    config.add_route('mahasiswa_delete', '/api/mahasiswa/{id:\\d+}',
                     request_method='DELETE')

    # --- Matakuliah ---
    config.add_route('matakuliah_list', '/api/matakuliah',
                     request_method='GET')
    config.add_route('matakuliah_add', '/api/matakuliah',
                     request_method='POST')
    config.add_route('matakuliah_detail', '/api/matakuliah/{id:\\d+}',
                     request_method='GET')
    config.add_route('matakuliah_update', '/api/matakuliah/{id:\\d+}',
                     request_method='PUT')
    config.add_route('matakuliah_delete', '/api/matakuliah/{id:\\d+}',
                     request_method='DELETE')
