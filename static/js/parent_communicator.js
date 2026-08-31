// EduFlow ERP Client Module — Parent Communicator
document.addEventListener('DOMContentLoaded', () => {
    const moduleContainer = document.querySelector('[data-module="parent_communicator"]');
    console.log('Parent Communicator client module initialized.');

    if (moduleContainer) {
        initModuleEvents(moduleContainer);
    }

    function initModuleEvents(container) {
        const actionBtns = container.querySelectorAll('.btn-action');
        actionBtns.forEach(btn => {
            btn.addEventListener('click', (e) => {
                const action = btn.getAttribute('data-action');
                handleAction(action, btn);
            });
        });
    }

    function handleAction(action, element) {
        console.log('Action trigger: ' + action + ' on ' + element);
        const statusBadge = document.getElementById('status-indicator');
        if (statusBadge) {
            statusBadge.textContent = 'Processing ' + action;
            statusBadge.className = 'badge badge-warning';
            setTimeout(() => {
                statusBadge.textContent = 'Completed';
                statusBadge.className = 'badge badge-success';
            }, 800);
        }
    }

    function renderComponentWidget(data) {
        const widget = document.createElement('div');
        widget.className = 'component-widget-card p-15 border border-radius-6 m-b-15';
        widget.innerHTML = `
            <div class="d-flex justify-content-between align-items-center">
                <strong>Parent Communicator Status</strong>
                <span class="badge badge-primary">Active</span>
            </div>
            <div class="small-text text-muted m-t-5">Last Updated: ` + new Date().toLocaleTimeString() + `</div>
        `;
        return widget;
    }
});
