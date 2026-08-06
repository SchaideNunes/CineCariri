import { useEffect, useState } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { ArrowLeft, Clock, MonitorPlay, Volume2, Plus, Minus } from 'lucide-react'
import { fetchMovieById, fetchShowtimes, createReservation } from '../api'
import type { Movie, Showtime } from '../api'

export function MovieDetailsPage() {
  const { id } = useParams<{ id: string }>()
  const navigate = useNavigate()
  
  const [movie, setMovie] = useState<Movie | null>(null)
  const [showtimes, setShowtimes] = useState<Showtime[]>([])
  const [loading, setLoading] = useState(true)
  
  const [selectedShowtime, setSelectedShowtime] = useState<Showtime | null>(null)
  const [ticketsCount, setTicketsCount] = useState(1)
  const [isReserving, setIsReserving] = useState(false)
  const [error, setError] = useState('')

  useEffect(() => {
    if (!id) return;
    
    Promise.all([fetchMovieById(parseInt(id)), fetchShowtimes()])
      .then(([m, s]) => {
        setMovie(m)
        // Filter showtimes for this movie
        setShowtimes(s.filter(st => st.movie_id === m.id))
      })
      .catch(err => {
        console.error(err)
        setError("Erro ao carregar o filme.")
      })
      .finally(() => setLoading(false))
  }, [id])

  const handleReserve = async () => {
    if (!selectedShowtime) return;
    
    setIsReserving(true)
    setError('')
    try {
      await createReservation(selectedShowtime.id, ticketsCount)
      alert("Reserva confirmada com sucesso!")
      navigate('/')
    } catch (err: any) {
      if (err.response?.status === 401) {
         setError("Você precisa estar logado para comprar ingressos.")
      } else {
         setError(err.response?.data?.detail || "Erro ao fazer a reserva.")
      }
    } finally {
      setIsReserving(false)
    }
  }

  if (loading) {
    return <div className="flex items-center justify-center min-h-screen text-white bg-cinema-black">Carregando...</div>
  }

  if (!movie) {
    return (
      <div className="flex flex-col items-center justify-center min-h-screen text-white bg-cinema-black">
        <h2>Filme não encontrado</h2>
        <button onClick={() => navigate('/')} className="mt-4 text-cinema-red hover:underline">Voltar</button>
      </div>
    )
  }

  return (
    <div className="min-h-screen text-white bg-cinema-black">
      {/* Header Backdrop */}
      <div 
        className="relative w-full h-[60vh] bg-cover bg-center"
        style={{ backgroundImage: `url(${movie.poster_url || 'https://images.unsplash.com/photo-1489599849927-2ee91cede3ba?q=80&w=800&auto=format&fit=crop'})` }}
      >
        <div className="absolute inset-0 bg-gradient-to-t from-cinema-black via-cinema-black/60 to-transparent"></div>
        
        <button 
          onClick={() => navigate('/')}
          className="absolute flex items-center gap-2 p-2 px-4 transition-colors rounded-full top-24 left-8 bg-black/50 hover:bg-cinema-red backdrop-blur-md"
        >
          <ArrowLeft size={20} />
          Voltar
        </button>

        <div className="absolute bottom-0 left-0 p-8 max-w-4xl">
          <h1 className="mb-2 text-5xl font-bold md:text-6xl text-white">{movie.title}</h1>
          <div className="flex items-center gap-4 text-lg text-gray-300">
            <span>{movie.genre}</span>
            <span>&bull;</span>
            <span>{movie.duration_mins} min</span>
          </div>
          <p className="mt-4 text-gray-300 text-lg max-w-2xl">
            {movie.description || "Prepare-se para uma experiência inesquecível no CineCariri."}
          </p>
        </div>
      </div>

      <div className="p-8 mx-auto max-w-7xl">
        <h2 className="mb-8 text-3xl font-bold border-l-4 border-cinema-gold pl-4 text-cinema-gold">
          Comprar Ingressos
        </h2>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-12">
          {/* Sessões Disponíveis */}
          <div>
            <h3 className="mb-4 text-xl font-semibold">Escolha a Sessão</h3>
            
            <div className="flex flex-col gap-4">
              {showtimes.length === 0 ? (
                 <p className="text-gray-400">Nenhuma sessão disponível no momento.</p>
              ) : (
                showtimes.map(st => {
                  const isSelected = selectedShowtime?.id === st.id;
                  const time = new Date(st.start_time).toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'})
                  const date = new Date(st.start_time).toLocaleDateString()
                  const isSoldOut = st.available_tickets <= 0;

                  return (
                    <button
                      key={st.id}
                      disabled={isSoldOut}
                      onClick={() => {
                        setSelectedShowtime(st)
                        setTicketsCount(1)
                      }}
                      className={`text-left p-4 rounded-xl border transition-all ${
                        isSoldOut ? 'opacity-50 cursor-not-allowed border-gray-700 bg-gray-900' : 
                        isSelected ? 'border-cinema-gold bg-cinema-gold/10' : 'border-white/10 hover:border-cinema-red/50 bg-white/5'
                      }`}
                    >
                      <div className="flex items-center justify-between">
                        <div className="flex flex-col">
                          <span className="text-2xl font-bold">{time}</span>
                          <span className="text-sm text-gray-400">{date}</span>
                        </div>
                        
                        <div className="flex items-center gap-6">
                          <div className="flex flex-col gap-1 text-sm text-gray-300">
                            <span className="flex items-center gap-1"><MonitorPlay size={14}/> {st.format}</span>
                            <span className="flex items-center gap-1"><Volume2 size={14}/> {st.audio}</span>
                          </div>
                          
                          <div className="flex flex-col items-end">
                            <span className={`text-sm font-semibold ${isSoldOut ? 'text-red-500' : 'text-green-400'}`}>
                              {isSoldOut ? 'Esgotado' : `${st.available_tickets} livres`}
                            </span>
                          </div>
                        </div>
                      </div>
                    </button>
                  )
                })
              )}
            </div>
          </div>

          {/* Seletor de Ingressos */}
          <div>
            <div className={`p-8 rounded-2xl border border-white/10 bg-white/5 ${!selectedShowtime ? 'opacity-50 pointer-events-none' : ''}`}>
              <h3 className="mb-6 text-xl font-semibold">Quantidade de Ingressos</h3>
              
              <div className="flex items-center justify-between mb-8 p-4 bg-black/50 rounded-xl">
                <span className="text-lg text-gray-300">Ingresso Inteira</span>
                
                <div className="flex items-center gap-4">
                  <button 
                    onClick={() => setTicketsCount(prev => Math.max(1, prev - 1))}
                    disabled={ticketsCount <= 1}
                    className="p-2 rounded-full bg-white/10 hover:bg-cinema-red transition-colors disabled:opacity-50"
                  >
                    <Minus size={20} />
                  </button>
                  
                  <span className="text-2xl font-bold w-8 text-center">{ticketsCount}</span>
                  
                  <button 
                    onClick={() => {
                      if (selectedShowtime && ticketsCount < selectedShowtime.available_tickets) {
                        setTicketsCount(prev => prev + 1)
                      }
                    }}
                    disabled={selectedShowtime ? ticketsCount >= selectedShowtime.available_tickets : true}
                    className="p-2 rounded-full bg-white/10 hover:bg-cinema-red transition-colors disabled:opacity-50"
                  >
                    <Plus size={20} />
                  </button>
                </div>
              </div>

              {error && (
                <div className="p-3 mb-6 text-sm text-red-200 bg-red-900/50 rounded-lg border border-red-500/50">
                  {error}
                </div>
              )}

              <button
                onClick={handleReserve}
                disabled={isReserving || !selectedShowtime}
                className="w-full py-4 text-lg font-bold text-white transition-colors rounded-xl bg-cinema-red hover:bg-red-700 disabled:opacity-50 flex items-center justify-center gap-2"
              >
                {isReserving ? 'Processando...' : 'Confirmar Reserva'}
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
