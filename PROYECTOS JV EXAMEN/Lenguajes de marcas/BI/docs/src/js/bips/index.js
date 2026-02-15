/**
 * =============================================================================
 * BOMBAS IDEAL - BIPS Main Module
 * =============================================================================
 * 
 * @description  Punto de entrada del sistema BIPS (Bombas Ideal Product Selector).
 *               Exporta todas las funcionalidades del selector de productos.
 * 
 * @author       Bombas Ideal Development Team
 * @version      4.1.0
 * @module       bips
 * 
 * USO:
 * import BIPS from './bips/index.js';
 * BIPS.init(); // Inicializa la UI
 * BIPS.search({ flow: 10, head: 50 }); // Busca programáticamente
 */

// Importar módulos
import * as Data from './data.js';
import * as Filter from './filter.js';
import * as UI from './ui.js';

/**
 * Inicializa el sistema BIPS
 */
export function init() {
    UI.init();
    
    console.log(`
    ╔═══════════════════════════════════════════════╗
    ║  🔵 BIPS - Bombas Ideal Product Selector 🔵   ║
    ║                                               ║
    ║  Sistema de selección de bombas v4.1.0        ║
    ║  ${Data.SERIES_DATABASE.length} series disponibles                        ║
    ╚═══════════════════════════════════════════════╝
    `);
}

// Re-exportar módulos
export { Data, Filter, UI };

// Exportar funciones comunes directamente
export const {
    SERIES_DATABASE,
    SECTORS,
    INSTALLATION_TYPES,
    MATERIALS,
    getSeriesById,
    getSeriesBySector,
} = Data;

export const {
    filterSeries,
    getSuggestionsBySector,
    getPopularSeries,
    validateParams,
} = Filter;

export const {
    search,
    setView,
    getResults,
} = UI;

// Export default
export default {
    init,
    // Data
    SERIES_DATABASE: Data.SERIES_DATABASE,
    SECTORS: Data.SECTORS,
    getSeriesById: Data.getSeriesById,
    getSeriesBySector: Data.getSeriesBySector,
    // Filter
    filterSeries: Filter.filterSeries,
    getSuggestionsBySector: Filter.getSuggestionsBySector,
    getPopularSeries: Filter.getPopularSeries,
    validateParams: Filter.validateParams,
    // UI
    search: UI.search,
    setView: UI.setView,
    getResults: UI.getResults,
};
