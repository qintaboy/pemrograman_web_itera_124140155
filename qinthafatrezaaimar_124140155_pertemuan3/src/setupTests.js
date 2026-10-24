// Menambahkan matcher seperti toBeInTheDocument() ke expect milik Vitest
import '@testing-library/jest-dom/vitest'
import { afterEach } from 'vitest'
import { cleanup } from '@testing-library/react'

// Bersihkan DOM dan localStorage setelah setiap test agar test tidak saling memengaruhi
afterEach(() => {
  cleanup()
  localStorage.clear()
})
