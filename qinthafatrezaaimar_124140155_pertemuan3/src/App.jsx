import { Routes, Route } from 'react-router-dom'
import Navbar from './components/Navbar/Navbar.jsx'
import Home from './pages/Home/Home.jsx'
import Stats from './pages/Stats/Stats.jsx'
import NotFound from './pages/NotFound/NotFound.jsx'

// Kerangka aplikasi: navbar di atas, isi halaman ditentukan oleh URL
function App() {
  return (
    <>
      <Navbar />
      <main className="container">
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/statistik" element={<Stats />} />
          <Route path="*" element={<NotFound />} />
        </Routes>
      </main>
      <footer className="footer">
        Qinthafa Treza Aimar &middot; 124140155 &middot; Praktikum PAW Kelas RA
      </footer>
    </>
  )
}

export default App
