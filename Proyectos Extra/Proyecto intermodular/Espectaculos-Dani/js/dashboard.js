/* ============================================
   ESPECTÁCULOS DANI - DASHBOARD JAVASCRIPT
   ============================================ */

// Database Keys
const DB_KEYS = {
    EVENTS: 'ed_events',
    CLIENTS: 'ed_clients',
    INVOICES: 'ed_invoices',
    HINCHABLES: 'ed_hinchables',
    ATRACCIONES: 'ed_atracciones',
    MOBILIARIO: 'ed_mobiliario',
    EQUIPOS: 'ed_equipos',
    SETTINGS: 'ed_settings'
};

// Current state
let currentSection = 'overview';
let currentDate = new Date();
let editingId = null;

// Initialize
document.addEventListener('DOMContentLoaded', function() {
    initializeSidebar();
    initializeNavigation();
    initializeCalendar();
    initializeSearch();
    loadAllData();
    updateDashboard();
});

// Sidebar Toggle
function initializeSidebar() {
    const menuToggle = document.getElementById('menuToggle');
    const sidebar = document.getElementById('sidebar');
    const mainContent = document.getElementById('mainContent');
    const sidebarClose = document.getElementById('sidebarClose');

    menuToggle.addEventListener('click', () => {
        sidebar.classList.toggle('collapsed');
        sidebar.classList.toggle('active');
        mainContent.classList.toggle('expanded');
    });

    sidebarClose.addEventListener('click', () => {
        sidebar.classList.remove('active');
    });

    // Close sidebar on mobile when clicking outside
    document.addEventListener('click', (e) => {
        if (window.innerWidth <= 768) {
            if (!sidebar.contains(e.target) && !menuToggle.contains(e.target)) {
                sidebar.classList.remove('active');
            }
        }
    });
}

// Navigation
function initializeNavigation() {
    const navLinks = document.querySelectorAll('.sidebar-menu a');
    
    navLinks.forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            const section = link.dataset.section;
            if (section) {
                switchSection(section);
            }
        });
    });

    // Also handle card header links
    document.querySelectorAll('[data-section]').forEach(el => {
        if (!el.closest('.sidebar-menu')) {
            el.addEventListener('click', (e) => {
                e.preventDefault();
                switchSection(el.dataset.section);
            });
        }
    });
}

function switchSection(section) {
    currentSection = section;
    
    // Update active nav
    document.querySelectorAll('.sidebar-menu a').forEach(link => {
        link.classList.remove('active');
        if (link.dataset.section === section) {
            link.classList.add('active');
        }
    });

    // Show section
    document.querySelectorAll('.dashboard-section').forEach(sec => {
        sec.classList.remove('active');
    });
    const targetSection = document.getElementById(`section-${section}`);
    if (targetSection) {
        targetSection.classList.add('active');
    }

    // Close sidebar on mobile
    if (window.innerWidth <= 768) {
        document.getElementById('sidebar').classList.remove('active');
    }

    // Update section-specific data
    updateSectionData(section);
}

function updateSectionData(section) {
    switch(section) {
        case 'calendar':
            renderCalendar();
            break;
        case 'events':
            renderEventsTable();
            break;
        case 'clients':
            renderClientsTable();
            break;
        case 'invoices':
            renderInvoicesTable();
            break;
        case 'hinchables':
        case 'atracciones':
        case 'mobiliario':
        case 'equipos':
            renderInventoryTable(section);
            break;
        case 'income':
            updateIncomeReport();
            break;
    }
}

// Search
function initializeSearch() {
    const globalSearch = document.getElementById('globalSearch');
    if (globalSearch) {
        globalSearch.addEventListener('input', (e) => {
            const query = e.target.value.toLowerCase();
            if (query.length >= 2) {
                performGlobalSearch(query);
            }
        });
    }

    const clientSearch = document.getElementById('clientSearch');
    if (clientSearch) {
        clientSearch.addEventListener('input', (e) => {
            filterClients(e.target.value.toLowerCase());
        });
    }
}

function performGlobalSearch(query) {
    const events = getData(DB_KEYS.EVENTS);
    const clients = getData(DB_KEYS.CLIENTS);
    
    const results = [];
    
    events.forEach(e => {
        if (e.location?.toLowerCase().includes(query) || e.notes?.toLowerCase().includes(query)) {
            results.push({ type: 'event', data: e });
        }
    });
    
    clients.forEach(c => {
        if (c.name?.toLowerCase().includes(query) || c.phone?.includes(query)) {
            results.push({ type: 'client', data: c });
        }
    });
    
    // Could display results in a dropdown - for now just console log
    console.log('Search results:', results);
}

function filterClients(query) {
    const clients = getData(DB_KEYS.CLIENTS);
    const filtered = clients.filter(c => 
        c.name?.toLowerCase().includes(query) || 
        c.phone?.includes(query) ||
        c.email?.toLowerCase().includes(query)
    );
    renderClientsTable(filtered);
}

// Calendar
function initializeCalendar() {
    document.getElementById('prevMonth').addEventListener('click', () => {
        currentDate.setMonth(currentDate.getMonth() - 1);
        renderCalendar();
    });

    document.getElementById('nextMonth').addEventListener('click', () => {
        currentDate.setMonth(currentDate.getMonth() + 1);
        renderCalendar();
    });

    document.getElementById('todayBtn').addEventListener('click', () => {
        currentDate = new Date();
        renderCalendar();
    });
}

function renderCalendar() {
    const grid = document.getElementById('calendarGrid');
    const monthDisplay = document.getElementById('currentMonth');
    
    const year = currentDate.getFullYear();
    const month = currentDate.getMonth();
    
    const months = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 
                    'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'];
    const days = ['Lun', 'Mar', 'Mié', 'Jue', 'Vie', 'Sáb', 'Dom'];
    
    monthDisplay.textContent = `${months[month]} ${year}`;
    
    // Get events for this month
    const events = getData(DB_KEYS.EVENTS);
    const monthEvents = events.filter(e => {
        const eventDate = new Date(e.date);
        return eventDate.getMonth() === month && eventDate.getFullYear() === year;
    });
    
    let html = '';
    
    // Day headers
    days.forEach(day => {
        html += `<div class="calendar-day-header">${day}</div>`;
    });
    
    // Get first day of month and total days
    const firstDay = new Date(year, month, 1).getDay();
    const daysInMonth = new Date(year, month + 1, 0).getDate();
    const daysInPrevMonth = new Date(year, month, 0).getDate();
    
    // Adjust for Monday start
    const startDay = firstDay === 0 ? 6 : firstDay - 1;
    
    // Previous month days
    for (let i = startDay - 1; i >= 0; i--) {
        html += `<div class="calendar-day other-month"><span class="day-number">${daysInPrevMonth - i}</span></div>`;
    }
    
    // Current month days
    const today = new Date();
    for (let day = 1; day <= daysInMonth; day++) {
        const isToday = day === today.getDate() && month === today.getMonth() && year === today.getFullYear();
        const dayEvents = monthEvents.filter(e => new Date(e.date).getDate() === day);
        
        html += `<div class="calendar-day${isToday ? ' today' : ''}" onclick="openEventModal(null, '${year}-${String(month+1).padStart(2,'0')}-${String(day).padStart(2,'0')}')">`;
        html += `<span class="day-number">${day}</span>`;
        
        dayEvents.forEach(event => {
            const clients = getData(DB_KEYS.CLIENTS);
            const client = clients.find(c => c.id === parseInt(event.clientId));
            html += `<div class="calendar-event ${event.service}" onclick="event.stopPropagation(); editEvent(${event.id})">${client?.name || 'Sin cliente'}</div>`;
        });
        
        html += '</div>';
    }
    
    // Next month days
    const totalCells = 42;
    const usedCells = startDay + daysInMonth;
    const remaining = totalCells - usedCells;
    
    for (let i = 1; i <= remaining; i++) {
        html += `<div class="calendar-day other-month"><span class="day-number">${i}</span></div>`;
    }
    
    grid.innerHTML = html;
}

// Data Management
function getData(key) {
    return JSON.parse(localStorage.getItem(key) || '[]');
}

function setData(key, data) {
    localStorage.setItem(key, JSON.stringify(data));
}

function loadAllData() {
    // Initialize with empty arrays if not exist
    Object.values(DB_KEYS).forEach(key => {
        if (!localStorage.getItem(key)) {
            if (key === DB_KEYS.SETTINGS) {
                setData(key, {
                    companyName: 'Espectáculos Dani',
                    companyAddress: 'Valencia, España',
                    companyPhone: '661 725 756',
                    companyEmail: 'info@espectaculosdani.es'
                });
            } else {
                setData(key, []);
            }
        }
    });
}

// Dashboard Updates
function updateDashboard() {
    const events = getData(DB_KEYS.EVENTS);
    const clients = getData(DB_KEYS.CLIENTS);
    
    // Count events this month
    const now = new Date();
    const thisMonthEvents = events.filter(e => {
        const eventDate = new Date(e.date);
        return eventDate.getMonth() === now.getMonth() && eventDate.getFullYear() === now.getFullYear();
    });
    
    // Calculate income
    const monthIncome = thisMonthEvents
        .filter(e => e.status !== 'cancelled')
        .reduce((sum, e) => sum + parseFloat(e.price || 0), 0);
    
    // Count inventory items
    const inventoryCount = 
        getData(DB_KEYS.HINCHABLES).length +
        getData(DB_KEYS.ATRACCIONES).length +
        getData(DB_KEYS.MOBILIARIO).length +
        getData(DB_KEYS.EQUIPOS).length;
    
    // Update stats
    document.getElementById('statEvents').textContent = thisMonthEvents.length;
    document.getElementById('statIncome').textContent = formatCurrency(monthIncome);
    document.getElementById('statClients').textContent = clients.length;
    document.getElementById('statItems').textContent = inventoryCount;
    
    // Update badge
    const pendingEvents = events.filter(e => e.status === 'pending').length;
    document.getElementById('eventsBadge').textContent = pendingEvents;
    
    // Update upcoming events table
    renderUpcomingEvents();
    
    // Update recent clients
    renderRecentClients();
}

function renderUpcomingEvents() {
    const events = getData(DB_KEYS.EVENTS);
    const clients = getData(DB_KEYS.CLIENTS);
    const tbody = document.getElementById('upcomingEventsTable');
    
    const upcoming = events
        .filter(e => new Date(e.date) >= new Date() && e.status !== 'cancelled')
        .sort((a, b) => new Date(a.date) - new Date(b.date))
        .slice(0, 5);
    
    if (upcoming.length === 0) {
        tbody.innerHTML = '<tr><td colspan="3" class="text-center">No hay eventos próximos</td></tr>';
        return;
    }
    
    tbody.innerHTML = upcoming.map(event => {
        const client = clients.find(c => c.id === parseInt(event.clientId));
        return `
            <tr>
                <td>${client?.name || 'Sin cliente'}</td>
                <td>${formatDate(event.date)}</td>
                <td><span class="status status-${event.status}">${getStatusText(event.status)}</span></td>
            </tr>
        `;
    }).join('');
}

function renderRecentClients() {
    const clients = getData(DB_KEYS.CLIENTS);
    const events = getData(DB_KEYS.EVENTS);
    const tbody = document.getElementById('recentClientsTable');
    
    const recent = clients.slice(-5).reverse();
    
    if (recent.length === 0) {
        tbody.innerHTML = '<tr><td colspan="5" class="text-center">No hay clientes registrados</td></tr>';
        return;
    }
    
    tbody.innerHTML = recent.map(client => {
        const clientEvents = events.filter(e => e.clientId === client.id.toString()).length;
        return `
            <tr>
                <td>${client.name}</td>
                <td>${client.phone}</td>
                <td>${client.email || '-'}</td>
                <td>${clientEvents}</td>
                <td class="table-actions">
                    <button class="btn btn-sm btn-secondary btn-icon" onclick="editClient(${client.id})"><i class="fas fa-edit"></i></button>
                </td>
            </tr>
        `;
    }).join('');
}

// Events Management
function openEventModal(id = null, date = null) {
    editingId = id;
    const modal = document.getElementById('eventModal');
    const form = document.getElementById('eventForm');
    const title = document.getElementById('eventModalTitle');
    
    // Populate client select
    const clientSelect = document.getElementById('eventClient');
    const clients = getData(DB_KEYS.CLIENTS);
    clientSelect.innerHTML = '<option value="">Seleccionar cliente...</option>' +
        clients.map(c => `<option value="${c.id}">${c.name}</option>`).join('');
    
    if (id) {
        title.textContent = 'Editar Evento';
        const events = getData(DB_KEYS.EVENTS);
        const event = events.find(e => e.id === id);
        if (event) {
            document.getElementById('eventId').value = event.id;
            document.getElementById('eventClient').value = event.clientId;
            document.getElementById('eventService').value = event.service;
            document.getElementById('eventDate').value = event.date;
            document.getElementById('eventTime').value = event.time || '';
            document.getElementById('eventLocation').value = event.location || '';
            document.getElementById('eventPrice').value = event.price;
            document.getElementById('eventStatus').value = event.status;
            document.getElementById('eventNotes').value = event.notes || '';
        }
    } else {
        title.textContent = 'Nuevo Evento';
        form.reset();
        document.getElementById('eventId').value = '';
        if (date) {
            document.getElementById('eventDate').value = date;
        }
    }
    
    modal.classList.add('active');
}

function saveEvent() {
    const id = document.getElementById('eventId').value;
    const eventData = {
        clientId: document.getElementById('eventClient').value,
        service: document.getElementById('eventService').value,
        date: document.getElementById('eventDate').value,
        time: document.getElementById('eventTime').value,
        location: document.getElementById('eventLocation').value,
        price: document.getElementById('eventPrice').value,
        status: document.getElementById('eventStatus').value,
        notes: document.getElementById('eventNotes').value
    };
    
    if (!eventData.clientId || !eventData.service || !eventData.date || !eventData.price) {
        showToast('Por favor, completa los campos obligatorios', 'error');
        return;
    }
    
    const events = getData(DB_KEYS.EVENTS);
    
    if (id) {
        const index = events.findIndex(e => e.id === parseInt(id));
        if (index !== -1) {
            events[index] = { ...events[index], ...eventData };
        }
        showToast('Evento actualizado correctamente', 'success');
    } else {
        eventData.id = Date.now();
        eventData.createdAt = new Date().toISOString();
        events.push(eventData);
        showToast('Evento creado correctamente', 'success');
    }
    
    setData(DB_KEYS.EVENTS, events);
    closeModal('eventModal');
    updateDashboard();
    
    if (currentSection === 'events') {
        renderEventsTable();
    } else if (currentSection === 'calendar') {
        renderCalendar();
    }
}

function editEvent(id) {
    openEventModal(id);
}

function deleteEvent(id) {
    if (confirm('¿Estás seguro de eliminar este evento?')) {
        let events = getData(DB_KEYS.EVENTS);
        events = events.filter(e => e.id !== id);
        setData(DB_KEYS.EVENTS, events);
        showToast('Evento eliminado', 'success');
        updateDashboard();
        renderEventsTable();
    }
}

function renderEventsTable(eventsData = null) {
    const events = eventsData || getData(DB_KEYS.EVENTS);
    const clients = getData(DB_KEYS.CLIENTS);
    const tbody = document.getElementById('eventsTable');
    const filter = document.getElementById('eventFilter')?.value || 'all';
    
    let filtered = events;
    if (filter !== 'all') {
        filtered = events.filter(e => e.status === filter);
    }
    
    if (filtered.length === 0) {
        tbody.innerHTML = '<tr><td colspan="7" class="text-center">No hay eventos registrados</td></tr>';
        return;
    }
    
    // Sort by date descending
    filtered.sort((a, b) => new Date(b.date) - new Date(a.date));
    
    tbody.innerHTML = filtered.map(event => {
        const client = clients.find(c => c.id === parseInt(event.clientId));
        return `
            <tr>
                <td>${client?.name || 'Sin cliente'}</td>
                <td>${getServiceName(event.service)}</td>
                <td>${formatDate(event.date)}</td>
                <td>${event.location || '-'}</td>
                <td>${formatCurrency(event.price)}</td>
                <td><span class="status status-${event.status}">${getStatusText(event.status)}</span></td>
                <td class="table-actions">
                    <button class="btn btn-sm btn-secondary btn-icon" onclick="editEvent(${event.id})"><i class="fas fa-edit"></i></button>
                    <button class="btn btn-sm btn-danger btn-icon" onclick="deleteEvent(${event.id})"><i class="fas fa-trash"></i></button>
                </td>
            </tr>
        `;
    }).join('');
}

// Event filter listener
document.getElementById('eventFilter')?.addEventListener('change', () => renderEventsTable());

// Clients Management
function openClientModal(id = null) {
    editingId = id;
    const modal = document.getElementById('clientModal');
    const form = document.getElementById('clientForm');
    const title = document.getElementById('clientModalTitle');
    
    if (id) {
        title.textContent = 'Editar Cliente';
        const clients = getData(DB_KEYS.CLIENTS);
        const client = clients.find(c => c.id === id);
        if (client) {
            document.getElementById('clientId').value = client.id;
            document.getElementById('clientName').value = client.name;
            document.getElementById('clientPhone').value = client.phone;
            document.getElementById('clientEmail').value = client.email || '';
            document.getElementById('clientAddress').value = client.address || '';
            document.getElementById('clientNotes').value = client.notes || '';
        }
    } else {
        title.textContent = 'Nuevo Cliente';
        form.reset();
        document.getElementById('clientId').value = '';
    }
    
    modal.classList.add('active');
}

function saveClient() {
    const id = document.getElementById('clientId').value;
    const clientData = {
        name: document.getElementById('clientName').value,
        phone: document.getElementById('clientPhone').value,
        email: document.getElementById('clientEmail').value,
        address: document.getElementById('clientAddress').value,
        notes: document.getElementById('clientNotes').value
    };
    
    if (!clientData.name || !clientData.phone) {
        showToast('Por favor, completa los campos obligatorios', 'error');
        return;
    }
    
    const clients = getData(DB_KEYS.CLIENTS);
    
    if (id) {
        const index = clients.findIndex(c => c.id === parseInt(id));
        if (index !== -1) {
            clients[index] = { ...clients[index], ...clientData };
        }
        showToast('Cliente actualizado correctamente', 'success');
    } else {
        clientData.id = Date.now();
        clientData.createdAt = new Date().toISOString();
        clients.push(clientData);
        showToast('Cliente creado correctamente', 'success');
    }
    
    setData(DB_KEYS.CLIENTS, clients);
    closeModal('clientModal');
    updateDashboard();
    
    if (currentSection === 'clients') {
        renderClientsTable();
    }
}

function editClient(id) {
    openClientModal(id);
}

function deleteClient(id) {
    if (confirm('¿Estás seguro de eliminar este cliente? Se eliminarán también sus eventos asociados.')) {
        let clients = getData(DB_KEYS.CLIENTS);
        let events = getData(DB_KEYS.EVENTS);
        
        clients = clients.filter(c => c.id !== id);
        events = events.filter(e => e.clientId !== id.toString());
        
        setData(DB_KEYS.CLIENTS, clients);
        setData(DB_KEYS.EVENTS, events);
        
        showToast('Cliente eliminado', 'success');
        updateDashboard();
        renderClientsTable();
    }
}

function renderClientsTable(clientsData = null) {
    const clients = clientsData || getData(DB_KEYS.CLIENTS);
    const events = getData(DB_KEYS.EVENTS);
    const tbody = document.getElementById('clientsTable');
    
    if (clients.length === 0) {
        tbody.innerHTML = '<tr><td colspan="6" class="text-center">No hay clientes registrados</td></tr>';
        return;
    }
    
    tbody.innerHTML = clients.map(client => {
        const clientEvents = events.filter(e => e.clientId === client.id.toString()).length;
        return `
            <tr>
                <td>${client.name}</td>
                <td>${client.phone}</td>
                <td>${client.email || '-'}</td>
                <td>${client.address || '-'}</td>
                <td>${clientEvents}</td>
                <td class="table-actions">
                    <button class="btn btn-sm btn-secondary btn-icon" onclick="editClient(${client.id})"><i class="fas fa-edit"></i></button>
                    <button class="btn btn-sm btn-danger btn-icon" onclick="deleteClient(${client.id})"><i class="fas fa-trash"></i></button>
                </td>
            </tr>
        `;
    }).join('');
}

// Inventory Management
function openInventoryModal(category, id = null) {
    editingId = id;
    const modal = document.getElementById('inventoryModal');
    const form = document.getElementById('inventoryForm');
    const title = document.getElementById('inventoryModalTitle');
    const detailLabel = document.getElementById('inventoryDetailLabel');
    
    document.getElementById('inventoryCategory').value = category;
    
    // Set appropriate label
    switch(category) {
        case 'hinchables':
            detailLabel.textContent = 'Dimensiones';
            break;
        case 'atracciones':
            detailLabel.textContent = 'Capacidad';
            break;
        case 'mobiliario':
            detailLabel.textContent = 'Cantidad';
            break;
        case 'equipos':
            detailLabel.textContent = 'Tipo';
            break;
    }
    
    if (id) {
        title.textContent = 'Editar Item';
        const items = getData(DB_KEYS[category.toUpperCase()]);
        const item = items.find(i => i.id === id);
        if (item) {
            document.getElementById('inventoryId').value = item.id;
            document.getElementById('inventoryName').value = item.name;
            document.getElementById('inventoryDetail').value = item.detail || '';
            document.getElementById('inventoryPrice').value = item.price;
            document.getElementById('inventoryStatus').value = item.status;
        }
    } else {
        title.textContent = 'Añadir Item';
        form.reset();
        document.getElementById('inventoryId').value = '';
    }
    
    modal.classList.add('active');
}

function saveInventoryItem() {
    const id = document.getElementById('inventoryId').value;
    const category = document.getElementById('inventoryCategory').value;
    const itemData = {
        name: document.getElementById('inventoryName').value,
        detail: document.getElementById('inventoryDetail').value,
        price: document.getElementById('inventoryPrice').value,
        status: document.getElementById('inventoryStatus').value
    };
    
    if (!itemData.name || !itemData.price) {
        showToast('Por favor, completa los campos obligatorios', 'error');
        return;
    }
    
    const key = DB_KEYS[category.toUpperCase()];
    const items = getData(key);
    
    if (id) {
        const index = items.findIndex(i => i.id === parseInt(id));
        if (index !== -1) {
            items[index] = { ...items[index], ...itemData };
        }
        showToast('Item actualizado correctamente', 'success');
    } else {
        itemData.id = Date.now();
        items.push(itemData);
        showToast('Item añadido correctamente', 'success');
    }
    
    setData(key, items);
    closeModal('inventoryModal');
    updateDashboard();
    renderInventoryTable(category);
}

function editInventoryItem(category, id) {
    openInventoryModal(category, id);
}

function deleteInventoryItem(category, id) {
    if (confirm('¿Estás seguro de eliminar este item?')) {
        const key = DB_KEYS[category.toUpperCase()];
        let items = getData(key);
        items = items.filter(i => i.id !== id);
        setData(key, items);
        showToast('Item eliminado', 'success');
        updateDashboard();
        renderInventoryTable(category);
    }
}

function renderInventoryTable(category) {
    const key = DB_KEYS[category.toUpperCase()];
    const items = getData(key);
    const tbody = document.getElementById(`${category}Table`);
    
    if (items.length === 0) {
        tbody.innerHTML = `<tr><td colspan="5" class="text-center">No hay ${category} registrados</td></tr>`;
        return;
    }
    
    tbody.innerHTML = items.map(item => `
        <tr>
            <td>${item.name}</td>
            <td>${item.detail || '-'}</td>
            <td>${formatCurrency(item.price)}</td>
            <td><span class="status status-${item.status}">${getInventoryStatusText(item.status)}</span></td>
            <td class="table-actions">
                <button class="btn btn-sm btn-secondary btn-icon" onclick="editInventoryItem('${category}', ${item.id})"><i class="fas fa-edit"></i></button>
                <button class="btn btn-sm btn-danger btn-icon" onclick="deleteInventoryItem('${category}', ${item.id})"><i class="fas fa-trash"></i></button>
            </td>
        </tr>
    `).join('');
}

// Invoices
function openInvoiceModal() {
    showToast('Función de facturación en desarrollo', 'warning');
}

function renderInvoicesTable() {
    const invoices = getData(DB_KEYS.INVOICES);
    const tbody = document.getElementById('invoicesTable');
    
    if (invoices.length === 0) {
        tbody.innerHTML = '<tr><td colspan="6" class="text-center">No hay facturas registradas</td></tr>';
        return;
    }
    
    // Render invoices...
}

// Income Report
function updateIncomeReport() {
    const events = getData(DB_KEYS.EVENTS);
    const year = parseInt(document.getElementById('incomeYear')?.value || new Date().getFullYear());
    
    const yearEvents = events.filter(e => {
        const eventYear = new Date(e.date).getFullYear();
        return eventYear === year && e.status !== 'cancelled';
    });
    
    const yearlyIncome = yearEvents.reduce((sum, e) => sum + parseFloat(e.price || 0), 0);
    const avgEvent = yearEvents.length > 0 ? yearlyIncome / yearEvents.length : 0;
    
    // Find best month
    const monthTotals = {};
    yearEvents.forEach(e => {
        const month = new Date(e.date).getMonth();
        monthTotals[month] = (monthTotals[month] || 0) + parseFloat(e.price || 0);
    });
    
    const months = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 
                    'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'];
    
    let bestMonth = '-';
    let maxIncome = 0;
    Object.entries(monthTotals).forEach(([month, total]) => {
        if (total > maxIncome) {
            maxIncome = total;
            bestMonth = months[parseInt(month)];
        }
    });
    
    // Find top service
    const serviceCounts = {};
    yearEvents.forEach(e => {
        serviceCounts[e.service] = (serviceCounts[e.service] || 0) + 1;
    });
    
    let topService = '-';
    let maxCount = 0;
    Object.entries(serviceCounts).forEach(([service, count]) => {
        if (count > maxCount) {
            maxCount = count;
            topService = getServiceName(service);
        }
    });
    
    document.getElementById('yearlyIncome').textContent = formatCurrency(yearlyIncome);
    document.getElementById('avgEvent').textContent = formatCurrency(avgEvent);
    document.getElementById('bestMonth').textContent = bestMonth;
    document.getElementById('topService').textContent = topService;
}

document.getElementById('incomeYear')?.addEventListener('change', updateIncomeReport);

// Settings
function saveSettings() {
    const settings = {
        companyName: document.getElementById('companyName').value,
        companyCIF: document.getElementById('companyCIF').value,
        companyAddress: document.getElementById('companyAddress').value,
        companyPhone: document.getElementById('companyPhone').value,
        companyEmail: document.getElementById('companyEmail').value
    };
    
    setData(DB_KEYS.SETTINGS, settings);
    showToast('Configuración guardada correctamente', 'success');
}

function exportData() {
    const data = {
        events: getData(DB_KEYS.EVENTS),
        clients: getData(DB_KEYS.CLIENTS),
        invoices: getData(DB_KEYS.INVOICES),
        hinchables: getData(DB_KEYS.HINCHABLES),
        atracciones: getData(DB_KEYS.ATRACCIONES),
        mobiliario: getData(DB_KEYS.MOBILIARIO),
        equipos: getData(DB_KEYS.EQUIPOS),
        settings: getData(DB_KEYS.SETTINGS),
        exportDate: new Date().toISOString()
    };
    
    const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `espectaculos-dani-backup-${new Date().toISOString().split('T')[0]}.json`;
    a.click();
    URL.revokeObjectURL(url);
    
    showToast('Datos exportados correctamente', 'success');
}

function importData(event) {
    const file = event.target.files[0];
    if (!file) return;
    
    const reader = new FileReader();
    reader.onload = function(e) {
        try {
            const data = JSON.parse(e.target.result);
            
            if (data.events) setData(DB_KEYS.EVENTS, data.events);
            if (data.clients) setData(DB_KEYS.CLIENTS, data.clients);
            if (data.invoices) setData(DB_KEYS.INVOICES, data.invoices);
            if (data.hinchables) setData(DB_KEYS.HINCHABLES, data.hinchables);
            if (data.atracciones) setData(DB_KEYS.ATRACCIONES, data.atracciones);
            if (data.mobiliario) setData(DB_KEYS.MOBILIARIO, data.mobiliario);
            if (data.equipos) setData(DB_KEYS.EQUIPOS, data.equipos);
            if (data.settings) setData(DB_KEYS.SETTINGS, data.settings);
            
            showToast('Datos importados correctamente', 'success');
            updateDashboard();
            
        } catch (error) {
            showToast('Error al importar datos: archivo inválido', 'error');
        }
    };
    reader.readAsText(file);
}

function clearAllData() {
    if (confirm('¿Estás seguro de borrar TODOS los datos? Esta acción no se puede deshacer.')) {
        Object.values(DB_KEYS).forEach(key => localStorage.removeItem(key));
        loadAllData();
        updateDashboard();
        showToast('Todos los datos han sido eliminados', 'success');
    }
}

// Modal Management
function closeModal(modalId) {
    document.getElementById(modalId).classList.remove('active');
    editingId = null;
}

// Close modal on click outside
document.querySelectorAll('.modal').forEach(modal => {
    modal.addEventListener('click', (e) => {
        if (e.target === modal) {
            modal.classList.remove('active');
            editingId = null;
        }
    });
});

// Close modal on Escape key
document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
        document.querySelectorAll('.modal.active').forEach(modal => {
            modal.classList.remove('active');
        });
        editingId = null;
    }
});

// Toast Notifications
function showToast(message, type = 'success') {
    const container = document.getElementById('toastContainer');
    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    
    const icons = {
        success: 'fa-check',
        error: 'fa-times',
        warning: 'fa-exclamation'
    };
    
    toast.innerHTML = `
        <div class="toast-icon"><i class="fas ${icons[type]}"></i></div>
        <div class="toast-content">
            <div class="toast-title">${type === 'success' ? 'Éxito' : type === 'error' ? 'Error' : 'Aviso'}</div>
            <div class="toast-message">${message}</div>
        </div>
        <button class="toast-close" onclick="this.parentElement.remove()"><i class="fas fa-times"></i></button>
    `;
    
    container.appendChild(toast);
    
    // Trigger animation
    setTimeout(() => toast.classList.add('show'), 10);
    
    // Auto remove
    setTimeout(() => {
        toast.classList.remove('show');
        setTimeout(() => toast.remove(), 300);
    }, 4000);
}

// Utility Functions
function formatDate(dateString) {
    const options = { day: 'numeric', month: 'short', year: 'numeric' };
    return new Date(dateString).toLocaleDateString('es-ES', options);
}

function formatCurrency(amount) {
    return new Intl.NumberFormat('es-ES', {
        style: 'currency',
        currency: 'EUR',
        minimumFractionDigits: 0
    }).format(amount);
}

function getStatusText(status) {
    const statuses = {
        pending: 'Pendiente',
        confirmed: 'Confirmado',
        completed: 'Completado',
        cancelled: 'Cancelado'
    };
    return statuses[status] || status;
}

function getInventoryStatusText(status) {
    const statuses = {
        available: 'Disponible',
        rented: 'Alquilado',
        maintenance: 'Mantenimiento'
    };
    return statuses[status] || status;
}

function getServiceName(service) {
    const services = {
        hinchables: 'Hinchables',
        atracciones: 'Atracciones Mecánicas',
        megafonia: 'Megafonía',
        mobiliario: 'Mobiliario',
        disco: 'Disco Móvil',
        espuma: 'Cañón de Espuma',
        escenario: 'Escenario'
    };
    return services[service] || service;
}
