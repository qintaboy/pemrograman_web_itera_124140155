import PropTypes from 'prop-types'
import { DAFTAR_STATUS } from './status.js'

// Bentuk data satu buku, dipakai ulang oleh BookItem dan BookList
export const bookShape = PropTypes.shape({
  id: PropTypes.string.isRequired,
  title: PropTypes.string.isRequired,
  author: PropTypes.string.isRequired,
  status: PropTypes.oneOf(DAFTAR_STATUS).isRequired,
  createdAt: PropTypes.string,
})
