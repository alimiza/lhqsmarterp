/**
 * dashboard-switcher.js
 * Populates the navbar switcher dropdown and role selector modal.
 * Depends on: frappe.call (Frappe's jQuery-based AJAX), notification.js
 */

document.addEventListener('DOMContentLoaded', function () {
	loadUserDashboards();
});


function loadUserDashboards() {
	frappe.call({
		method: 'smartapp.api.dashboard.get_user_dashboards',
		callback: function (r) {
			if (!r || !r.message) return;
			const data = r.message;

			// Populate navbar profile info
			const usernameEl = document.getElementById('nav-username');
			const fullnameEl = document.getElementById('profile-fullname');
			const avatarEl   = document.getElementById('avatar-initials');

			if (usernameEl) usernameEl.textContent = data.full_name || data.user || '';
			if (fullnameEl) fullnameEl.textContent = data.full_name || data.user || '';
			if (avatarEl && data.full_name) {
				const initials = data.full_name
					.split(' ')
					.slice(0, 2)
					.map(w => w[0])
					.join('')
					.toUpperCase();
				avatarEl.textContent = initials;
			}

			const dashboards = data.dashboards || [];

			// Show switcher only if user has multiple dashboards
			if (dashboards.length > 1) {
				const wrapper = document.getElementById('switcher-wrapper');
				if (wrapper) wrapper.style.display = '';

				// Populate dropdown list
				const list = document.getElementById('switcher-list');
				if (list) {
					list.innerHTML = dashboards
						.map(d => `
							<a href="${d.route}"
							   class="flex items-center gap-2 px-4 py-2 text-sm text-gray-700 hover:bg-blue-50 hover:text-blue-700 transition-colors">
								<i class="fa-solid fa-grid-2 text-xs text-gray-400"></i>
								${d.label}
							</a>
						`)
						.join('');
				}

				// Show role selector modal on first visit (no localStorage key)
				const key = `smartapp_modal_shown_${data.user}`;
				if (!localStorage.getItem(key)) {
					populateModal(dashboards, data.default_dashboard);
					document.getElementById('role-modal').classList.remove('hidden');
					localStorage.setItem(key, '1');
				}
			}
		},
		error: function () {
			console.warn('SmartApp: Could not load user dashboard info.');
		}
	});
}


function populateModal(dashboards, defaultDashboard) {
	const list = document.getElementById('modal-dashboard-list');
	if (!list) return;

	list.innerHTML = dashboards.map(d => {
		const isDefault = defaultDashboard && d.name === defaultDashboard.name;
		return `
			<a href="${d.route}"
			   class="flex items-center justify-between px-4 py-3 rounded-xl border ${isDefault ? 'border-blue-300 bg-blue-50' : 'border-gray-200 hover:border-blue-200 hover:bg-blue-50'} transition-colors">
				<span class="font-medium text-gray-800 text-sm">${d.label}</span>
				${isDefault ? '<span class="text-xs text-blue-600 font-semibold">Default</span>' : '<i class="fa-solid fa-arrow-right text-xs text-gray-400"></i>'}
			</a>
		`;
	}).join('');
}


function toggleSwitcherMenu() {
	const menu = document.getElementById('switcher-menu');
	if (!menu) return;
	const isHidden = menu.classList.contains('hidden');
	if (isHidden) {
		menu.classList.remove('hidden');
		requestAnimationFrame(() => {
			menu.classList.remove('opacity-0', '-translate-y-1');
		});
	} else {
		menu.classList.add('opacity-0', '-translate-y-1');
		setTimeout(() => menu.classList.add('hidden'), 150);
	}
}


function dismissModal() {
	const modal = document.getElementById('role-modal');
	if (modal) modal.classList.add('hidden');
}


// Close modal on backdrop click
document.addEventListener('click', function (e) {
	const modal = document.getElementById('role-modal');
	if (modal && e.target === modal) dismissModal();
});
