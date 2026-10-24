import { NavLink } from 'react-router-dom'
import { useBooks } from '../../context/useBooks.js'
import './Navbar.css'

// Navigasi utama. NavLink otomatis memberi class "active" pada halaman yang sedang dibuka.
function Navbar() {
  const { books } = useBooks()

  return (
    <header className="navbar">
      <div className="navbar-isi">
        <NavLink to="/" className="navbar-logo">
          Rak Buku Pribadi
        </NavLink>
        <nav className="navbar-menu" aria-label="Navigasi utama">
          <NavLink to="/" end className="navbar-link">
            Koleksi <span className="navbar-jumlah">{books.length}</span>
          </NavLink>
          <NavLink to="/statistik" className="navbar-link">
            Statistik
          </NavLink>
        </nav>
      </div>
    </header>
  )
}

export default Navbar
