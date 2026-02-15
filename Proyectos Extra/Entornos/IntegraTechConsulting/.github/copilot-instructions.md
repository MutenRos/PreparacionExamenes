# Integra Tech Consulting - AI Coding Instructions

## Project Overview
Static web application for a consulting firm ("Integra Tech") comprising a public landing page and an internal administration dashboard.
- **Stack:** Vanilla HTML5, CSS3, JavaScript (ES6+).
- **Server:** Python `http.server` (Development).
- **Design System:** "Dark Tech" (Slate/Sky Blue) for UI; "Professional Clean" (Black/White) for documents.

## Architecture & Key Components

### 1. Public Website
- **Entry:** `index.html`
- **Styles:** `styles.css`
- **Logic:** `script.js`
- **Theme:** Dark mode, glassmorphism, tech-oriented aesthetics.

### 2. Admin Dashboard
- **Entry:** `dashboard.html`
- **Modules:**
  - **Calendar:** `agenda.html` + `agenda.js` (Custom vanilla JS month/event logic).
  - **Clients:** `clients.html`, `client-details.html`.
  - **Projects/Budget:** `new-project.html` + `budget-calculator.js`.
- **Styles:** `dashboard.css` (Handles grid layouts, sidebar, and PDF generation styles).

### 3. PDF Generation Engine
- **File:** `budget-calculator.js`
- **Mechanism:** 
  1. User fills "Cuestionario Maestro" form (`new-project.html`).
  2. JS reads values and dynamically constructs a *new* DOM element (`.proposal-document`).
  3. This element is styled specifically for print/PDF (see `dashboard.css` -> `.proposal-document`).
  4. `html2pdf.js` renders this specific element, NOT the screen view.
- **Key Pattern:** Decoupled View. The screen shows a form; the PDF shows a formal contract.

## Development Workflows

### Running the Server
Always run from the project root (`integra-tech-website`):
```bash
python3 -m http.server 8000
```
Access at: `http://localhost:8000`

### PDF Debugging
To debug the PDF layout without downloading:
1. In `budget-calculator.js`, comment out `document.body.removeChild(proposalContainer)`.
2. Trigger PDF generation.
3. Inspect the appended `.proposal-document` at the bottom of the `<body>`.

## Coding Conventions

### HTML/CSS
- **Fonts:** `Space Grotesk` (Headings/Tech), `Manrope` (Body).
- **Colors:** Use CSS variables (`--bg-main`, `--primary`, etc.).
- **Layout:** CSS Grid for dashboards, Flexbox for components.
- **Print Styles:** 
  - Use `@media print` for basic printing.
  - Use `.generating-pdf` class or `.proposal-document` scope for PDF-specific overrides.

### JavaScript
- **No Frameworks:** Use standard DOM APIs (`document.querySelector`, `createElement`).
- **Event Delegation:** Prefer attaching listeners to containers for dynamic lists.
- **Budget Logic:** Ensure `calculateBudget()` in `budget-calculator.js` updates both the UI summary and the internal state for PDF generation.

## Critical Files
- `dashboard.css`: Contains the "AAA Professional" PDF styles at the bottom.
- `budget-calculator.js`: Contains the "Cuestionario Maestro" logic and PDF builder.
- `agenda.js`: Handles the calendar grid generation (watch out for "zombie" static HTML when editing).
