import { useMemo } from 'react'
import { DAFTAR_STATUS } from '../constants/status.js'

/**
 * Custom hook: menghitung statistik dari daftar buku.
 * useMemo membuat perhitungan hanya diulang saat daftar buku berubah.
 *
 * @param {Array} books - daftar buku
 * @returns {{ total: number, perStatus: Object, persenSelesaiDimiliki: number, penulisTeratas: Array }}
 */
export function useBookStats(books) {
  return useMemo(() => {
    // Jumlah buku untuk setiap status, contoh: { milik: 3, baca: 1, beli: 2 }
    const perStatus = Object.fromEntries(DAFTAR_STATUS.map((status) => [status, 0]))
    books.forEach((book) => {
      perStatus[book.status] = (perStatus[book.status] ?? 0) + 1
    })

    // Persentase buku yang sudah dimiliki (milik + sedang dibaca) dibanding semua buku
    const sudahPunya = perStatus.milik + perStatus.baca
    const persenSelesaiDimiliki = books.length === 0 ? 0 : Math.round((sudahPunya / books.length) * 100)

    // Penulis yang paling banyak bukunya, maksimal 5 orang
    const hitungPenulis = {}
    books.forEach(({ author }) => {
      const nama = author.trim()
      hitungPenulis[nama] = (hitungPenulis[nama] ?? 0) + 1
    })
    const penulisTeratas = Object.entries(hitungPenulis)
      .map(([nama, jumlah]) => ({ nama, jumlah }))
      .sort((a, b) => b.jumlah - a.jumlah || a.nama.localeCompare(b.nama))
      .slice(0, 5)

    return { total: books.length, perStatus, persenSelesaiDimiliki, penulisTeratas }
  }, [books])
}
