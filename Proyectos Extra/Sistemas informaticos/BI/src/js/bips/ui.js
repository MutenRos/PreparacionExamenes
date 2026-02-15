/**
 * =============================================================================
 * BOMBAS IDEAL - BIPS UI Module
 * =============================================================================
 * 
 * @description  Interfaz de usuario del selector de bombas BIPS.
 *               Maneja la interacción con el formulario, renderizado de
 *               resultados y estados de la UI.
 * 
 * @author       Bombas Ideal Development Team
 * @version      4.1.0
 * @module       bips/ui
 */

import { $, $$, addClass, removeClass, hasClass } from '../modules/utils.js';
import { filterSeries, validateParams, getPopularSeries, DEFAULT_PARAMS } from './filter.js';
import { SECTORS, INSTALLATION_TYPES, MATERIALS } from './data.js';

/* =========================================================================
 * STATE
 * ========================================================================= */

/** @type {Object} Estado interno */
const state = {
    currentView: 'grid', // 'grid' o 'list'
    currentResults: [],
    isLoading: false,
    lastParams: null,
};

/** @type {Object} Referencias a elementos del DOM */
let elements = {};


/* =========================================================================
 * DOM REFERENCES
 * ========================================================================= */

/**
 * Cachea las referencias a elementos del DOM
 */
function cacheElements() {
    elements = {
        form: $('#bips-form'),
        flowInput: $('#bips-flow'),
        headInput: $('#bips-head'),
        sectorSelect: $('#bips-sector'),
        installationSelect: $('#bips-installation'),
        phaseSelect: $('#bips-phase'),
        searchBtn: $('#bips-search-btn'),
        resetBtn: $('#bips-reset-btn'),
        resultsContainer: $('#bips-results'),
        resultsCount: $('#bips-results-count'),
        viewButtons: $$('.bips-view-btn'),
    };
}


/* =========================================================================
 * RENDERING
 * ========================================================================= */

/**
 * Renderiza el estado de carga
 */
function renderLoading() {
    if (!elements.resultsContainer) return;
    
    elements.resultsContainer.innerHTML = `
        <div class="bips-loading">
            <div class="bips-loading-spinner"></div>
            <p class="bips-loading-text">Buscando productos...</p>
        </div>
    `;
}

/**
 * Renderiza el estado vacío (sin resultados)
 */
function renderEmpty() {
    if (!elements.resultsContainer) return;
    
    elements.resultsContainer.innerHTML = `
        <div class="bips-empty">
            <div class="bips-empty-icon">🔍</div>
            <h3 class="bips-empty-title">Sin resultados</h3>
            <p class="bips-empty-text">
                No hemos encontrado bombas que coincidan con tus parámetros.
                Prueba a ajustar el caudal o la altura.
            </p>
        </div>
    `;
}

/**
 * Renderiza el estado inicial
 */
function renderInitial() {
    if (!elements.resultsContainer) return;
    
    // Mostrar series populares
    const popular = getPopularSeries(6);
    
    elements.resultsContainer.innerHTML = `
        <div class="bips-initial">
            <div class="bips-initial-icon">
                <i class="fas fa-tint"></i>
            </div>
            <h3 class="bips-initial-title">Encuentra tu bomba ideal</h3>
            <p class="bips-initial-text">
                Introduce los parámetros de tu instalación para encontrar
                la serie de bombas más adecuada.
            </p>
        </div>
        
        <div class="section--sm">
            <h4 class="text-center mb-6">Series destacadas</h4>
            <div class="bips-products-grid">
                ${popular.map(series => renderProductCard(series, false)).join('')}
            </div>
        </div>
    `;
}

/**
 * Renderiza una tarjeta de producto
 * @param {Object} series - Datos de la serie
 * @param {boolean} showScore - Mostrar score de coincidencia
 * @returns {string} HTML
 */
function renderProductCard(series, showScore = true) {
    const sectors = series.sectors
        .slice(0, 3)
        .map(s => SECTORS[s])
        .filter(Boolean)
        .map(s => `<span><i class="${s.icon}"></i> ${s.name}</span>`)
        .join('');
    
    const matchBadge = showScore && series.matchScore
        ? `<span class="bips-match-badge ${series.matchScore < 70 ? 'bips-match-badge--partial' : ''}">${series.matchScore}%</span>`
        : '';
    
    return `
        <div class="bips-product-card">
            ${matchBadge}
            <div class="bips-product-image">
                <img src="${series.image}" alt="${series.name}" 
                     onerror="this.src='assets/images/placeholder-pump.jpg'">
            </div>
            <div class="bips-product-info">
                <span class="bips-product-series">${series.type}</span>
                <h3 class="bips-product-name">${series.name}</h3>
                <p class="card-text text-sm">${series.description.slice(0, 100)}...</p>
                
                <div class="bips-product-specs">
                    <div class="bips-spec">
                        <span>Caudal</span>
                        <strong>${series.flow.min}-${series.flow.max} m³/h</strong>
                    </div>
                    <div class="bips-spec">
                        <span>Altura</span>
                        <strong>${series.head.min}-${series.head.max} m</strong>
                    </div>
                    <div class="bips-spec">
                        <span>Potencia</span>
                        <strong>${series.power.min}-${series.power.max} kW</strong>
                    </div>
                    <div class="bips-spec">
                        <span>Eficiencia</span>
                        <strong>${series.efficiency}%</strong>
                    </div>
                </div>
                
                <div class="card-applications">
                    ${sectors}
                </div>
                
                <div class="bips-product-actions mt-4">
                    <a href="${series.productPage}" class="btn btn-primary btn-sm">
                        Ver detalles
                    </a>
                    <a href="assets/docs/${series.catalog}" 
                       class="btn btn-outline btn-sm" 
                       target="_blank">
                        <i class="fas fa-file-pdf"></i>
                    </a>
                </div>
            </div>
        </div>
    `;
}

/**
 * Renderiza una fila de tabla
 * @param {Object} series - Datos de la serie
 * @returns {string} HTML
 */
function renderTableRow(series) {
    return `
        <tr>
            <td>
                <div class="bips-table-product">
                    <div class="bips-table-thumb">
                        <img src="${series.image}" alt="${series.name}"
                             onerror="this.src='assets/images/placeholder-pump.jpg'">
                    </div>
                    <div>
                        <strong>${series.name}</strong>
                        <small class="d-block text-muted">${series.type}</small>
                    </div>
                </div>
            </td>
            <td>${series.flow.min}-${series.flow.max}</td>
            <td>${series.head.min}-${series.head.max}</td>
            <td>${series.power.min}-${series.power.max}</td>
            <td>${series.efficiency}%</td>
            <td>
                <span class="bips-match-badge ${series.matchScore < 70 ? 'bips-match-badge--partial' : ''}">
                    ${series.matchScore}%
                </span>
            </td>
            <td>
                <a href="${series.productPage}" class="btn btn-primary btn-sm">Ver</a>
            </td>
        </tr>
    `;
}

/**
 * Renderiza los resultados en vista grid
 * @param {Array} results - Array de resultados
 */
function renderGridView(results) {
    if (!elements.resultsContainer) return;
    
    elements.resultsContainer.innerHTML = `
        <div class="bips-products-grid">
            ${results.map(series => renderProductCard(series)).join('')}
        </div>
    `;
}

/**
 * Renderiza los resultados en vista lista/tabla
 * @param {Array} results - Array de resultados
 */
function renderListView(results) {
    if (!elements.resultsContainer) return;
    
    elements.resultsContainer.innerHTML = `
        <div class="bips-table-wrapper">
            <table class="bips-table">
                <thead>
                    <tr>
                        <th>Serie</th>
                        <th>Caudal (m³/h)</th>
                        <th>Altura (m)</th>
                        <th>Potencia (kW)</th>
                        <th>Eficiencia</th>
                        <th>Match</th>
                        <th>Acción</th>
                    </tr>
                </thead>
                <tbody>
                    ${results.map(series => renderTableRow(series)).join('')}
                </tbody>
            </table>
        </div>
    `;
}

/**
 * Renderiza los resultados según la vista actual
 * @param {Array} results - Array de resultados
 */
function renderResults(results) {
    // Actualizar contador
    if (elements.resultsCount) {
        elements.resultsCount.innerHTML = `
            <strong>${results.length}</strong> serie${results.length !== 1 ? 's' : ''} encontrada${results.length !== 1 ? 's' : ''}
        `;
    }
    
    if (results.length === 0) {
        renderEmpty();
        return;
    }
    
    if (state.currentView === 'grid') {
        renderGridView(results);
    } else {
        renderListView(results);
    }
}


/* =========================================================================
 * EVENT HANDLERS
 * ========================================================================= */

/**
 * Obtiene los parámetros del formulario
 * @returns {Object}
 */
function getFormParams() {
    return {
        flow: elements.flowInput?.value ? parseFloat(elements.flowInput.value) : null,
        head: elements.headInput?.value ? parseFloat(elements.headInput.value) : null,
        sector: elements.sectorSelect?.value || null,
        installation: elements.installationSelect?.value || null,
        phase: elements.phaseSelect?.value || null,
    };
}

/**
 * Maneja la búsqueda
 * @param {Event} [event]
 */
function handleSearch(event) {
    if (event) event.preventDefault();
    
    const params = getFormParams();
    
    // Validar
    const validation = validateParams(params);
    if (!validation.valid) {
        alert(validation.errors.join('\n'));
        return;
    }
    
    // Mostrar loading
    state.isLoading = true;
    renderLoading();
    
    // Simular pequeño delay para UX
    setTimeout(() => {
        const result = filterSeries(params);
        
        state.isLoading = false;
        state.currentResults = result.matches;
        state.lastParams = params;
        
        renderResults(result.matches);
    }, 300);
}

/**
 * Maneja el reset del formulario
 */
function handleReset() {
    if (elements.form) {
        elements.form.reset();
    }
    
    state.currentResults = [];
    state.lastParams = null;
    
    renderInitial();
}

/**
 * Maneja el cambio de vista
 * @param {string} view - 'grid' o 'list'
 */
function handleViewChange(view) {
    state.currentView = view;
    
    // Actualizar botones
    elements.viewButtons.forEach(btn => {
        removeClass(btn, 'active');
        if (btn.dataset.view === view) {
            addClass(btn, 'active');
        }
    });
    
    // Re-renderizar si hay resultados
    if (state.currentResults.length > 0) {
        renderResults(state.currentResults);
    }
}


/* =========================================================================
 * PUBLIC API
 * ========================================================================= */

/**
 * Inicializa la UI de BIPS
 */
export function init() {
    cacheElements();
    
    // Verificar elementos necesarios
    if (!elements.resultsContainer) {
        console.warn('BIPS UI: Results container not found');
        return;
    }
    
    // Event listeners
    if (elements.form) {
        elements.form.addEventListener('submit', handleSearch);
    }
    
    if (elements.searchBtn) {
        elements.searchBtn.addEventListener('click', handleSearch);
    }
    
    if (elements.resetBtn) {
        elements.resetBtn.addEventListener('click', handleReset);
    }
    
    elements.viewButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            handleViewChange(btn.dataset.view);
        });
    });
    
    // Estado inicial
    renderInitial();
    
    console.log('BIPS UI initialized');
}

/**
 * Ejecuta una búsqueda con parámetros dados
 * @param {Object} params - Parámetros de búsqueda
 */
export function search(params) {
    // Rellenar formulario
    if (params.flow && elements.flowInput) {
        elements.flowInput.value = params.flow;
    }
    if (params.head && elements.headInput) {
        elements.headInput.value = params.head;
    }
    if (params.sector && elements.sectorSelect) {
        elements.sectorSelect.value = params.sector;
    }
    
    // Ejecutar búsqueda
    handleSearch();
}

/**
 * Cambia la vista actual
 * @param {'grid'|'list'} view
 */
export function setView(view) {
    handleViewChange(view);
}

/**
 * Obtiene los resultados actuales
 * @returns {Array}
 */
export function getResults() {
    return state.currentResults;
}

export default {
    init,
    search,
    setView,
    getResults,
};
