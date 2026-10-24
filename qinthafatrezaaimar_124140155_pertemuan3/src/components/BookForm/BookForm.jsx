import { useState } from 'react'
import PropTypes from 'prop-types'
import { STATUS_BUKU, DAFTAR_STATUS } from '../../constants/status.js'
import { validasiBuku } from '../../utils/validasiBuku.js'
import './BookForm.css'

const DATA_KOSONG = { title: '', author: '', status: 'milik' }

/**
 * Form untuk menambah atau mengedit buku (reusable).
 * - Mode tambah: initialData tidak diisi, form dikosongkan setelah berhasil.
 * - Mode edit: initialData berisi data buku, muncul tombol Batal.
 */
function BookForm({ initialData = null, onSubmit, onCancel = null, submitLabel = 'Tambah Buku' }) {
  const [form, setForm] = useState(initialData ?? DATA_KOSONG)
  const [error, setError] = useState({})
  const modeEdit = Boolean(initialData)

  // Satu handler untuk semua input, memakai atribut "name" sebagai kunci
  const handleChange = (event) => {
    const { name, value } = event.target
    setForm((lama) => ({ ...lama, [name]: value }))
    // Pesan error langsung hilang begitu kolom tersebut diperbaiki
    if (error[name]) setError((lama) => ({ ...lama, [name]: undefined }))
  }

  const handleSubmit = (event) => {
    event.preventDefault()
    const hasil = validasiBuku(form)
    setError(hasil)
    if (Object.keys(hasil).length > 0) return

    onSubmit({ title: form.title, author: form.author, status: form.status })
    if (!modeEdit) setForm(DATA_KOSONG)
  }

  return (
    <form className="book-form" onSubmit={handleSubmit} noValidate>
      <div className="book-form-field">
        <label htmlFor="book-title">Judul Buku</label>
        <input
          id="book-title"
          name="title"
          type="text"
          value={form.title}
          onChange={handleChange}
          placeholder="Contoh: Laskar Pelangi"
          className={error.title ? 'input-salah' : ''}
          aria-invalid={Boolean(error.title)}
          aria-describedby="error-title"
        />
        <p className="book-form-error" id="error-title" role={error.title ? 'alert' : undefined}>
          {error.title}
        </p>
      </div>

      <div className="book-form-field">
        <label htmlFor="book-author">Penulis</label>
        <input
          id="book-author"
          name="author"
          type="text"
          value={form.author}
          onChange={handleChange}
          placeholder="Contoh: Andrea Hirata"
          className={error.author ? 'input-salah' : ''}
          aria-invalid={Boolean(error.author)}
          aria-describedby="error-author"
        />
        <p className="book-form-error" id="error-author" role={error.author ? 'alert' : undefined}>
          {error.author}
        </p>
      </div>

      <div className="book-form-field">
        <label htmlFor="book-status">Status</label>
        <select id="book-status" name="status" value={form.status} onChange={handleChange}>
          {DAFTAR_STATUS.map((status) => (
            <option key={status} value={status}>
              {STATUS_BUKU[status]}
            </option>
          ))}
        </select>
        <p className="book-form-error">{error.status}</p>
      </div>

      <div className="book-form-aksi">
        <button type="submit" className="btn btn-utama">
          {submitLabel}
        </button>
        {onCancel && (
          <button type="button" className="btn btn-garis" onClick={onCancel}>
            Batal
          </button>
        )}
      </div>
    </form>
  )
}

BookForm.propTypes = {
  initialData: PropTypes.shape({
    title: PropTypes.string.isRequired,
    author: PropTypes.string.isRequired,
    status: PropTypes.oneOf(DAFTAR_STATUS).isRequired,
  }),
  onSubmit: PropTypes.func.isRequired,
  onCancel: PropTypes.func,
  submitLabel: PropTypes.string,
}

export default BookForm
