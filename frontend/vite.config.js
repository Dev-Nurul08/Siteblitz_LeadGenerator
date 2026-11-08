import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  // MapLibre's worker module must not be pre-bundled away from its main file.
  optimizeDeps: { exclude: ['maplibre-gl'] },
  server: {
    port: 5173,
    proxy: {
      '/api': 'http://localhost:8000',
      '/health': 'http://localhost:8000',
    }
  }
})
