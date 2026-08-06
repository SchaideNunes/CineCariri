import axios from 'axios';

// The proxy in vite.config.ts routes /api to http://localhost:8000
const api = axios.create({
  baseURL: '/api',
});

// Interceptor to add JWT token if user is logged in
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token && config.headers) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export interface Movie {
  id: number;
  title: string;
  description: string;
  poster_url: string;
  genre: string;
  duration_mins: number;
}

export interface Room {
  id: number;
  name: string;
  capacity: number;
}

export interface Showtime {
  id: number;
  movie_id: number;
  room_id: number;
  start_time: string;
  format: string;
  audio: string;
  available_tickets: number;
}

export const fetchMovies = async (): Promise<Movie[]> => {
  const response = await api.get('/movies/');
  return response.data;
};

export const fetchMovieById = async (id: number): Promise<Movie> => {
  const response = await api.get(`/movies/${id}`);
  return response.data;
};

export const fetchShowtimes = async (): Promise<Showtime[]> => {
  const response = await api.get('/showtimes/');
  return response.data;
};

export const createReservation = async (showtimeId: number, ticketsCount: number) => {
  const response = await api.post('/reservations/', {
    showtime_id: showtimeId,
    tickets_count: ticketsCount,
  });
  return response.data;
};

export const logout = () => {
  localStorage.removeItem('token');
  window.location.reload();
};

export default api;
