import { defineConfig, loadEnv } from "vite";
import react from "@vitejs/plugin-react";

// https://vitejs.dev/config/
export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, "./");
  const BASE_PATH = env.VITE_BASE_PATH;
  const PROXY = env.VITE_PROXY;
  return {
    base: BASE_PATH,
    plugins: [react()],
    server: {
      https: {
        cert: "certs/cert.pem",
        key: "certs/key.pem",
      },
      // watch: { cwd: "./app" },
      proxy: {
        "/api": {
          target: PROXY,
          changeOrigin: true,
          secure: false,
          rewrite: (path) => path.replace(/^\/api/, ""),
        },
      },
    },
  };
});
