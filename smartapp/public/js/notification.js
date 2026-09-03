/**
 * notification.js
 * Toast notification helper for SmartApp dashboards.
 * Usage: showToast('Pesan', 'success' | 'error' | 'warning' | 'info')
 */

function showToast(message, type = 'info', duration = 4000) {
	const container = document.getElementById('toast-container');
	if (!container) return;

	const icons = {
		success: 'fa-circle-check text-green-500',
		error:   'fa-circle-xmark text-red-500',
		warning: 'fa-triangle-exclamation text-yellow-500',
		info:    'fa-circle-info text-blue-500',
	};

	const bg = {
		success: 'bg-white border-green-200',
		error:   'bg-white border-red-200',
		warning: 'bg-white border-yellow-200',
		info:    'bg-white border-blue-200',
	};

	const toast = document.createElement('div');
	toast.className = `toast flex items-center gap-3 px-4 py-3 rounded-xl shadow-lg border text-sm text-gray-700 ${bg[type] || bg.info} transform translate-x-full transition-transform duration-300`;
	toast.innerHTML = `
		<i class="fa-solid ${icons[type] || icons.info} text-base flex-shrink-0"></i>
		<span>${message}</span>
		<button onclick="this.closest('.toast').remove()" class="ml-auto text-gray-300 hover:text-gray-500 flex-shrink-0">
			<i class="fa-solid fa-xmark text-xs"></i>
		</button>
	`;

	container.appendChild(toast);

	// Slide in
	requestAnimationFrame(() => {
		requestAnimationFrame(() => {
			toast.classList.remove('translate-x-full');
		});
	});

	// Auto remove
	setTimeout(() => {
		toast.classList.add('translate-x-full');
		setTimeout(() => toast.remove(), 350);
	}, duration);
}
