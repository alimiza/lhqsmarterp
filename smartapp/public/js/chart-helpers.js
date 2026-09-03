/**
 * chart-helpers.js
 * Chart.js utility functions for SmartApp dashboards.
 * Requires Chart.js to be loaded before this script.
 */

const SmartChart = {
	_instances: {},

	/**
	 * Create or update a line chart.
	 * @param {string} canvasId - The canvas element id.
	 * @param {string[]} labels - X-axis labels.
	 * @param {Array} datasets - Chart.js dataset objects.
	 * @param {object} options - Optional Chart.js options override.
	 */
	line(canvasId, labels, datasets, options = {}) {
		return this._render(canvasId, 'line', labels, datasets, {
			responsive: true,
			maintainAspectRatio: true,
			plugins: {
				legend: { display: datasets.length > 1, position: 'top' },
				tooltip: { mode: 'index', intersect: false },
			},
			scales: {
				x: { grid: { display: false } },
				y: { beginAtZero: true, grid: { color: '#f3f4f6' } },
			},
			...options,
		});
	},

	/**
	 * Create or update a bar chart.
	 */
	bar(canvasId, labels, datasets, options = {}) {
		return this._render(canvasId, 'bar', labels, datasets, {
			responsive: true,
			maintainAspectRatio: true,
			plugins: {
				legend: { display: datasets.length > 1, position: 'top' },
			},
			scales: {
				x: { grid: { display: false } },
				y: { beginAtZero: true, grid: { color: '#f3f4f6' } },
			},
			...options,
		});
	},

	/**
	 * Create or update a horizontal bar chart.
	 */
	horizontalBar(canvasId, labels, datasets, options = {}) {
		return this._render(canvasId, 'bar', labels, datasets, {
			indexAxis: 'y',
			responsive: true,
			maintainAspectRatio: true,
			plugins: { legend: { display: false } },
			scales: {
				x: { beginAtZero: true, grid: { color: '#f3f4f6' } },
				y: { grid: { display: false } },
			},
			...options,
		});
	},

	/**
	 * Create or update a pie/doughnut chart.
	 */
	doughnut(canvasId, labels, data, colors = [], options = {}) {
		const datasets = [{
			data,
			backgroundColor: colors.length ? colors : this._defaultColors(data.length),
			borderWidth: 2,
			borderColor: '#fff',
		}];
		return this._render(canvasId, 'doughnut', labels, datasets, {
			responsive: true,
			maintainAspectRatio: true,
			plugins: { legend: { position: 'bottom' } },
			...options,
		});
	},

	/**
	 * Destroy all chart instances (call before re-render).
	 */
	destroy(canvasId) {
		if (this._instances[canvasId]) {
			this._instances[canvasId].destroy();
			delete this._instances[canvasId];
		}
	},

	_render(canvasId, type, labels, datasets, options) {
		this.destroy(canvasId);
		const canvas = document.getElementById(canvasId);
		if (!canvas) {
			console.warn(`SmartChart: canvas #${canvasId} not found.`);
			return null;
		}
		const chart = new Chart(canvas, { type, data: { labels, datasets }, options });
		this._instances[canvasId] = chart;
		return chart;
	},

	_defaultColors(count) {
		const palette = [
			'#3b82f6', '#10b981', '#f59e0b', '#ef4444',
			'#8b5cf6', '#06b6d4', '#f97316', '#84cc16',
		];
		return Array.from({ length: count }, (_, i) => palette[i % palette.length]);
	},

	/**
	 * Build a standard single-dataset line dataset.
	 */
	lineDataset(label, data, color = '#3b82f6') {
		return {
			label,
			data,
			borderColor: color,
			backgroundColor: color + '22',
			fill: true,
			tension: 0.4,
			pointRadius: 3,
			pointHoverRadius: 6,
		};
	},

	/**
	 * Build a standard bar dataset.
	 */
	barDataset(label, data, color = '#3b82f6') {
		return {
			label,
			data,
			backgroundColor: color + 'cc',
			borderColor: color,
			borderWidth: 1,
			borderRadius: 4,
		};
	},
};
