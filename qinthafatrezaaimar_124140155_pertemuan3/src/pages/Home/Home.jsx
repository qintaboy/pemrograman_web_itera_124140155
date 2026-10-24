import { useState, useEffect, useMemo } from 'react'
import { useBooks } from '../../context/useBooks.js'
import { useBookStats } from '../../hooks/useBookStats.js'
import BookForm from '../../components/BookForm/BookForm.jsx'
import BookFilter from '../../components/BookFilter/BookFilter.jsx'
import BookList from '../../components/BookList/BookList.jsx'
import './Home.css'

// Halaman utama: form tambah/edit di kiri, pencarian + filter + daftar buku di kanan
function Home() {
  const { books, addBook, updateBook, deleteBook } = useBooks()
  const { perStatus } = useBookStats(books)

  const [search, setSearch] = useState('')
  const [statusFilter, setStatusFilter] = useState('semua')
  const [bukuDiedit, setBukuDiedit] = useState(null)

  // useEffect: judul tab browser ikut menampilkan jumlah buku
  useEffect(() => {
    document.title = `Koleksi (${books.length}) | Rak Buku Pribadi`
  }, [books.length])

  // Daftar buku setelah difilter status dan dicari berdasarkan judul/penulis
  const bukuTampil = useMemo(() => {
    const kataKunci = search.trim().toLowerCase()
    return books.filter((book) => {
      const cocokStatus = statusFilter === 'semua' || book.status === statusFilter
      const cocokCari =
        kataKunci === '' ||
        book.title.toLowerCase().includes(kataKunci) ||
        book.author.toLowerCase().includes(kataKunci)
      return cocokStatus && cocokCari
    })
  }, [books, search, statusFilter])

  const handleSimpan = (data) => {
    if (bukuDiedit) {
      updateBook(bukuDiedit.id, data)
      setBukuDiedit(null)
    } else {
      addBook(data)
    }
  }

  const handleHapus = (book) => {
    if (!window.confirm(`Hapus buku "${book.title}"?`)) return
    if (bukuDiedit?.id === book.id) setBukuDiedit(null)
    deleteBook(book.id)
  }

  const handleEdit = (book) => {
    setBukuDiedit(book)
    window.scrollTo({ top: 0, behavior: 'smooth' })
  }

  // Pesan kosong dibedakan: belum ada buku sama sekali vs. tidak ada yang cocok
  const pesanKosong =
    books.length === 0
      ? 'Rak masih kosong. Tambahkan buku pertamamu lewat form.'
      : 'Tidak ada buku yang cocok dengan pencarian atau filter.'

  return (
    <>
      <h1 className="judul-halaman">Koleksi Buku</h1>
      <p className="subjudul">Catat buku yang kamu miliki, sedang dibaca, atau ingin dibeli.</p>

      <div className="home-grid">
        <section className="card home-form">
          <h2>{bukuDiedit ? 'Edit Buku' : 'Tambah Buku'}</h2>
          {/* key berubah saat buku yang diedit berganti, sehingga isi form ikut direset */}
          <BookForm
            key={bukuDiedit?.id ?? 'baru'}
            initialData={bukuDiedit}
            onSubmit={handleSimpan}
            onCancel={bukuDiedit ? () => setBukuDiedit(null) : null}
            submitLabel={bukuDiedit ? 'Simpan Perubahan' : 'Tambah Buku'}
          />
        </section>

        <section className="card">
          <BookFilter
            search={search}
            onSearchChange={setSearch}
            status={statusFilter}
            onStatusChange={setStatusFilter}
            jumlahPerStatus={{ semua: books.length, ...perStatus }}
          />
          <BookList
            books={bukuTampil}
            onEdit={handleEdit}
            onDelete={handleHapus}
            idDiedit={bukuDiedit?.id ?? null}
            pesanKosong={pesanKosong}
          />
        </section>
      </div>
    </>
  )
}

export default Home
