import PropTypes from 'prop-types'
import './StatCard.css'

// Kartu angka ringkasan, contoh: "12 / Total buku"
function StatCard({ label, value, aksen }) {
  return (
    <div className={`stat-card ${aksen ? `stat-card-${aksen}` : ''}`}>
      <p className="stat-card-angka">{value}</p>
      <p className="stat-card-label">{label}</p>
    </div>
  )
}

StatCard.propTypes = {
  label: PropTypes.string.isRequired,
  value: PropTypes.oneOfType([PropTypes.number, PropTypes.string]).isRequired,
  aksen: PropTypes.oneOf(['milik', 'baca', 'beli']),
}

export default StatCard
