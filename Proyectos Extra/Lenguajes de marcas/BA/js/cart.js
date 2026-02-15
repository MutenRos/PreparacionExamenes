/**
 * Sistema de Carrito de Compras - Bombas Bloch
 * Con soporte para pagos simulados (modo demo)
 */

class ShoppingCart {
    constructor() {
        this.items = JSON.parse(localStorage.getItem('ba_cart')) || [];
        this.isDemo = true; // MODO DEMO - Pagos simulados
        this.init();
    }

    init() {
        this.updateCartUI();
        this.bindEvents();
    }

    // Guardar carrito en localStorage
    save() {
        localStorage.setItem('ba_cart', JSON.stringify(this.items));
        this.updateCartUI();
    }

    // Añadir producto al carrito
    addItem(product) {
        const existingItem = this.items.find(item => item.id === product.id);
        
        if (existingItem) {
            existingItem.quantity += product.quantity || 1;
        } else {
            this.items.push({
                id: product.id,
                name: product.name,
                price: product.price,
                image: product.image || 'images/producto-default.jpg',
                quantity: product.quantity || 1
            });
        }
        
        this.save();
        this.showNotification(`${product.name} añadido al carrito`);
    }

    // Eliminar producto del carrito
    removeItem(productId) {
        this.items = this.items.filter(item => item.id !== productId);
        this.save();
    }

    // Actualizar cantidad
    updateQuantity(productId, quantity) {
        const item = this.items.find(item => item.id === productId);
        if (item) {
            item.quantity = Math.max(1, quantity);
            this.save();
        }
    }

    // Vaciar carrito
    clear() {
        this.items = [];
        this.save();
    }

    // Obtener total
    getTotal() {
        return this.items.reduce((total, item) => total + (item.price * item.quantity), 0);
    }

    // Obtener cantidad total de items
    getItemCount() {
        return this.items.reduce((count, item) => count + item.quantity, 0);
    }

    // Actualizar UI del carrito (icono en header)
    updateCartUI() {
        const cartCount = document.getElementById('cart-count');
        const cartTotal = document.getElementById('cart-total');
        
        if (cartCount) {
            const count = this.getItemCount();
            cartCount.textContent = count;
            cartCount.style.display = count > 0 ? 'flex' : 'none';
        }
        
        if (cartTotal) {
            cartTotal.textContent = this.getTotal().toFixed(2) + ' €';
        }

        // Actualizar mini-carrito si existe
        this.updateMiniCart();
    }

    // Mini carrito desplegable
    updateMiniCart() {
        const miniCart = document.getElementById('mini-cart-items');
        if (!miniCart) return;

        if (this.items.length === 0) {
            miniCart.innerHTML = '<p class="empty-cart">Tu carrito está vacío</p>';
            return;
        }

        miniCart.innerHTML = this.items.map(item => `
            <div class="mini-cart-item" data-id="${item.id}">
                <img src="${item.image}" alt="${item.name}">
                <div class="mini-cart-item-info">
                    <h4>${item.name}</h4>
                    <p>${item.quantity} x ${item.price.toFixed(2)} €</p>
                </div>
                <button class="remove-item" onclick="cart.removeItem('${item.id}')">
                    <i class="fas fa-times"></i>
                </button>
            </div>
        `).join('');
    }

    // Mostrar notificación
    showNotification(message) {
        // Eliminar notificación anterior si existe
        const existingNotif = document.querySelector('.cart-notification');
        if (existingNotif) existingNotif.remove();

        const notification = document.createElement('div');
        notification.className = 'cart-notification';
        notification.innerHTML = `
            <i class="fas fa-check-circle"></i>
            <span>${message}</span>
        `;
        document.body.appendChild(notification);

        setTimeout(() => notification.classList.add('show'), 10);
        setTimeout(() => {
            notification.classList.remove('show');
            setTimeout(() => notification.remove(), 300);
        }, 3000);
    }

    // Bind eventos globales
    bindEvents() {
        // Delegación de eventos para botones añadir al carrito
        document.addEventListener('click', (e) => {
            if (e.target.closest('.add-to-cart')) {
                e.preventDefault();
                const btn = e.target.closest('.add-to-cart');
                const product = {
                    id: btn.dataset.id,
                    name: btn.dataset.name,
                    price: parseFloat(btn.dataset.price),
                    image: btn.dataset.image
                };
                this.addItem(product);
            }
        });
    }

    // Renderizar página de carrito completo
    renderFullCart() {
        const cartContainer = document.getElementById('cart-container');
        if (!cartContainer) return;

        if (this.items.length === 0) {
            cartContainer.innerHTML = `
                <div class="empty-cart-page">
                    <i class="fas fa-shopping-cart"></i>
                    <h2>Tu carrito está vacío</h2>
                    <p>Explora nuestros productos y añade lo que necesites</p>
                    <a href="productos.html" class="btn btn-primary">Ver Productos</a>
                </div>
            `;
            return;
        }

        cartContainer.innerHTML = `
            <div class="cart-items">
                <table class="cart-table">
                    <thead>
                        <tr>
                            <th>Producto</th>
                            <th>Precio</th>
                            <th>Cantidad</th>
                            <th>Subtotal</th>
                            <th></th>
                        </tr>
                    </thead>
                    <tbody>
                        ${this.items.map(item => `
                            <tr data-id="${item.id}">
                                <td class="cart-product">
                                    <img src="${item.image}" alt="${item.name}">
                                    <span>${item.name}</span>
                                </td>
                                <td class="cart-price">${item.price.toFixed(2)} €</td>
                                <td class="cart-quantity">
                                    <div class="quantity-control">
                                        <button onclick="cart.updateQuantity('${item.id}', ${item.quantity - 1}); cart.renderFullCart();">-</button>
                                        <input type="number" value="${item.quantity}" min="1" 
                                            onchange="cart.updateQuantity('${item.id}', parseInt(this.value)); cart.renderFullCart();">
                                        <button onclick="cart.updateQuantity('${item.id}', ${item.quantity + 1}); cart.renderFullCart();">+</button>
                                    </div>
                                </td>
                                <td class="cart-subtotal">${(item.price * item.quantity).toFixed(2)} €</td>
                                <td class="cart-remove">
                                    <button onclick="cart.removeItem('${item.id}'); cart.renderFullCart();">
                                        <i class="fas fa-trash"></i>
                                    </button>
                                </td>
                            </tr>
                        `).join('')}
                    </tbody>
                </table>
            </div>
            <div class="cart-summary">
                <h3>Resumen del Pedido</h3>
                <div class="summary-row">
                    <span>Subtotal:</span>
                    <span>${this.getTotal().toFixed(2)} €</span>
                </div>
                <div class="summary-row">
                    <span>IVA (21%):</span>
                    <span>${(this.getTotal() * 0.21).toFixed(2)} €</span>
                </div>
                <div class="summary-row">
                    <span>Envío:</span>
                    <span>${this.getTotal() > 500 ? 'Gratis' : '15.00 €'}</span>
                </div>
                <div class="summary-row total">
                    <span>Total:</span>
                    <span>${this.getFinalTotal().toFixed(2)} €</span>
                </div>
                ${this.isDemo ? '<p class="demo-mode"><i class="fas fa-info-circle"></i> Modo Demo - Los pagos son simulados</p>' : ''}
                <a href="checkout.html" class="btn btn-primary btn-block">Proceder al Pago</a>
                <button onclick="cart.clear(); cart.renderFullCart();" class="btn btn-outline btn-block">Vaciar Carrito</button>
            </div>
        `;
    }

    // Total final con IVA y envío
    getFinalTotal() {
        const subtotal = this.getTotal();
        const iva = subtotal * 0.21;
        const envio = subtotal > 500 ? 0 : 15;
        return subtotal + iva + envio;
    }
}

// Inicializar carrito global
const cart = new ShoppingCart();
