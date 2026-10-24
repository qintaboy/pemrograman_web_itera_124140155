// Daftar status buku. Kunci (milik/baca/beli) disimpan di data,
// label dipakai untuk ditampilkan ke pengguna.
export const STATUS_BUKU = {
  milik: 'Dimiliki',
  baca: 'Sedang Dibaca',
  beli: 'Ingin Dibeli',
}

export const DAFTAR_STATUS = Object.keys(STATUS_BUKU)
