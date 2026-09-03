/**
 * dashboard-guard.js
 * Detects ?denied=1 in the URL and shows a toast notification.
 * Runs on DOMContentLoaded on every dashboard page.
 */

document.addEventListener('DOMContentLoaded', function () {
	const params = new URLSearchParams(window.location.search);
	if (params.get('denied') === '1') {
		// Show toast after a short delay so notification.js is ready
		setTimeout(function () {
			showToast('Anda tidak memiliki akses ke halaman tersebut.', 'warning', 6000);
		}, 300);

		// Remove ?denied=1 from the URL without reloading
		params.delete('denied');
		const newSearch = params.toString();
		const newUrl = window.location.pathname + (newSearch ? '?' + newSearch : '');
		history.replaceState(null, '', newUrl);
	}
});
