const monthNames = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"];
let currentDate = new Date(2026, 0, 3); // Start at Jan 2026 based on context

// Dummy events database
const events = {
    "2026-0-2": [
        { type: "event-meeting", title: "10:00 Reunión Logística Norte" },
        { type: "event-work", title: "15:00 Dev Sprint" }
    ],
    "2026-0-5": [
        { type: "event-meeting", title: "11:30 Demo Cliente" }
    ],
    "2026-0-9": [
        { type: "event-deadline", title: "Entrega Prototipo" }
    ],
    "2026-0-15": [
        { type: "event-work", title: "Inicio Fase 2" }
    ],
    "2026-1-10": [
        { type: "event-meeting", title: "Revisión Mensual" }
    ]
};

function renderCalendar() {
    const year = currentDate.getFullYear();
    const month = currentDate.getMonth();

    // Update Header
    document.getElementById('currentMonthDisplay').textContent = `${monthNames[month]} ${year}`;

    const firstDay = new Date(year, month, 1);
    const lastDay = new Date(year, month + 1, 0);
    const prevLastDay = new Date(year, month, 0);
    
    const daysInMonth = lastDay.getDate();
    const daysInPrevMonth = prevLastDay.getDate();
    
    // Adjust for Monday start (0 = Sunday, 1 = Monday, ...)
    let firstDayIndex = firstDay.getDay() - 1; 
    if (firstDayIndex === -1) firstDayIndex = 6; // Sunday becomes 6

    const grid = document.getElementById('calendarGrid');
    
    // Keep headers
    let html = `
        <div class="calendar-day-header">Lun</div>
        <div class="calendar-day-header">Mar</div>
        <div class="calendar-day-header">Mié</div>
        <div class="calendar-day-header">Jue</div>
        <div class="calendar-day-header">Vie</div>
        <div class="calendar-day-header">Sáb</div>
        <div class="calendar-day-header">Dom</div>
    `;

    // Previous month days
    for (let i = firstDayIndex; i > 0; i--) {
        html += `<div class="calendar-day" style="opacity: 0.3"><span class="day-number">${daysInPrevMonth - i + 1}</span></div>`;
    }

    // Current month days
    const today = new Date(); // Real today for highlighting
    
    for (let i = 1; i <= daysInMonth; i++) {
        const isToday = i === today.getDate() && month === today.getMonth() && year === today.getFullYear();
        const dateKey = `${year}-${month}-${i}`;
        const dayEvents = events[dateKey] || [];
        
        let eventsHtml = '';
        dayEvents.forEach(evt => {
            eventsHtml += `<div class="event-chip ${evt.type}">${evt.title}</div>`;
        });

        html += `
            <div class="calendar-day ${isToday ? 'day-today' : ''}">
                <span class="day-number">${i}</span>
                ${eventsHtml}
            </div>
        `;
    }

    // Next month days to fill grid (42 cells total usually 6 rows * 7 cols)
    const totalCells = firstDayIndex + daysInMonth;
    const nextDays = 42 - totalCells;
    
    for (let i = 1; i <= nextDays; i++) {
        html += `<div class="calendar-day" style="opacity: 0.3"><span class="day-number">${i}</span></div>`;
    }

    grid.innerHTML = html;
}

document.getElementById('prevMonth').addEventListener('click', () => {
    currentDate.setMonth(currentDate.getMonth() - 1);
    renderCalendar();
});

document.getElementById('nextMonth').addEventListener('click', () => {
    currentDate.setMonth(currentDate.getMonth() + 1);
    renderCalendar();
});

// Initial render
renderCalendar();
