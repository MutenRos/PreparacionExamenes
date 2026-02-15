/**
 * OmniERP POS Widget - Embeddable shopping cart widget
 * Usage: <script src="https://omnierp.com/static/widget-pos.js" data-token="YOUR_TOKEN"></script>
 */

(function() {
    'use strict';

    // Get token from script tag
    const script = document.currentScript || document.scripts[document.scripts.length - 1];
    const token = script.getAttribute('data-token');
    
    if (!token) {
        console.error('OmniERP Widget: data-token attribute is required');
        return;
    }

    const API_BASE = 'https://omnierp.com/api/pos/public/widget';
    const WIDGET_ID = 'omnierp-pos-widget';
    const CART_STORAGE_KEY = `omnierp_cart_${token}`;
    
    let cart = [];
    let productos = [];
    let config = {
        color_primario: '#2563eb',
        color_boton: '#10b981',
        icono_carrito: true,
        mostrar_precio: true,
        mostrar_stock: true,
    };

    // Load config
    async function loadConfig() {
        try {
            const response = await fetch(`${API_BASE}/${token}/productos`, {
                headers: {
                    'Origin': window.location.origin,
                }
            });
            
            if (!response.ok) throw new Error('Widget not found or disabled');
            
            productos = await response.json();
            renderWidget();
        } catch (error) {
            console.error('OmniERP Widget Error:', error);
            renderError(error.message);
        }
    }

    // Render widget HTML
    function renderWidget() {
        const container = document.getElementById(WIDGET_ID);
        if (!container) {
            console.error('OmniERP Widget: Container with id="' + WIDGET_ID + '" not found');
            return;
        }

        const styles = `
            <style>
                .omnierp-widget {
                    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
                    max-width: 100%;
                }

                .omnierp-widget * {
                    box-sizing: border-box;
                }

                .omnierp-widget-header {
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                    padding: 1rem;
                    background-color: ${config.color_primario};
                    color: white;
                    border-radius: 8px 8px 0 0;
                }

                .omnierp-widget-title {
                    font-size: 1.125rem;
                    font-weight: 600;
                }

                .omnierp-cart-count {
                    display: inline-block;
                    min-width: 24px;
                    height: 24px;
                    background-color: ${config.color_boton};
                    color: white;
                    border-radius: 50%;
                    text-align: center;
                    line-height: 24px;
                    font-size: 0.75rem;
                    font-weight: 700;
                    margin-left: 0.5rem;
                }

                .omnierp-productos-grid {
                    display: grid;
                    grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
                    gap: 1rem;
                    padding: 1rem;
                    background-color: #f9fafb;
                }

                .omnierp-producto-card {
                    background: white;
                    border: 1px solid #e5e7eb;
                    border-radius: 8px;
                    padding: 1rem;
                    transition: all 0.2s ease;
                    cursor: pointer;
                }

                .omnierp-producto-card:hover {
                    box-shadow: 0 4px 12px rgba(37, 99, 235, 0.15);
                    border-color: ${config.color_primario};
                }

                .omnierp-producto-nombre {
                    font-weight: 600;
                    color: #1f2937;
                    margin-bottom: 0.5rem;
                    font-size: 0.95rem;
                }

                .omnierp-producto-precio {
                    font-size: 1.25rem;
                    font-weight: 700;
                    color: ${config.color_boton};
                    margin-bottom: 0.5rem;
                }

                .omnierp-producto-stock {
                    font-size: 0.75rem;
                    color: #6b7280;
                    margin-bottom: 0.75rem;
                }

                .omnierp-producto-stock.bajo {
                    color: #ef4444;
                    font-weight: 600;
                }

                .omnierp-btn-agregar {
                    width: 100%;
                    padding: 0.5rem;
                    background-color: ${config.color_boton};
                    color: white;
                    border: none;
                    border-radius: 6px;
                    font-weight: 600;
                    cursor: pointer;
                    transition: all 0.2s ease;
                    font-size: 0.875rem;
                }

                .omnierp-btn-agregar:hover {
                    opacity: 0.9;
                    transform: translateY(-2px);
                }

                .omnierp-btn-agregar:disabled {
                    background-color: #d1d5db;
                    cursor: not-allowed;
                    transform: none;
                }

                .omnierp-cart-modal {
                    display: none;
                    position: fixed;
                    top: 0;
                    left: 0;
                    right: 0;
                    bottom: 0;
                    background-color: rgba(0, 0, 0, 0.5);
                    z-index: 10000;
                    justify-content: center;
                    align-items: center;
                }

                .omnierp-cart-modal.active {
                    display: flex;
                }

                .omnierp-cart-content {
                    background: white;
                    border-radius: 12px;
                    padding: 2rem;
                    max-width: 600px;
                    width: 90%;
                    max-height: 90vh;
                    overflow-y: auto;
                }

                .omnierp-cart-header {
                    font-size: 1.5rem;
                    font-weight: 700;
                    color: #1f2937;
                    margin-bottom: 1.5rem;
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                }

                .omnierp-close-btn {
                    background: none;
                    border: none;
                    font-size: 1.5rem;
                    cursor: pointer;
                    color: #6b7280;
                }

                .omnierp-cart-items {
                    margin-bottom: 1.5rem;
                }

                .omnierp-cart-item {
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                    padding: 1rem;
                    border-bottom: 1px solid #e5e7eb;
                }

                .omnierp-cart-item-info {
                    flex: 1;
                }

                .omnierp-cart-item-nombre {
                    font-weight: 600;
                    color: #1f2937;
                }

                .omnierp-cart-item-subtotal {
                    color: ${config.color_boton};
                    font-weight: 600;
                    margin-right: 1rem;
                }

                .omnierp-cart-item-cantidad {
                    display: flex;
                    gap: 0.5rem;
                    align-items: center;
                }

                .omnierp-cart-item-cantidad button {
                    width: 24px;
                    height: 24px;
                    border: 1px solid #d1d5db;
                    background: white;
                    border-radius: 4px;
                    cursor: pointer;
                    font-weight: 600;
                    font-size: 0.875rem;
                }

                .omnierp-cart-item-cantidad button:hover {
                    background-color: #f3f4f6;
                }

                .omnierp-cart-summary {
                    background-color: #f9fafb;
                    padding: 1rem;
                    border-radius: 6px;
                    margin-bottom: 1.5rem;
                }

                .omnierp-cart-summary-row {
                    display: flex;
                    justify-content: space-between;
                    margin-bottom: 0.75rem;
                    font-size: 0.875rem;
                }

                .omnierp-cart-summary-row.total {
                    font-size: 1.125rem;
                    font-weight: 700;
                    color: ${config.color_boton};
                    border-top: 2px solid #e5e7eb;
                    padding-top: 0.75rem;
                    margin-top: 0.75rem;
                }

                .omnierp-cart-actions {
                    display: flex;
                    gap: 1rem;
                }

                .omnierp-btn-checkout {
                    flex: 1;
                    padding: 0.75rem;
                    background-color: ${config.color_boton};
                    color: white;
                    border: none;
                    border-radius: 6px;
                    font-weight: 600;
                    cursor: pointer;
                    transition: all 0.2s ease;
                }

                .omnierp-btn-checkout:hover {
                    opacity: 0.9;
                }

                .omnierp-btn-volver {
                    flex: 1;
                    padding: 0.75rem;
                    background-color: #e5e7eb;
                    color: #374151;
                    border: none;
                    border-radius: 6px;
                    font-weight: 600;
                    cursor: pointer;
                }

                .omnierp-btn-volver:hover {
                    background-color: #d1d5db;
                }

                .omnierp-empty-cart {
                    text-align: center;
                    padding: 2rem 1rem;
                    color: #6b7280;
                }

                .omnierp-empty-cart-icon {
                    font-size: 2rem;
                    margin-bottom: 1rem;
                }

                .omnierp-empty-cart-text {
                    font-size: 0.875rem;
                }

                .omnierp-alert {
                    padding: 0.75rem;
                    border-radius: 6px;
                    margin-bottom: 1rem;
                    font-size: 0.875rem;
                }

                .omnierp-alert-success {
                    background-color: #d1fae5;
                    color: #065f46;
                    border: 1px solid #a7f3d0;
                }

                .omnierp-alert-error {
                    background-color: #fee2e2;
                    color: #7f1d1d;
                    border: 1px solid #fecaca;
                }
            </style>
        `;

        const html = `
            <div class="omnierp-widget">
                <div class="omnierp-widget-header">
                    <div class="omnierp-widget-title">⚡ Tienda</div>
                    <button onclick="omnierp_openCart()" style="background: none; border: none; color: white; cursor: pointer; font-size: 1.25rem; display: flex; align-items: center;">
                        🛒
                        <span class="omnierp-cart-count" id="omnierp-cart-badge">0</span>
                    </button>
                </div>

                <div id="omnierp-alert" style="display: none;"></div>

                <div class="omnierp-productos-grid" id="omnierp-productos">
                    <!-- Productos se cargarán aquí -->
                </div>
            </div>

            <!-- Cart Modal -->
            <div class="omnierp-cart-modal" id="omnierp-cart-modal">
                <div class="omnierp-cart-content">
                    <div class="omnierp-cart-header">
                        <span>Mi Carrito</span>
                        <button class="omnierp-close-btn" onclick="omnierp_closeCart()">✕</button>
                    </div>

                    <div id="omnierp-cart-items"></div>

                    <div id="omnierp-cart-summary" style="display: none;"></div>

                    <div class="omnierp-cart-actions" id="omnierp-cart-actions" style="display: none;">
                        <button class="omnierp-btn-checkout" onclick="omnierp_checkout()">Comprar Ahora</button>
                        <button class="omnierp-btn-volver" onclick="omnierp_closeCart()">Volver</button>
                    </div>

                    <div id="omnierp-empty-cart" class="omnierp-empty-cart" style="display: none;">
                        <div class="omnierp-empty-cart-icon">🛒</div>
                        <div class="omnierp-empty-cart-text">Tu carrito está vacío</div>
                    </div>
                </div>
            </div>
        `;

        container.innerHTML = styles + html;
        renderProductos();
    }

    // Render productos
    function renderProductos() {
        const container = document.getElementById('omnierp-productos');
        if (!container) return;

        container.innerHTML = productos.map(p => `
            <div class="omnierp-producto-card">
                <div class="omnierp-producto-nombre">${p.nombre}</div>
                ${config.mostrar_precio ? `<div class="omnierp-producto-precio">$${p.precio_venta.toFixed(2)}</div>` : ''}
                ${config.mostrar_stock ? `<div class="omnierp-producto-stock ${p.stock_actual <= 5 ? 'bajo' : ''}">Stock: ${p.stock_actual}</div>` : ''}
                <button class="omnierp-btn-agregar" onclick="omnierp_addToCart(${p.id}, '${p.nombre.replace(/'/g, "\\'")}', ${p.precio_venta})" ${p.stock_actual === 0 ? 'disabled' : ''}>
                    ${p.stock_actual === 0 ? 'Agotado' : 'Agregar'}
                </button>
            </div>
        `).join('');
    }

    // Add to cart
    window.omnierp_addToCart = function(productoId, nombre, precio) {
        const existente = cart.find(i => i.producto_id === productoId);
        
        if (existente) {
            existente.cantidad++;
        } else {
            cart.push({
                producto_id: productoId,
                nombre,
                precio_unitario: precio,
                cantidad: 1,
                descuento: 0,
            });
        }

        saveCart();
        updateCartBadge();
        showAlert(`${nombre} agregado al carrito`, 'success');
    };

    // Remove from cart
    window.omnierp_removeFromCart = function(productoId) {
        cart = cart.filter(i => i.producto_id !== productoId);
        saveCart();
        updateCartBadge();
        renderCart();
    };

    // Update quantity
    window.omnierp_updateQuantity = function(productoId, cantidad) {
        const item = cart.find(i => i.producto_id === productoId);
        if (item) {
            item.cantidad = Math.max(1, cantidad);
            saveCart();
            updateCartBadge();
            renderCart();
        }
    };

    // Open cart
    window.omnierp_openCart = function() {
        document.getElementById('omnierp-cart-modal').classList.add('active');
        renderCart();
    };

    // Close cart
    window.omnierp_closeCart = function() {
        document.getElementById('omnierp-cart-modal').classList.remove('active');
    };

    // Render cart
    function renderCart() {
        const modal = document.getElementById('omnierp-cart-modal');
        
        if (cart.length === 0) {
            modal.querySelector('#omnierp-cart-items').innerHTML = '';
            modal.querySelector('#omnierp-cart-summary').style.display = 'none';
            modal.querySelector('#omnierp-cart-actions').style.display = 'none';
            modal.querySelector('#omnierp-empty-cart').style.display = 'block';
            return;
        }

        modal.querySelector('#omnierp-empty-cart').style.display = 'none';
        modal.querySelector('#omnierp-cart-summary').style.display = 'block';
        modal.querySelector('#omnierp-cart-actions').style.display = 'flex';

        // Render items
        const itemsHtml = cart.map(item => {
            const subtotal = item.cantidad * item.precio_unitario;
            return `
                <div class="omnierp-cart-item">
                    <div class="omnierp-cart-item-info">
                        <div class="omnierp-cart-item-nombre">${item.nombre}</div>
                        <div style="font-size: 0.75rem; color: #6b7280;">$${item.precio_unitario.toFixed(2)} c/u</div>
                    </div>
                    <div class="omnierp-cart-item-cantidad">
                        <button onclick="omnierp_updateQuantity(${item.producto_id}, ${item.cantidad - 1})">−</button>
                        <span style="width: 30px; text-align: center;">${item.cantidad}</span>
                        <button onclick="omnierp_updateQuantity(${item.producto_id}, ${item.cantidad + 1})">+</button>
                    </div>
                    <div class="omnierp-cart-item-subtotal">$${subtotal.toFixed(2)}</div>
                    <button onclick="omnierp_removeFromCart(${item.producto_id})" style="background: none; border: none; color: #ef4444; cursor: pointer; font-size: 1.25rem;">✕</button>
                </div>
            `;
        }).join('');

        modal.querySelector('#omnierp-cart-items').innerHTML = itemsHtml;

        // Calculate totals
        const subtotal = cart.reduce((sum, i) => sum + (i.cantidad * i.precio_unitario), 0);
        const impuesto = subtotal * 0.18;
        const total = subtotal + impuesto;

        const summaryHtml = `
            <div class="omnierp-cart-summary">
                <div class="omnierp-cart-summary-row">
                    <span>Subtotal:</span>
                    <span>$${subtotal.toFixed(2)}</span>
                </div>
                <div class="omnierp-cart-summary-row">
                    <span>Impuesto (18%):</span>
                    <span>$${impuesto.toFixed(2)}</span>
                </div>
                <div class="omnierp-cart-summary-row total">
                    <span>Total:</span>
                    <span>$${total.toFixed(2)}</span>
                </div>
            </div>
        `;

        modal.querySelector('#omnierp-cart-summary').innerHTML = summaryHtml;
    }

    // Checkout
    window.omnierp_checkout = async function() {
        if (cart.length === 0) return;

        try {
            const response = await fetch(`${API_BASE}/${token}/compra`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Origin': window.location.origin,
                },
                body: JSON.stringify({
                    detalles: cart,
                    metodo_pago: 'online',
                }),
            });

            if (!response.ok) throw new Error('Error en la compra');

            const result = await response.json();
            cart = [];
            saveCart();
            updateCartBadge();

            showAlert(`¡Compra exitosa! Número: ${result.numero}`, 'success');
            document.getElementById('omnierp-cart-modal').classList.remove('active');
            renderProductos();
        } catch (error) {
            showAlert('Error: ' + error.message, 'error');
        }
    };

    // Utilities
    function saveCart() {
        localStorage.setItem(CART_STORAGE_KEY, JSON.stringify(cart));
    }

    function loadCart() {
        const saved = localStorage.getItem(CART_STORAGE_KEY);
        if (saved) {
            try {
                cart = JSON.parse(saved);
            } catch (e) {
                cart = [];
            }
        }
    }

    function updateCartBadge() {
        const badge = document.getElementById('omnierp-cart-badge');
        if (badge) {
            const count = cart.reduce((sum, i) => sum + i.cantidad, 0);
            badge.textContent = count;
        }
    }

    function showAlert(message, type) {
        const container = document.getElementById('omnierp-alert');
        if (!container) return;

        const alert = document.createElement('div');
        alert.className = `omnierp-alert omnierp-alert-${type}`;
        alert.textContent = message;
        container.innerHTML = '';
        container.appendChild(alert);
        container.style.display = 'block';

        setTimeout(() => {
            container.style.display = 'none';
        }, 4000);
    }

    function renderError(message) {
        const container = document.getElementById(WIDGET_ID);
        if (container) {
            container.innerHTML = `
                <div style="padding: 2rem; text-align: center; color: #ef4444;">
                    <div style="font-size: 2rem; margin-bottom: 1rem;">⚠️</div>
                    <div style="font-weight: 600; margin-bottom: 0.5rem;">Widget no disponible</div>
                    <div style="font-size: 0.875rem;">${message}</div>
                </div>
            `;
        }
    }

    // Initialize
    loadCart();
    loadConfig();
})();
