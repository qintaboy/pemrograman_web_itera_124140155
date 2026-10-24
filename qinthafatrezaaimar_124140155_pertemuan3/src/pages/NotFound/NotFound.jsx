import { Link } from 'react-router-dom'

// Halaman untuk alamat (URL) yang tidak terdaftar di router
function NotFound() {
  return (
    <div className="card" style={{ textAlign: 'center', padding: '40px 20px' }}>
      <h1 className="judul-halaman">Halaman tidak ditemukan</h1>
      <p className="subjudul">Alamat yang kamu buka tidak ada di Rak Buku Pribadi.</p>
      <Link to="/" className="btn btn-utama" style={{ textDecoration: 'none' }}>
        Kembali ke Koleksi
      </Link>
    </div>
  )
}

export default NotFound
