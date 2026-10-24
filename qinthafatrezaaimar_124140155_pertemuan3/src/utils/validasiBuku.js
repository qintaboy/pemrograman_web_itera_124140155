import { DAFTAR_STATUS } from '../constants/status.js'

// Memeriksa isi form. Mengembalikan objek berisi pesan error untuk kolom yang salah.
export function validasiBuku({ title, author, status }) {
  const error = {}
  if (title.trim() === '') error.title = 'Judul buku wajib diisi.'
  else if (title.trim().length < 2) error.title = 'Judul buku minimal 2 karakter.'

  if (author.trim() === '') error.author = 'Nama penulis wajib diisi.'

  if (!DAFTAR_STATUS.includes(status)) error.status = 'Pilih status buku.'
  return error
}
