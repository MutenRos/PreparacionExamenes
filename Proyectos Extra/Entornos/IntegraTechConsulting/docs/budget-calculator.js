document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('budgetForm');
    
    // Inputs
    const blueprintRadios = document.getElementsByName('blueprint');
    const webTypeSelect = document.getElementById('webType');
    const supportPlanSelect = document.getElementById('supportPlan');
    const deadlineMultSelect = document.getElementById('deadlineMult');
    const complexityMultSelect = document.getElementById('complexityMult');
    const pmMultSelect = document.getElementById('pmMult');
    
    // Dynamic Inputs (Qty & Checkboxes)
    const qtyInputs = document.querySelectorAll('.qty-input[data-price]');
    const featureChecks = document.querySelectorAll('.feature-check');

    // Output Elements
    const sumBlueprintEl = document.getElementById('sumBlueprint');
    const sumImplementationEl = document.getElementById('sumImplementation');
    const sumMultipliersEl = document.getElementById('sumMultipliers');
    const sumPMEl = document.getElementById('sumPM');
    const totalAmountEl = document.getElementById('totalAmount');
    const monthlyAmountEl = document.getElementById('monthlyAmount');

    function formatCurrency(amount) {
        return new Intl.NumberFormat('es-ES', { style: 'currency', currency: 'EUR', maximumFractionDigits: 0 }).format(amount);
    }

    function calculateBudget() {
        let blueprintCost = 0;
        let implementationBase = 0;
        let monthlyCost = 0;

        // 1. Blueprint
        for (const radio of blueprintRadios) {
            if (radio.checked) {
                blueprintCost = parseFloat(radio.value);
                break;
            }
        }

        // 2. Web Type
        implementationBase += parseFloat(webTypeSelect.value || 0);

        // 3. Quantity Inputs
        qtyInputs.forEach(input => {
            const qty = parseFloat(input.value || 0);
            const price = parseFloat(input.dataset.price);
            if (qty > 0) {
                implementationBase += qty * price;
            }
        });

        // 4. Checkboxes
        featureChecks.forEach(check => {
            if (check.checked) {
                implementationBase += parseFloat(check.value);
            }
        });

        // 5. Training (is a qty input, already handled)

        // 6. Support (Monthly)
        monthlyCost = parseFloat(supportPlanSelect.value || 0);

        // Total Base for Multipliers (Includes Blueprint + Implementation)
        // The prompt says: Subtotal = Blueprint + Web + ... 
        // Implementación = Subtotal
        // So Blueprint IS part of the base.
        const totalBase = blueprintCost + implementationBase;

        // 7. Multipliers
        const deadlineMult = parseFloat(deadlineMultSelect.value);
        const complexityMult = parseFloat(complexityMultSelect.value);
        const combinedMult = deadlineMult * complexityMult;

        const multipliedBase = totalBase * combinedMult;

        // 8. PM
        const pmRate = parseFloat(pmMultSelect.value);
        const pmCost = multipliedBase * pmRate;

        // 9. Final Total
        const finalTotal = multipliedBase + pmCost;

        // Update UI
        sumBlueprintEl.textContent = formatCurrency(blueprintCost);
        sumImplementationEl.textContent = formatCurrency(implementationBase);
        sumMultipliersEl.textContent = `x${combinedMult.toFixed(2)} (Plazo x${deadlineMult} · Comp x${complexityMult})`;
        sumPMEl.textContent = formatCurrency(pmCost);
        
        totalAmountEl.textContent = formatCurrency(finalTotal);
        monthlyAmountEl.textContent = `${formatCurrency(monthlyCost)}/mes`;
    }

    // Event Listeners
    form.addEventListener('input', calculateBudget);
    form.addEventListener('change', calculateBudget);

    // Initial Calculation
    calculateBudget();

    // Set Date in PDF Header
    const dateEl = document.getElementById('pdfDate');
    if (dateEl) {
        dateEl.textContent = new Date().toLocaleDateString('es-ES', { year: 'numeric', month: 'long', day: 'numeric' });
    }

    // Print & PDF Logic
    const btnPrint = document.getElementById('btnPrint');
    const btnPdf = document.getElementById('btnPdf');
    const actionButtons = document.querySelector('.action-buttons');

    if (btnPrint) {
        btnPrint.addEventListener('click', () => {
            window.print();
        });
    }

    if (btnPdf) {
        btnPdf.addEventListener('click', () => {
            // 1. Create a temporary container for the proposal
            const proposalContainer = document.createElement('div');
            proposalContainer.className = 'proposal-document';
            
            // 2. Build the content
            // Header
            const dateStr = new Date().toLocaleDateString('es-ES', { year: 'numeric', month: 'long', day: 'numeric' });
            
            // Get values
            const projectNameInput = document.querySelector('input[placeholder*="Portal Clientes"]');
            const projectName = projectNameInput ? projectNameInput.value : 'Sin Nombre';
            const clientName = "Logística Norte S.L."; 
            
            let html = `
                <div class="prop-header">
                    <div class="prop-brand">INTEGRA TECH <span style="color:#666; font-weight:400;">CONSULTING</span></div>
                    <div class="prop-meta">
                        <div><strong>FECHA:</strong> ${dateStr}</div>
                        <div><strong>CLIENTE:</strong> ${clientName}</div>
                        <div><strong>PROYECTO:</strong> ${projectName}</div>
                    </div>
                </div>
                
                <div class="prop-title">
                    <h1>PROPUESTA DE SERVICIOS</h1>
                    <div class="prop-subtitle">DEFINICIÓN DE ALCANCE Y PRESUPUESTO</div>
                </div>
            `;

            // 3. Sections Logic
            const sections = document.querySelectorAll('.form-section');
            let sectionHtml = '';
            
            sections.forEach(sec => {
                const header = sec.querySelector('h3').innerText;
                const rows = sec.querySelectorAll('.form-row');
                let hasContent = false;
                let rowsHtml = '';
                
                rows.forEach(row => {
                    // Checkboxes/Radios
                    const check = row.querySelector('input[type="checkbox"], input[type="radio"]');
                    if (check && check.checked) {
                        const label = row.querySelector('label').innerText.trim();
                        const priceEl = row.querySelector('.price-tag');
                        const price = priceEl ? priceEl.innerText : '';
                        // Don't show price for "Sin Blueprint" or 0 items if we want clean look, but let's show all checked.
                        rowsHtml += `<div class="prop-item"><span class="item-name">▪ ${label}</span> <span class="item-price">${price}</span></div>`;
                        hasContent = true;
                    }
                    
                    // Qty Inputs (that are not checkboxes)
                    const qtyInput = row.querySelector('input[type="number"]');
                    if (qtyInput && qtyInput.value > 0) {
                        const label = row.querySelector('label').innerText.trim();
                        const priceEl = row.querySelector('.price-tag'); // Usually not on the row for qty, but let's check
                        // If price is data-price, calculate? Or just show unit price?
                        // The UI shows price in label sometimes or not.
                        // Let's just show the label and quantity.
                        rowsHtml += `<div class="prop-item"><span class="item-name">▪ ${label} (x${qtyInput.value})</span> <span class="item-price"></span></div>`;
                        hasContent = true;
                    }
                    
                    // Text Inputs / Textareas (Data & Objectives)
                    const textInput = row.querySelector('input[type="text"], textarea, input[type="date"]');
                    // Exclude the project name inputs we already used in header if we want, but they are in section A.
                    if (textInput && textInput.value.trim() !== '' && !textInput.placeholder.includes('Portal Clientes')) {
                        const label = row.querySelector('label').innerText.trim();
                        rowsHtml += `<div class="prop-text-block"><strong>${label}:</strong><br>${textInput.value}</div>`;
                        hasContent = true;
                    }
                    
                    // Selects
                    const select = row.querySelector('select');
                    if (select && select.value != '0' && select.value != '1') { 
                         const label = row.querySelector('label').innerText.trim();
                         const selectedText = select.options[select.selectedIndex].text;
                         rowsHtml += `<div class="prop-item"><span class="item-name">▪ ${label}: ${selectedText}</span></div>`;
                         hasContent = true;
                    }
                });
                
                if (hasContent) {
                    sectionHtml += `
                        <div class="prop-section">
                            <h3>${header}</h3>
                            <div class="prop-content">${rowsHtml}</div>
                        </div>
                    `;
                }
            });
            
            html += sectionHtml;

            // 4. Budget Summary
            const total = document.getElementById('totalAmount').innerText;
            const monthly = document.getElementById('monthlyAmount').innerText;
            
            html += `
                <div class="prop-financials">
                    <h3>RESUMEN ECONÓMICO</h3>
                    <div class="financial-row main-total">
                        <span>INVERSIÓN TOTAL (Pago Único)</span>
                        <span>${total}</span>
                    </div>
                    <div class="financial-row">
                        <span>Soporte Recurrente</span>
                        <span>${monthly}</span>
                    </div>
                    <div class="financial-note">
                        * Precios sin IVA. Validez de la oferta: 15 días.
                    </div>
                </div>
                
                <div class="prop-footer">
                    Integra Tech Consulting — Confidencial
                </div>
            `;

            proposalContainer.innerHTML = html;
            
            // Append to body to render (hidden)
            document.body.appendChild(proposalContainer);

            // PDF Options
            const opt = {
                margin:       [15, 15, 15, 15],
                filename:     `Propuesta_${(projectName || 'Proyecto').replace(/\s+/g, '_')}.pdf`,
                image:        { type: 'jpeg', quality: 0.98 },
                html2canvas:  { scale: 2, useCORS: true },
                jsPDF:        { unit: 'mm', format: 'a4', orientation: 'portrait' }
            };

            // Generate
            if (typeof html2pdf !== 'undefined') {
                html2pdf().set(opt).from(proposalContainer).save().then(() => {
                    document.body.removeChild(proposalContainer);
                }).catch(err => {
                    console.error(err);
                    alert('Error al generar PDF.');
                    if(document.body.contains(proposalContainer)) document.body.removeChild(proposalContainer);
                });
            } else {
                alert('Librería PDF no cargada.');
            }
        });
    }
});
