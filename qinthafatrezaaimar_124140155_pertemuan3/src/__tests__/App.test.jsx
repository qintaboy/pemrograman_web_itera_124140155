import { describe, it, expect, vi } from 'vitest'
import { render, screen, within } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { MemoryRouter } from 'react-router-dom'
import { BookProvider } from '../context/BookContext.jsx'
import App from '../App.jsx'

// Merender aplikasi lengkap (router + context) seperti di main.jsx
const renderApp = (alamat = '/') =>
  render(
    <MemoryRouter initialEntries={[alamat]}>
      <BookProvider>
        <App />
      </BookProvider>
    </MemoryRouter>,
  )

const tambahBuku = async (judul, penulis, status = 'milik') => {
  await userEvent.type(screen.getByLabelText('Judul Buku'), judul)
  await userEvent.type(screen.getByLabelText('Penulis'), penulis)
  await userEvent.selectOptions(screen.getByLabelText('Status'), status)
  await userEvent.click(screen.getByRole('button', { name: 'Tambah Buku' }))
}

describe('Aplikasi Rak Buku (integrasi)', () => {
  it('menambah buku, menyimpannya ke localStorage, dan mencarinya', async () => {
    renderApp()
    await tambahBuku('Laskar Pelangi', 'Andrea Hirata', 'milik')
    await tambahBuku('Atomic Habits', 'James Clear', 'beli')

    const daftar = screen.getByRole('list')
    expect(within(daftar).getAllByRole('listitem')).toHaveLength(2)
    expect(JSON.parse(localStorage.getItem('rakBukuPribadi'))).toHaveLength(2)

    // Pencarian berdasarkan nama penulis
    await userEvent.type(screen.getByLabelText('Cari judul atau penulis'), 'clear')
    expect(within(daftar).getAllByRole('listitem')).toHaveLength(1)
    expect(screen.getByText('Atomic Habits')).toBeInTheDocument()
  })

  it('mengedit dan menghapus buku', async () => {
    vi.spyOn(window, 'confirm').mockReturnValue(true)
    vi.spyOn(window, 'scrollTo').mockImplementation(() => {})
    renderApp()
    await tambahBuku('Bumi', 'Tere Liye')

    await userEvent.click(screen.getByRole('button', { name: 'Edit Bumi' }))
    const inputJudul = screen.getByLabelText('Judul Buku')
    await userEvent.clear(inputJudul)
    await userEvent.type(inputJudul, 'Bumi (Edisi Baru)')
    await userEvent.click(screen.getByRole('button', { name: 'Simpan Perubahan' }))
    expect(screen.getByText('Bumi (Edisi Baru)')).toBeInTheDocument()

    await userEvent.click(screen.getByRole('button', { name: 'Hapus Bumi (Edisi Baru)' }))
    expect(screen.getByText(/Rak masih kosong/)).toBeInTheDocument()
  })

  it('berpindah ke halaman Statistik lewat navbar', async () => {
    renderApp()
    await tambahBuku('Bumi', 'Tere Liye', 'baca')

    await userEvent.click(screen.getByRole('link', { name: 'Statistik' }))
    expect(screen.getByRole('heading', { name: 'Statistik' })).toBeInTheDocument()
    expect(screen.getByText('Penulis Terbanyak')).toBeInTheDocument()
  })
})
