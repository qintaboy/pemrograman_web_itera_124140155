import { describe, it, expect, vi } from 'vitest'
import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import BookForm from '../components/BookForm/BookForm.jsx'

describe('BookForm', () => {
  it('menampilkan pesan error dan tidak mengirim data jika form kosong', async () => {
    const onSubmit = vi.fn()
    render(<BookForm onSubmit={onSubmit} />)

    await userEvent.click(screen.getByRole('button', { name: 'Tambah Buku' }))

    expect(screen.getByText('Judul buku wajib diisi.')).toBeInTheDocument()
    expect(screen.getByText('Nama penulis wajib diisi.')).toBeInTheDocument()
    expect(screen.getByLabelText('Judul Buku')).toHaveClass('input-salah')
    expect(onSubmit).not.toHaveBeenCalled()
  })

  it('mengirim data yang valid lalu mengosongkan form', async () => {
    const onSubmit = vi.fn()
    render(<BookForm onSubmit={onSubmit} />)

    await userEvent.type(screen.getByLabelText('Judul Buku'), 'Laskar Pelangi')
    await userEvent.type(screen.getByLabelText('Penulis'), 'Andrea Hirata')
    await userEvent.selectOptions(screen.getByLabelText('Status'), 'baca')
    await userEvent.click(screen.getByRole('button', { name: 'Tambah Buku' }))

    expect(onSubmit).toHaveBeenCalledWith({ title: 'Laskar Pelangi', author: 'Andrea Hirata', status: 'baca' })
    expect(screen.getByLabelText('Judul Buku')).toHaveValue('')
  })

  it('menghapus pesan error begitu kolom diperbaiki', async () => {
    render(<BookForm onSubmit={vi.fn()} />)

    await userEvent.click(screen.getByRole('button', { name: 'Tambah Buku' }))
    expect(screen.getByText('Judul buku wajib diisi.')).toBeInTheDocument()

    await userEvent.type(screen.getByLabelText('Judul Buku'), 'B')
    expect(screen.queryByText('Judul buku wajib diisi.')).not.toBeInTheDocument()
  })

  it('mode edit: mengisi form dengan data lama dan menampilkan tombol Batal', async () => {
    const onCancel = vi.fn()
    render(
      <BookForm
        initialData={{ title: 'Bumi', author: 'Tere Liye', status: 'milik' }}
        onSubmit={vi.fn()}
        onCancel={onCancel}
        submitLabel="Simpan Perubahan"
      />,
    )

    expect(screen.getByLabelText('Judul Buku')).toHaveValue('Bumi')
    await userEvent.click(screen.getByRole('button', { name: 'Batal' }))
    expect(onCancel).toHaveBeenCalledTimes(1)
  })
})
