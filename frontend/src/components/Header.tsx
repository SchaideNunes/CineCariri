import { Link } from 'react-router-dom'
import { Film } from 'lucide-react'

export function Header() {
  const isLoggedIn = !!localStorage.getItem('token')

  const handleLogout = () => {
    localStorage.removeItem('token')
    window.location.reload()
  }

  return (
    <header className="fixed top-0 left-0 right-0 z-50 flex items-center justify-between px-8 py-4 bg-cinema-black/80 backdrop-blur-md border-b border-white/10">
      <Link to="/" className="flex items-center gap-2 transition-transform hover:scale-105">
        <Film size={32} className="text-cinema-red" />
        <span className="text-2xl font-bold tracking-widest uppercase text-white">CineCariri</span>
      </Link>

      <nav className="flex items-center gap-6">
        <Link to="/" className="text-sm font-semibold text-gray-300 transition-colors hover:text-cinema-red">
          Em Cartaz
        </Link>
        {isLoggedIn ? (
          <button 
            onClick={handleLogout}
            className="px-4 py-2 text-sm font-semibold text-white transition-colors border rounded-full border-white/20 bg-white/10 hover:bg-cinema-red"
          >
            Sair
          </button>
        ) : (
          <Link 
            to="/login"
            className="px-4 py-2 text-sm font-semibold text-white transition-colors border rounded-full border-white/20 bg-white/10 hover:bg-cinema-red"
          >
            Entrar
          </Link>
        )}
      </nav>
    </header>
  )
}
