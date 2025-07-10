import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      '/prompts': 'http://localhost:8000',
      '/images': 'http://localhost:8000',
      '/music': 'http://localhost:8000',
      '/render': 'http://localhost:8000',
      '/lora': 'http://localhost:8000',
      '/static': 'http://localhost:8000'
    }
  }
});
