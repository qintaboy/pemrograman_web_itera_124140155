import PropTypes from 'prop-types'
import { STATUS_BUKU, DAFTAR_STATUS } from '../../constants/status.js'
import './StatusBadge.css'

// Label kecil berwarna untuk status buku. Dipakai di daftar buku dan halaman statistik.
function StatusBadge({ status }) {
  return <span className={`status-badge status-${status}`}>{STATUS_BUKU[status]}</span>
}

StatusBadge.propTypes = {
  status: PropTypes.oneOf(DAFTAR_STATUS).isRequired,
}

export default StatusBadge
