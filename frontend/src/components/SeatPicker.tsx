import { useState, useEffect } from 'react'
import { fetchSeatsForRoom, createReservation } from '../api'
import type { Seat } from '../api'
import { Check, X } from 'lucide-react'

interface SeatPickerProps {
  roomId: number;
  showtimeId: number;
  onClose: () => void;
}

export function SeatPicker({ roomId, showtimeId, onClose }: SeatPickerProps) {
  const [seats, setSeats] = useState<Seat[]>([])
  const [selectedSeats, setSelectedSeats] = useState<number[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [success, setSuccess] = useState(false)

  useEffect(() => {
    fetchSeatsForRoom(roomId)
      .then(setSeats)
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false))
  }, [roomId])

  const toggleSeat = (seatId: number) => {
    setSelectedSeats(prev => 
      prev.includes(seatId) 
        ? prev.filter(id => id !== seatId)
        : [...prev, seatId]
    )
  }

  const handleReserve = async () => {
    if (selectedSeats.length === 0) return
    setError(null)
    try {
      await createReservation(showtimeId, selectedSeats)
      setSuccess(true)
      setTimeout(onClose, 2000)
    } catch (err: any) {
      if (err.response && err.response.status === 409) {
        setError('Opa! Um ou mais assentos já foram reservados. Tente outro.')
      } else if (err.response && err.response.status === 401) {
        setError('Você precisa fazer login primeiro.')
      } else {
        setError('Erro ao reservar. Tente novamente.')
      }
    }
  }

  if (loading) return <div className="text-white">Carregando mapa de assentos...</div>

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/80 backdrop-blur-sm">
      <div className="relative flex flex-col w-full max-w-3xl p-8 glass-panel max-h-[90vh]">
        <button onClick={onClose} className="absolute top-4 right-4 hover:text-cinema-red">
          <X size={24} />
        </button>
        
        <h2 className="mb-6 text-2xl font-bold text-center text-white">Escolha sua poltrona</h2>
        
        {/* Screen Indicator */}
        <div className="w-3/4 h-2 mx-auto mb-12 rounded-full shadow-[0_10px_20px_rgba(255,255,255,0.2)] bg-gradient-to-r from-transparent via-white/50 to-transparent"></div>
        <p className="mb-8 -mt-8 text-xs text-center text-gray-500 uppercase tracking-widest">Tela</p>

        <div className="flex-1 overflow-y-auto">
          {error && <div className="p-4 mb-6 text-red-100 bg-red-900/50 rounded-xl border border-red-500/50">{error}</div>}
          {success && <div className="p-4 mb-6 text-green-100 bg-green-900/50 rounded-xl border border-green-500/50 flex items-center gap-2"><Check /> Reserva confirmada com sucesso!</div>}

          <div className="flex flex-wrap justify-center gap-4">
            {seats.length === 0 ? (
              <p className="text-gray-400">Nenhum assento configurado para esta sala.</p>
            ) : (
              seats.map(seat => {
                const isSelected = selectedSeats.includes(seat.id)
                return (
                  <button
                    key={seat.id}
                    onClick={() => toggleSeat(seat.id)}
                    className={`w-12 h-12 flex items-center justify-center rounded-t-xl rounded-b-md transition-all font-bold text-sm border-b-4
                      ${isSelected 
                        ? 'bg-cinema-red text-white border-red-900 scale-110 shadow-[0_0_15px_rgba(229,9,20,0.5)]' 
                        : 'bg-white/10 text-white border-white/5 hover:bg-white/20'}`}
                  >
                    {seat.row_letter}{seat.seat_number}
                  </button>
                )
              })
            )}
          </div>
        </div>

        <div className="flex items-center justify-between mt-8 pt-6 border-t border-white/10">
          <div className="text-gray-300">
            <span className="font-bold text-white">{selectedSeats.length}</span> poltronas
          </div>
          <button 
            onClick={handleReserve}
            disabled={selectedSeats.length === 0 || success}
            className="px-8 py-3 font-bold text-white transition-colors rounded-full bg-cinema-red hover:bg-red-700 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            Reservar
          </button>
        </div>
      </div>
    </div>
  )
}
