import { createContext, useContext } from 'react'

// Context menyimpan data buku agar bisa dipakai di halaman mana pun
// tanpa harus mengoper props dari komponen ke komponen (prop drilling).
export const BookContext = createContext(null)

// Hook pembantu supaya komponen cukup menulis: const { books } = useBooks()
export function useBooks() {
  const context = useContext(BookContext)
  if (context === null) {
    throw new Error('useBooks harus dipakai di dalam <BookProvider>')
  }
  return context
}
