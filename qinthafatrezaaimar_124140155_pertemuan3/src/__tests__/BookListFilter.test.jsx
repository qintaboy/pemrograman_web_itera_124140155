import { describe, it, expect, vi } from 'vitest'
import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import BookList from '../components/BookList/BookList.jsx'
import BookFilter from '../components/BookFilter/BookFilter.jsx'

const contohBuku = [
  { id: '1', title: 'Laskar Pelangi', author: 'Andrea Hirata', status: 'milik' },
  { id: '2', title: 'Atomic Habits', author: 'James Clear', status: 'beli' },
]

describe('BookList', () => {
  it('menampilkan pesan kosong jika tidak ada buku', () => {
    render(<BookList books={[]} onEdit={vi.fn()} onDelete={vi.fn()} pesanKosong="Rak masih kosong." />)
    expect(screen.getByText('Rak masih kosong.')).toBeInTheDocument()
  })

  it('menampilkan semua buku dan memanggil onDelete dengan buku yang benar', async () => {
    const onDelete = vi.fn()
    render(<BookList books={contohBuku} onEdit={vi.fn()} onDelete={onDelete} />)

    expect(screen.getAllByRole('listitem')).toHaveLength(2)
    expect(screen.getByText('Ingin Dibeli')).toBeInTheDocument()

    await userEvent.click(screen.getByRole('button', { name: 'Hapus Atomic Habits' }))
    expect(onDelete).toHaveBeenCalledWith(contohBuku[1])
  })
})

describe('BookFilter', () => {
  it('memanggil onStatusChange dan onSearchChange saat dipakai', async () => {
    const onStatusChange = vi.fn()
    const onSearchChange = vi.fn()
    render(
      <BookFilter
        search=""
        onSearchChange={onSearchChange}
        status="semua"
        onStatusChange={onStatusChange}
      />,
    )

    await userEvent.click(screen.getByRole('button', { name: 'Sedang Dibaca' }))
    expect(onStatusChange).toHaveBeenCalledWith('baca')

    await userEvent.type(screen.getByLabelText('Cari judul atau penulis'), 'a')
    expect(onSearchChange).toHaveBeenCalledWith('a')
  })
})
