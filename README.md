# Cinema Cariri - Movie Reservation System

![CineCariri Logo](frontend/public/Assets/CineCaririLogo.png)

This project is a complete **Movie Reservation System** built as a solution for the [roadmap.sh Movie Reservation System Project](https://roadmap.sh/projects/movie-reservation-system). It provides a full-stack experience for both cinema administrators and regular users to browse movies, check showtimes, and book tickets.

## 🎯 Goal
The goal of this project is to implement complex business logic (e.g., seat reservation and scheduling), design a robust data model with relationships, and handle high-concurrency ticket booking while providing a visually stunning frontend.

---

## ✨ Features

### User Authentication and Authorization
- **Sign up and Login**: Users can create accounts and securely log in.
- **Role-based Access Control**: 
  - **Regular Users**: Can browse movies, view showtimes, and reserve tickets.
  - **Admins**: Can manage the entire catalog of movies, showtimes, and view reporting metrics.

### Movie Management
- **CRUD Operations**: Admins can add, update, and delete movies.
- **Movie Details**: Each movie contains a title, description, poster image, duration, and genre.
- **Showtimes**: Movies are linked to specific showtimes in designated rooms, with distinct formats (2D, 3D) and audio options (Dubbed, Subtitled).

### Reservation Management
- **Showtime Browsing**: Users can see available movies and their respective showtimes for specific dates.
- **Seat Booking**: Users can reserve tickets for a showtime and see available capacity.
- **Concurrency Control**: The system is designed to prevent double-booking using robust database constraints and temporary locks.
- **Reporting**: Admins can view all reservations, track room capacity, and monitor revenue.

---

## 🛠️ Technology Stack

### Backend
- **Python 3.11**
- **FastAPI**: Modern, fast web framework for building APIs.
- **PostgreSQL**: Robust relational database for data integrity.
- **SQLAlchemy (Async)**: ORM for asynchronous database interactions.
- **Pydantic**: Data validation and serialization.
- **JWT**: Secure JSON Web Token authentication.
- **Docker Compose**: Containerization for easy setup and deployment.

### Frontend
- **React 18**: Component-based UI library.
- **Vite**: Next-generation frontend tooling.
- **Tailwind CSS**: Utility-first CSS framework for rapid and responsive design.
- **React Router**: For client-side routing.
- **GSAP**: Powerful animation library for smooth transitions and micro-interactions.
- **Axios**: HTTP client for API requests.

---

## 🚀 How to Run the Project Locally

### Prerequisites
- [Docker](https://www.docker.com/) and Docker Compose
- Node.js (v18+)

### 1. Start the Backend & Database
The backend and PostgreSQL database are fully containerized. To start them:

```bash
# Clone the repository
git clone https://github.com/SchaideNunes/CineCariri.git
cd CineCariri

# Start the services in detached mode
docker-compose up -d

# Seed the database with initial movies, rooms, and showtimes
docker-compose exec backend python seed_db.py
```
The backend API will be available at `http://localhost:8000`. You can view the interactive Swagger documentation at `http://localhost:8000/docs`.

### 2. Start the Frontend
The frontend requires Node.js to run locally:

```bash
# Navigate to the frontend directory
cd frontend

# Install dependencies
npm install

# Start the development server
npm run dev
```
The frontend will be available at `http://localhost:5173`.

---

## 🏗️ Architecture & Considerations

- **Data Integrity**: Relationships between `User`, `Movie`, `Room`, `Showtime`, and `Reservation` are strictly enforced at the database level to prevent orphaned records.
- **Concurrency**: Seat capacities are checked atomically during reservations to prevent overbooking during high-traffic premieres.
- **Scalability**: The application is structured so that background tasks (like sending ticket emails) and caching layers (like Redis for temporary locks) can be easily integrated in future iterations.

## 📄 License
This project is open-source and available under the MIT License.
