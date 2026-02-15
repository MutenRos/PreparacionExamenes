/**
 * Sistema de Checkout - Bombas Bloch
 * Incluye pasarela de pago simulada
 */

class CheckoutSystem {
    constructor() {
        this.step = 1;
        this.orderData = {};
        this.init();
    }

    init() {
        this.renderCheckout();
        this.bindEvents();
    }

    bindEvents() {
        // Form submissions
        document.addEventListener('submit', (e) => {
            if (e.target.id === 'shipping-form') {
                e.preventDefault();
                this.processShipping(e.target);
            }
            if (e.target.id === 'payment-form') {
                e.preventDefault();
                this.processPayment(e.target);
            }
        });
    }

    renderCheckout() {
        const container = document.getElementById('checkout-container');
        if (!container) return;

        // Verificar que hay items en el carrito
        if (cart.items.length === 0) {
            container.innerHTML = `
                <div class="empty-cart-page">
                    <i class="fas fa-shopping-cart"></i>
                    <h2>Tu carrito está vacío</h2>
                    <p>Añade productos antes de proceder al pago</p>
                    <a href="productos.html" class="btn btn-primary">Ver Productos</a>
                </div>
            `;
            return;
        }

        container.innerHTML = `
            <div class="checkout-steps">
                <div class="step ${this.step >= 1 ? 'active' : ''} ${this.step > 1 ? 'completed' : ''}">
                    <span class="step-number">1</span>
                    <span class="step-label">Envío</span>
                </div>
                <div class="step-line ${this.step > 1 ? 'active' : ''}"></div>
                <div class="step ${this.step >= 2 ? 'active' : ''} ${this.step > 2 ? 'completed' : ''}">
                    <span class="step-number">2</span>
                    <span class="step-label">Pago</span>
                </div>
                <div class="step-line ${this.step > 2 ? 'active' : ''}"></div>
                <div class="step ${this.step >= 3 ? 'active' : ''}">
                    <span class="step-number">3</span>
                    <span class="step-label">Confirmación</span>
                </div>
            </div>

            <div class="checkout-content">
                <div class="checkout-main">
                    ${this.renderCurrentStep()}
                </div>
                <div class="checkout-sidebar">
                    ${this.renderOrderSummary()}
                </div>
            </div>
        `;
    }

    renderCurrentStep() {
        switch(this.step) {
            case 1:
                return this.renderShippingStep();
            case 2:
                return this.renderPaymentStep();
            case 3:
                return this.renderConfirmationStep();
            default:
                return '';
        }
    }

    renderShippingStep() {
        const user = auth.currentUser || {};
        
        return `
            <div class="checkout-step-content">
                <h2><i class="fas fa-truck"></i> Datos de Envío</h2>
                
                ${!auth.isAuthenticated() ? `
                    <div class="guest-notice">
                        <p>¿Ya tienes cuenta? <a href="login.html?redirect=checkout">Inicia sesión</a> para autorellenar tus datos</p>
                    </div>
                ` : ''}

                <form id="shipping-form">
                    <div class="form-row">
                        <div class="form-group">
                            <label for="name">Nombre completo *</label>
                            <input type="text" id="name" name="name" value="${user.name || ''}" required>
                        </div>
                        <div class="form-group">
                            <label for="email">Email *</label>
                            <input type="email" id="email" name="email" value="${user.email || ''}" required>
                        </div>
                    </div>
                    <div class="form-row">
                        <div class="form-group">
                            <label for="phone">Teléfono *</label>
                            <input type="tel" id="phone" name="phone" value="${user.phone || ''}" required>
                        </div>
                        <div class="form-group">
                            <label for="company">Empresa (opcional)</label>
                            <input type="text" id="company" name="company">
                        </div>
                    </div>
                    <div class="form-group">
                        <label for="address">Dirección *</label>
                        <input type="text" id="address" name="address" value="${user.address || ''}" required 
                            placeholder="Calle, número, piso...">
                    </div>
                    <div class="form-row">
                        <div class="form-group">
                            <label for="postalCode">Código Postal *</label>
                            <input type="text" id="postalCode" name="postalCode" value="${user.postalCode || ''}" required>
                        </div>
                        <div class="form-group">
                            <label for="city">Ciudad *</label>
                            <input type="text" id="city" name="city" value="${user.city || ''}" required>
                        </div>
                    </div>
                    <div class="form-group">
                        <label for="notes">Notas del pedido (opcional)</label>
                        <textarea id="notes" name="notes" rows="3" 
                            placeholder="Instrucciones especiales de entrega..."></textarea>
                    </div>
                    <div class="form-actions">
                        <a href="carrito.html" class="btn btn-outline">
                            <i class="fas fa-arrow-left"></i> Volver al carrito
                        </a>
                        <button type="submit" class="btn btn-primary">
                            Continuar al pago <i class="fas fa-arrow-right"></i>
                        </button>
                    </div>
                </form>
            </div>
        `;
    }

    renderPaymentStep() {
        return `
            <div class="checkout-step-content">
                <h2><i class="fas fa-credit-card"></i> Método de Pago</h2>
                
                <div class="demo-banner">
                    <i class="fas fa-info-circle"></i>
                    <div>
                        <strong>Modo Demostración</strong>
                        <p>Los pagos son simulados. No se realizará ningún cargo real.</p>
                    </div>
                </div>

                <form id="payment-form">
                    <div class="payment-methods">
                        <label class="payment-method">
                            <input type="radio" name="paymentMethod" value="card" checked>
                            <div class="payment-method-content">
                                <i class="fas fa-credit-card"></i>
                                <span>Tarjeta de Crédito/Débito</span>
                                <div class="card-icons">
                                    <i class="fab fa-cc-visa"></i>
                                    <i class="fab fa-cc-mastercard"></i>
                                    <i class="fab fa-cc-amex"></i>
                                </div>
                            </div>
                        </label>
                        <label class="payment-method">
                            <input type="radio" name="paymentMethod" value="paypal">
                            <div class="payment-method-content">
                                <i class="fab fa-paypal"></i>
                                <span>PayPal</span>
                            </div>
                        </label>
                        <label class="payment-method">
                            <input type="radio" name="paymentMethod" value="transfer">
                            <div class="payment-method-content">
                                <i class="fas fa-university"></i>
                                <span>Transferencia Bancaria</span>
                            </div>
                        </label>
                        <label class="payment-method">
                            <input type="radio" name="paymentMethod" value="bizum">
                            <div class="payment-method-content">
                                <i class="fas fa-mobile-alt"></i>
                                <span>Bizum</span>
                            </div>
                        </label>
                    </div>

                    <div id="card-form-fields" class="payment-details">
                        <div class="form-group">
                            <label for="cardNumber">Número de tarjeta</label>
                            <input type="text" id="cardNumber" placeholder="1234 5678 9012 3456" 
                                maxlength="19" value="4242 4242 4242 4242">
                            <small>Usa 4242 4242 4242 4242 para pruebas</small>
                        </div>
                        <div class="form-row">
                            <div class="form-group">
                                <label for="cardExpiry">Fecha de expiración</label>
                                <input type="text" id="cardExpiry" placeholder="MM/AA" maxlength="5" value="12/28">
                            </div>
                            <div class="form-group">
                                <label for="cardCvc">CVC</label>
                                <input type="text" id="cardCvc" placeholder="123" maxlength="4" value="123">
                            </div>
                        </div>
                        <div class="form-group">
                            <label for="cardName">Nombre en la tarjeta</label>
                            <input type="text" id="cardName" placeholder="NOMBRE APELLIDOS" 
                                value="${this.orderData.name || ''}">
                        </div>
                    </div>

                    <div class="form-group terms">
                        <label class="checkbox-label">
                            <input type="checkbox" id="acceptTerms" required>
                            <span>Acepto los <a href="aviso-legal.html" target="_blank">términos y condiciones</a> 
                            y la <a href="politica-privacidad.html" target="_blank">política de privacidad</a></span>
                        </label>
                    </div>

                    <div class="form-actions">
                        <button type="button" onclick="checkout.goToStep(1)" class="btn btn-outline">
                            <i class="fas fa-arrow-left"></i> Volver
                        </button>
                        <button type="submit" class="btn btn-primary btn-pay">
                            <i class="fas fa-lock"></i> Pagar ${cart.getFinalTotal().toFixed(2)} €
                        </button>
                    </div>
                </form>
            </div>
        `;
    }

    renderConfirmationStep() {
        return `
            <div class="checkout-step-content confirmation">
                <div class="confirmation-icon">
                    <i class="fas fa-check-circle"></i>
                </div>
                <h2>¡Pedido Confirmado!</h2>
                <p class="order-number">Número de pedido: <strong>${this.orderData.orderId}</strong></p>
                
                <div class="demo-notice">
                    <i class="fas fa-flask"></i>
                    <p><strong>Modo Demo:</strong> Este es un pedido de prueba. No se ha realizado ningún cargo real.</p>
                </div>

                <div class="confirmation-details">
                    <div class="detail-section">
                        <h4><i class="fas fa-envelope"></i> Confirmación enviada</h4>
                        <p>Hemos enviado los detalles a: <strong>${this.orderData.email}</strong></p>
                    </div>
                    <div class="detail-section">
                        <h4><i class="fas fa-truck"></i> Dirección de envío</h4>
                        <p>${this.orderData.address}<br>
                        ${this.orderData.postalCode} ${this.orderData.city}</p>
                    </div>
                    <div class="detail-section">
                        <h4><i class="fas fa-credit-card"></i> Método de pago</h4>
                        <p>${this.getPaymentMethodLabel(this.orderData.paymentMethod)}</p>
                    </div>
                </div>

                <div class="confirmation-actions">
                    ${auth.isAuthenticated() ? 
                        '<a href="cuenta.html" class="btn btn-outline">Ver mis pedidos</a>' : 
                        '<a href="registro.html" class="btn btn-outline">Crear cuenta</a>'
                    }
                    <a href="index.html" class="btn btn-primary">Volver a la tienda</a>
                </div>
            </div>
        `;
    }

    renderOrderSummary() {
        return `
            <div class="order-summary-box">
                <h3>Resumen del Pedido</h3>
                <div class="summary-items">
                    ${cart.items.map(item => `
                        <div class="summary-item">
                            <img src="${item.image}" alt="${item.name}">
                            <div class="item-details">
                                <span class="item-name">${item.name}</span>
                                <span class="item-qty">x${item.quantity}</span>
                            </div>
                            <span class="item-price">${(item.price * item.quantity).toFixed(2)} €</span>
                        </div>
                    `).join('')}
                </div>
                <div class="summary-totals">
                    <div class="summary-row">
                        <span>Subtotal</span>
                        <span>${cart.getTotal().toFixed(2)} €</span>
                    </div>
                    <div class="summary-row">
                        <span>IVA (21%)</span>
                        <span>${(cart.getTotal() * 0.21).toFixed(2)} €</span>
                    </div>
                    <div class="summary-row">
                        <span>Envío</span>
                        <span>${cart.getTotal() > 500 ? 'Gratis' : '15.00 €'}</span>
                    </div>
                    <div class="summary-row total">
                        <span>Total</span>
                        <span>${cart.getFinalTotal().toFixed(2)} €</span>
                    </div>
                </div>
            </div>
        `;
    }

    processShipping(form) {
        const formData = new FormData(form);
        this.orderData = {
            name: formData.get('name'),
            email: formData.get('email'),
            phone: formData.get('phone'),
            company: formData.get('company'),
            address: formData.get('address'),
            postalCode: formData.get('postalCode'),
            city: formData.get('city'),
            notes: formData.get('notes')
        };
        this.goToStep(2);
    }

    processPayment(form) {
        const formData = new FormData(form);
        const paymentMethod = formData.get('paymentMethod');
        
        // Mostrar loading
        const payBtn = form.querySelector('.btn-pay');
        const originalText = payBtn.innerHTML;
        payBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Procesando...';
        payBtn.disabled = true;

        // Simular procesamiento de pago (2 segundos)
        setTimeout(() => {
            // Crear pedido
            const order = auth.createOrder({
                ...this.orderData,
                items: cart.items,
                subtotal: cart.getTotal(),
                iva: cart.getTotal() * 0.21,
                shipping: cart.getTotal() > 500 ? 0 : 15,
                total: cart.getFinalTotal(),
                paymentMethod: paymentMethod
            });

            this.orderData.orderId = order.id;
            this.orderData.paymentMethod = paymentMethod;

            // Limpiar carrito
            cart.clear();

            // Ir a confirmación
            this.goToStep(3);
        }, 2000);
    }

    goToStep(step) {
        this.step = step;
        this.renderCheckout();
        window.scrollTo(0, 0);
    }

    getPaymentMethodLabel(method) {
        const labels = {
            'card': 'Tarjeta de crédito/débito',
            'paypal': 'PayPal',
            'transfer': 'Transferencia bancaria',
            'bizum': 'Bizum'
        };
        return labels[method] || method;
    }
}

// Inicializar checkout si estamos en la página
let checkout;
document.addEventListener('DOMContentLoaded', () => {
    if (document.getElementById('checkout-container')) {
        checkout = new CheckoutSystem();
    }
});
