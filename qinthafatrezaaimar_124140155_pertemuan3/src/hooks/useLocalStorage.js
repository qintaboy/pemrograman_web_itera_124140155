import { useState, useEffect } from 'react'

/**
 * Custom hook: seperti useState, tetapi nilainya otomatis disimpan ke localStorage.
 *
 * @param {string} key - nama kunci di localStorage
 * @param {*} nilaiAwal - nilai yang dipakai jika localStorage masih kosong
 * @returns {[*, Function]} pasangan [nilai, fungsi pengubah], sama seperti useState
 */
export function useLocalStorage(key, nilaiAwal) {
  // Lazy initialization: localStorage hanya dibaca sekali saat komponen pertama kali dibuat
  const [nilai, setNilai] = useState(() => {
    try {
      const tersimpan = localStorage.getItem(key)
      return tersimpan !== null ? JSON.parse(tersimpan) : nilaiAwal
    } catch (error) {
      // Data rusak atau localStorage tidak bisa diakses: pakai nilai awal
      console.error(`Gagal membaca localStorage "${key}":`, error)
      return nilaiAwal
    }
  })

  // Setiap kali nilai berubah, simpan versi terbarunya ke localStorage
  useEffect(() => {
    try {
      localStorage.setItem(key, JSON.stringify(nilai))
    } catch (error) {
      console.error(`Gagal menyimpan localStorage "${key}":`, error)
    }
  }, [key, nilai])

  return [nilai, setNilai]
}
