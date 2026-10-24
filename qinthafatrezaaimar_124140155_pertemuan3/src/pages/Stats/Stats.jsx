import { useEffect } from 'react'
import { Link } from 'react-router-dom'
import { useBooks } from '../../context/useBooks.js'
import { useBookStats } from '../../hooks/useBookStats.js'
import { STATUS_BUKU, DAFTAR_STATUS } from '../../constants/status.js'
import StatCard from '../../components/StatCard/StatCard.jsx'
import StatusBadge from '../../components/StatusBadge/StatusBadge.jsx'
import './Stats.css'

// Halaman statistik: ringkasan jumlah buku per status dan penulis terbanyak
function Stats() {
  const { books } = useBooks()
  const { total, perStatus, persenSelesaiDimiliki, penulisTeratas } = useBookStats(books)

  useEffect(() => {
    document.title = 'Statistik | Rak Buku Pribadi'
  }, [])

  if (total === 0) {
    return (
      <>
        <h1 className="judul-halaman">Statistik</h1>
        <div className="card stats-kosong">
          <p>Belum ada data untuk dihitung.</p>
          <Link to="/" className="btn btn-utama">
            Tambah buku dulu
          </Link>
        </div>
      </>
    )
  }

  return (
    <>
      <h1 className="judul-halaman">Statistik</h1>
      <p className="subjudul">Ringkasan isi rak bukumu.</p>

      <div className="stats-kartu">
        <StatCard label="Total buku" value={total} />
        {DAFTAR_STATUS.map((status) => (
          <StatCard key={status} label={STATUS_BUKU[status]} value={perStatus[status]} aksen={status} />
        ))}
      </div>

      <div className="stats-grid">
        <section className="card">
          <h2>Komposisi Rak</h2>
          <ul className="stats-bar-daftar">
            {DAFTAR_STATUS.map((status) => {
              const persen = Math.round((perStatus[status] / total) * 100)
              return (
                <li key={status}>
                  <div className="stats-bar-label">
                    <StatusBadge status={status} />
                    <span>
                      {perStatus[status]} buku &middot; {persen}%
                    </span>
                  </div>
                  <div className="stats-bar">
                    <div className={`stats-bar-isi stats-bar-${status}`} style={{ width: `${persen}%` }} />
                  </div>
                </li>
              )
            })}
          </ul>
          <p className="stats-catatan">
            {persenSelesaiDimiliki}% buku di rak sudah kamu miliki (dimiliki atau sedang dibaca).
          </p>
        </section>

        <section className="card">
          <h2>Penulis Terbanyak</h2>
          <ol className="stats-penulis">
            {penulisTeratas.map(({ nama, jumlah }) => (
              <li key={nama}>
                <span>{nama}</span>
                <span className="stats-penulis-jumlah">{jumlah} buku</span>
              </li>
            ))}
          </ol>
        </section>
      </div>
    </>
  )
}

export default Stats
