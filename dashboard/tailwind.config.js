import preset, { content } from "frappe-ui/tailwind";
// import frappeUIPreset from "frappe-ui/src/tailwind/preset"

/** @type {import('tailwindcss').Config} */
export default {
  presets: [preset],
  content: [...content, './index.html', './src/**/*.{vue,js,ts,jsx,tsx}'],
}

// export default {
// 	presets: [frappeUIPreset],
// 	content: [
// 		"./index.html",
// 		"./src/**/*.{vue,js,ts,jsx,tsx}",
// 		"./node_modules/frappe-ui/src/components/**/*.{vue,js,ts,jsx,tsx}",
// 	],
// 	theme: {
// 		extend: {},
// 	},
// 	plugins: [],
// }
