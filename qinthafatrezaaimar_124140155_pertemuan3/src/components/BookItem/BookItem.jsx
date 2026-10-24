import PropTypes from 'prop-types'
import StatusBadge from '../StatusBadge/StatusBadge.jsx'
import { bookShape } from '../../constants/propTypes.js'
import './BookItem.css'

// Satu baris buku di daftar, lengkap dengan tombol Edit dan Hapus
function BookItem({ book, onEdit, onDelete, sedangDiedit = false }) {
  const { title, author, status } = book

  return (
    <li className={`book-item book-item-${status} ${sedangDiedit ? 'diedit' : ''}`}>
      <div className="book-item-info">
        <p className="book-item-judul">{title}</p>
        <p className="book-item-penulis">{author}</p>
        <StatusBadge status={status} />
      </div>
      <div className="book-item-aksi">
        <button type="button" className="book-item-btn" onClick={() => onEdit(book)} aria-label={`Edit ${title}`}>
          Edit
        </button>
        <button
          type="button"
          className="book-item-btn hapus"
          onClick={() => onDelete(book)}
          aria-label={`Hapus ${title}`}
        >
          Hapus
        </button>
      </div>
    </li>
  )
}

BookItem.propTypes = {
  book: bookShape.isRequired,
  onEdit: PropTypes.func.isRequired,
  onDelete: PropTypes.func.isRequired,
  sedangDiedit: PropTypes.bool,
}

export default BookItem
