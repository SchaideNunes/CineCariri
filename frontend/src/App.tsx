import { useEffect, useState, useRef } from 'react'
import { Canvas, useFrame } from '@react-three/fiber'
import { OrbitControls, Environment, Float } from '@react-three/drei'
import Lenis from 'lenis'
import { gsap as gs } from 'gsap'
import { Film, Ticket, Popcorn } from 'lucide-react'

// --- THREE.JS COMPONENT ---
function CinematicShape() {
  const meshRef = useRef<any>(null)
  
  useFrame((_state, delta) => {
    if (meshRef.current) {
      meshRef.current.rotation.x += delta * 0.2
      meshRef.current.rotation.y += delta * 0.3
    }
  })

  return (
    <Float speed={2} rotationIntensity={1} floatIntensity={2}>
      <mesh ref={meshRef} castShadow receiveShadow>
        <octahedronGeometry args={[2, 1]} />
        <meshPhysicalMaterial 
          color="#D4AF37" 
          metalness={0.8} 
          roughness={0.2} 
          envMapIntensity={1}
          clearcoat={1}
          clearcoatRoughness={0.1}
        />
      </mesh>
    </Float>
  )
}

// --- PRELOADER COMPONENT ---
function Preloader({ onComplete }: { onComplete: () => void }) {
  const containerRef = useRef<HTMLDivElement>(null)
  const textRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    const tl = gs.timeline({
      onComplete: onComplete
    })

    tl.fromTo(textRef.current, 
      { opacity: 0, scale: 0.8 }, 
      { opacity: 1, scale: 1, duration: 1, ease: 'power2.out' }
    )
    .to(textRef.current, { opacity: 0, duration: 0.5, delay: 1 })
    .to(containerRef.current, { yPercent: -100, duration: 0.8, ease: 'power3.inOut' })

    return () => {
      tl.kill()
    }
  }, [onComplete])

  return (
    <div ref={containerRef} className="fixed inset-0 z-50 flex items-center justify-center bg-cinema-black text-white">
      <div ref={textRef} className="flex flex-col items-center gap-4">
        <Film size={64} className="text-cinema-red animate-pulse" />
        <h1 className="text-4xl font-bold tracking-widest uppercase">CineCariri</h1>
      </div>
    </div>
  )
}

// --- MAIN APP ---
function App() {
  const [loading, setLoading] = useState(true)

  // Initialize Lenis Smooth Scroll
  useEffect(() => {
    const lenis = new Lenis({
      duration: 1.2,
      easing: (t) => Math.min(1, 1.001 - Math.pow(2, -10 * t)),
      orientation: 'vertical',
      gestureOrientation: 'vertical',
      smoothWheel: true,
      wheelMultiplier: 1,
      touchMultiplier: 2,
    })

    function raf(time: number) {
      lenis.raf(time)
      requestAnimationFrame(raf)
    }

    requestAnimationFrame(raf)

    return () => lenis.destroy()
  }, [])

  return (
    <>
      {loading && <Preloader onComplete={() => setLoading(false)} />}
      
      {/* Hero Section with 3D Background */}
      <section className="relative w-full h-screen overflow-hidden">
        <div className="absolute inset-0 z-0 pointer-events-auto">
          <Canvas camera={{ position: [0, 0, 8], fov: 45 }}>
            <ambientLight intensity={0.5} />
            <directionalLight position={[10, 10, 10]} intensity={1} castShadow />
            <Environment preset="city" />
            <CinematicShape />
            <OrbitControls enableZoom={false} autoRotate autoRotateSpeed={0.5} />
          </Canvas>
        </div>

        {/* Hero Content (Overlay) */}
        <div className="relative z-10 flex flex-col items-center justify-center w-full h-full p-8 text-center bg-gradient-to-b from-transparent to-cinema-black/90 pointer-events-none">
          <h1 className="mb-4 text-6xl font-bold text-transparent md:text-8xl bg-clip-text bg-gradient-to-r from-cinema-red to-cinema-gold">
            A Magia do Cinema
          </h1>
          <p className="max-w-2xl mb-8 text-xl text-gray-300 md:text-2xl">
            Sua experiência premium começa aqui. Reserve sua poltrona com antecedência.
          </p>
          <button className="pointer-events-auto px-8 py-4 text-lg font-semibold text-white transition-all transform rounded-full bg-cinema-red hover:bg-red-700 hover:scale-105 shadow-[0_0_20px_rgba(229,9,20,0.4)]">
            Ver Filmes em Cartaz
          </button>
        </div>
      </section>

      {/* Movies Grid Section */}
      <section className="relative z-20 w-full min-h-screen px-8 py-24 mx-auto max-w-7xl">
        <div className="flex items-center justify-between mb-12">
          <h2 className="text-4xl font-bold border-l-4 border-cinema-red pl-4">
            Em Cartaz
          </h2>
        </div>

        <div className="grid grid-cols-1 gap-8 sm:grid-cols-2 lg:grid-cols-3">
          {[1, 2, 3, 4, 5, 6].map((item) => (
            <div key={item} className="relative overflow-hidden transition-transform duration-300 group glass-panel hover:-translate-y-2 cursor-pointer h-[450px]">
              {/* Dummy Movie Poster */}
              <div className="absolute inset-0 bg-gray-800 bg-[url('https://images.unsplash.com/photo-1489599849927-2ee91cede3ba?q=80&w=800&auto=format&fit=crop')] bg-cover bg-center opacity-50 group-hover:opacity-70 transition-opacity"></div>
              
              <div className="absolute inset-0 flex flex-col justify-end p-6 bg-gradient-to-t from-cinema-black to-transparent">
                <h3 className="mb-2 text-2xl font-bold">Filme {item}</h3>
                <div className="flex items-center gap-4 text-sm text-gray-300">
                  <span className="flex items-center gap-1"><Ticket size={16}/> Sala VIP</span>
                  <span className="flex items-center gap-1"><Popcorn size={16}/> 120 min</span>
                </div>
              </div>
            </div>
          ))}
        </div>
      </section>
    </>
  )
}

export default App
