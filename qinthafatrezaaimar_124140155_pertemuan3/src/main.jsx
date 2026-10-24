import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import { BrowserRouter } from 'react-router-dom'
import { BookProvider } from './context/BookContext.jsx'
import App from './App.jsx'
import './index.css'

// BrowserRouter mengaktifkan navigasi antarhalaman,
// BookProvider membagikan data buku ke seluruh komponen
createRoot(document.getElementById('root')).render(
  <StrictMode>
    <BrowserRouter>
      <BookProvider>
        <App />
      </BookProvider>
    </BrowserRouter>
  </StrictMode>,
)
