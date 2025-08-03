import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import path from "path";
import { fileURLToPath } from "url";
import fs from "fs";

// Corrige __dirname em ESM
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Checar se os certificados existem antes de usar HTTPS
const useHttps = process.env.NODE_ENV !== "production" &&
  fs.existsSync(path.resolve(__dirname, "certs/key.pem")) &&
  fs.existsSync(path.resolve(__dirname, "certs/cert.pem"));

export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "src"),
    },
  },
  server: {
    host: "0.0.0.0",
    port: 5173,
    ...(useHttps && {
      https: {
        key: fs.readFileSync(path.resolve(__dirname, "certs/key.pem")),
        cert: fs.readFileSync(path.resolve(__dirname, "certs/cert.pem")),
      },
    }),
  },
});
