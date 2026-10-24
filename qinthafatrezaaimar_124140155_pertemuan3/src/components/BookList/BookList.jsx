import PropTypes from 'prop-types'
import BookItem from '../BookItem/BookItem.jsx'
import { bookShape } from '../../constants/propTypes.js'
import './BookList.css'

// Menampilkan daftar buku, atau pesan kosong jika tidak ada buku yang cocok
function BookList({ books, onEdit, onDelete, idDiedit = null, pesanKosong = 'Belum ada buku.' }) {
  if (books.length === 0) {
    return <p className="book-list-kosong">{pesanKosong}</p>
  }

  return (
    <ul className="book-list">
      {books.map((book) => (
        <BookItem
          key={book.id}
          book={book}
          onEdit={onEdit}
          onDelete={onDelete}
          sedangDiedit={book.id === idDiedit}
        />
      ))}
    </ul>
  )
}

BookList.propTypes = {
  books: PropTypes.arrayOf(bookShape).isRequired,
  onEdit: PropTypes.func.isRequired,
  onDelete: PropTypes.func.isRequired,
  idDiedit: PropTypes.string,
  pesanKosong: PropTypes.string,
}

export default BookList
