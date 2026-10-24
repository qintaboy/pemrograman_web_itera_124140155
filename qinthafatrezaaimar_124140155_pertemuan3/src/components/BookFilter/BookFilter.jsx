import PropTypes from 'prop-types'
import { STATUS_BUKU, DAFTAR_STATUS } from '../../constants/status.js'
import './BookFilter.css'

// Komponen pencarian + filter status. Nilainya dikendalikan oleh halaman induk (controlled component).
function BookFilter({ search, onSearchChange, status, onStatusChange, jumlahPerStatus = null }) {
  const pilihan = ['semua', ...DAFTAR_STATUS]

  return (
    <div className="book-filter">
      <input
        type="search"
        className="book-filter-cari"
        value={search}
        onChange={(event) => onSearchChange(event.target.value)}
        placeholder="Cari judul atau penulis..."
        aria-label="Cari judul atau penulis"
      />

      <div className="book-filter-status" role="group" aria-label="Filter status">
        {pilihan.map((item) => (
          <button
            key={item}
            type="button"
            className={`book-filter-chip ${status === item ? 'aktif' : ''}`}
            aria-pressed={status === item}
            onClick={() => onStatusChange(item)}
          >
            {item === 'semua' ? 'Semua' : STATUS_BUKU[item]}
            {jumlahPerStatus && <span className="book-filter-jumlah">{jumlahPerStatus[item] ?? 0}</span>}
          </button>
        ))}
      </div>
    </div>
  )
}

BookFilter.propTypes = {
  search: PropTypes.string.isRequired,
  onSearchChange: PropTypes.func.isRequired,
  status: PropTypes.oneOf(['semua', ...DAFTAR_STATUS]).isRequired,
  onStatusChange: PropTypes.func.isRequired,
  jumlahPerStatus: PropTypes.objectOf(PropTypes.number),
}

export default BookFilter
