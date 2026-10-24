import { describe, it, expect } from 'vitest'
import { renderHook, act } from '@testing-library/react'
import { useLocalStorage } from '../hooks/useLocalStorage.js'
import { useBookStats } from '../hooks/useBookStats.js'

describe('useLocalStorage', () => {
  it('memakai nilai awal lalu menyimpan perubahan ke localStorage', () => {
    const { result } = renderHook(() => useLocalStorage('tes-kunci', []))
    expect(result.current[0]).toEqual([])

    act(() => result.current[1](['buku A']))

    expect(result.current[0]).toEqual(['buku A'])
    expect(JSON.parse(localStorage.getItem('tes-kunci'))).toEqual(['buku A'])
  })

  it('membaca data yang sudah ada di localStorage', () => {
    localStorage.setItem('tes-kunci', JSON.stringify(['tersimpan']))
    const { result } = renderHook(() => useLocalStorage('tes-kunci', []))
    expect(result.current[0]).toEqual(['tersimpan'])
  })
})

describe('useBookStats', () => {
  it('menghitung jumlah per status dan penulis terbanyak', () => {
    const books = [
      { id: '1', title: 'Bumi', author: 'Tere Liye', status: 'milik' },
      { id: '2', title: 'Bulan', author: 'Tere Liye', status: 'baca' },
      { id: '3', title: 'Atomic Habits', author: 'James Clear', status: 'beli' },
      { id: '4', title: 'Matahari', author: 'Tere Liye', status: 'beli' },
    ]
    const { result } = renderHook(() => useBookStats(books))

    expect(result.current.total).toBe(4)
    expect(result.current.perStatus).toEqual({ milik: 1, baca: 1, beli: 2 })
    expect(result.current.persenSelesaiDimiliki).toBe(50)
    expect(result.current.penulisTeratas[0]).toEqual({ nama: 'Tere Liye', jumlah: 3 })
  })
})
