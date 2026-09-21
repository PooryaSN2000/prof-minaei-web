import { defineConfig } from 'vite';
import tailwindcss from '@tailwindcss/vite';
import { resolve } from 'path';

export default defineConfig({
  base: './',
  plugins: [
    tailwindcss()
  ],
  server: {
    port: 5173
  },
  build: {
    rollupOptions: {
      input: {
        main: resolve(import.meta.dirname, 'index.html'),
        biography: resolve(import.meta.dirname, 'biography.html'),
        publications: resolve(import.meta.dirname, 'publications.html'),
        teaching: resolve(import.meta.dirname, 'teaching.html'),
        students: resolve(import.meta.dirname, 'students.html'),
        contact: resolve(import.meta.dirname, 'contact.html'),
      }
    }
  }
});
