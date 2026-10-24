import PropTypes from 'prop-types'
import { useLocalStorage } from '../hooks/useLocalStorage.js'
import { BookContext } from './useBooks.js'

const KUNCI_STORAGE = 'rakBukuPribadi'

// Id unik sederhana: waktu sekarang + angka acak
const buatId = () => `${Date.now().toString(36)}-${Math.random().toString(36).slice(2, 7)}`

// Provider membungkus aplikasi dan membagikan data buku + fungsi CRUD lewat Context
export function BookProvider({ children }) {
  // Data buku langsung tersimpan ke localStorage lewat custom hook
  const [books, setBooks] = useLocalStorage(KUNCI_STORAGE, [])

  const addBook = ({ title, author, status }) => {
    const bukuBaru = {
      id: buatId(),
      title: title.trim(),
      author: author.trim(),
      status,
      createdAt: new Date().toISOString(),
    }
    // Array baru dibuat dengan spread (immutable), buku terbaru di paling atas
    setBooks((lama) => [bukuBaru, ...lama])
  }

  const updateBook = (id, perubahan) => {
    setBooks((lama) =>
      lama.map((book) =>
        book.id === id
          ? { ...book, ...perubahan, title: perubahan.title.trim(), author: perubahan.author.trim() }
          : book,
      ),
    )
  }

  const deleteBook = (id) => {
    setBooks((lama) => lama.filter((book) => book.id !== id))
  }

  const nilai = { books, addBook, updateBook, deleteBook }

  return <BookContext.Provider value={nilai}>{children}</BookContext.Provider>
}

BookProvider.propTypes = {
  children: PropTypes.node.isRequired,
}
