import path from "node:path"
import vue from "@vitejs/plugin-vue"
import frappeui from "frappe-ui/vite"
import { defineConfig } from "vite"

// https://vitejs.dev/config/
export default defineConfig({
	plugins: [
		frappeui({
			frappeProxy: "http://smarterp.localhost:8001",
			jinjaBootData: true,
			lucideIcons: true,
			buildConfig: {
				outDir: "../smartapp/public/dashboard",
				indexHtmlPath: "../smartapp/www/dashboard.html",
				emptyOutDir: true,
				sourcemap: true,
			},
		}),
		vue(),
	],
	build: {
		chunkSizeWarningLimit: 1500,
		outDir: "../smartapp/public/dashboard",
		emptyOutDir: true,
		target: "es2015",
		sourcemap: true,
	},
	resolve: {
		alias: {
			"@": path.resolve(__dirname, "src"),
			"tailwind.config.js": path.resolve(__dirname, "tailwind.config.js"),
		},
	},
	optimizeDeps: {
		include: ["feather-icons", "showdown", "highlight.js/lib/core", "interactjs"],
	},
	server: {
		port: 8081,
        host: "0.0.0.0", // Agar dapat diakses dari luar container Docker
		allowedHosts: true,
		watch: {
			usePolling: true, // Memaksa Vite memeriksa perubahan file secara bertahap
			interval: 100,    // Interval pemeriksaan dalam milidetik
		},
	},
});
