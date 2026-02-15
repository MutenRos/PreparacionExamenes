/**
 * Sistema de Autenticación - Bombas Asoin
 * Simulado con localStorage para demo
 */

class AuthSystem {
    constructor() {
        this.currentUser = JSON.parse(localStorage.getItem('ba_user')) || null;
        this.users = JSON.parse(localStorage.getItem('ba_users')) || [];
        this.orders = JSON.parse(localStorage.getItem('ba_orders')) || [];
        this.init();
    }

    init() {
        this.updateAuthUI();
        
        // Crear admin por defecto si no existe
        if (!this.users.find(u => u.email === 'admin@asoinbombas.es')) {
            this.users.push({
                id: 'admin',
                email: 'admin@asoinbombas.es',
                password: 'admin123',
                name: 'Administrador',
                role: 'admin',
                createdAt: new Date().toISOString()
            });
            this.saveUsers();
        }
    }

    // Guardar usuarios
    saveUsers() {
        localStorage.setItem('ba_users', JSON.stringify(this.users));
    }

    // Guardar pedidos
    saveOrders() {
        localStorage.setItem('ba_orders', JSON.stringify(this.orders));
    }

    // Registrar usuario
    register(userData) {
        // Validar email único
        if (this.users.find(u => u.email === userData.email)) {
            return { success: false, message: 'Este email ya está registrado' };
        }

        const newUser = {
            id: 'user_' + Date.now(),
            email: userData.email,
            password: userData.password,
            name: userData.name,
            phone: userData.phone || '',
            address: userData.address || '',
            city: userData.city || '',
            postalCode: userData.postalCode || '',
            role: 'customer',
            createdAt: new Date().toISOString()
        };

        this.users.push(newUser);
        this.saveUsers();
        
        // Auto login
        this.login(userData.email, userData.password);
        
        return { success: true, message: 'Cuenta creada correctamente' };
    }

    // Iniciar sesión
    login(email, password) {
        const user = this.users.find(u => u.email === email && u.password === password);
        
        if (!user) {
            return { success: false, message: 'Email o contraseña incorrectos' };
        }

        this.currentUser = { ...user };
        delete this.currentUser.password;
        localStorage.setItem('ba_user', JSON.stringify(this.currentUser));
        this.updateAuthUI();
        
        return { success: true, message: 'Sesión iniciada', user: this.currentUser };
    }

    // Cerrar sesión
    logout() {
        this.currentUser = null;
        localStorage.removeItem('ba_user');
        this.updateAuthUI();
        window.location.href = 'index.html';
    }

    // Verificar si está autenticado
    isAuthenticated() {
        return this.currentUser !== null;
    }

    // Verificar si es admin
    isAdmin() {
        return this.currentUser && this.currentUser.role === 'admin';
    }

    // Actualizar UI según estado de autenticación
    updateAuthUI() {
        const authLinks = document.getElementById('auth-links');
        if (!authLinks) return;

        if (this.isAuthenticated()) {
            authLinks.innerHTML = `
                <a href="cuenta.html" class="auth-link">
                    <i class="fas fa-user"></i> ${this.currentUser.name}
                </a>
                ${this.isAdmin() ? '<a href="admin.html" class="auth-link admin-link"><i class="fas fa-cog"></i> Admin</a>' : ''}
                <a href="#" onclick="auth.logout(); return false;" class="auth-link">
                    <i class="fas fa-sign-out-alt"></i> Salir
                </a>
            `;
        } else {
            authLinks.innerHTML = `
                <a href="login.html" class="auth-link">
                    <i class="fas fa-sign-in-alt"></i> Iniciar Sesión
                </a>
                <a href="registro.html" class="auth-link">
                    <i class="fas fa-user-plus"></i> Registro
                </a>
            `;
        }
    }

    // Actualizar datos del usuario
    updateProfile(userData) {
        if (!this.isAuthenticated()) return { success: false };

        const userIndex = this.users.findIndex(u => u.id === this.currentUser.id);
        if (userIndex === -1) return { success: false };

        this.users[userIndex] = { ...this.users[userIndex], ...userData };
        this.saveUsers();

        this.currentUser = { ...this.users[userIndex] };
        delete this.currentUser.password;
        localStorage.setItem('ba_user', JSON.stringify(this.currentUser));

        return { success: true, message: 'Perfil actualizado' };
    }

    // Crear pedido
    createOrder(orderData) {
        const order = {
            id: 'ORD-' + Date.now(),
            userId: this.currentUser ? this.currentUser.id : 'guest',
            customerName: orderData.name,
            customerEmail: orderData.email,
            customerPhone: orderData.phone,
            shippingAddress: orderData.address,
            shippingCity: orderData.city,
            shippingPostalCode: orderData.postalCode,
            items: orderData.items,
            subtotal: orderData.subtotal,
            iva: orderData.iva,
            shipping: orderData.shipping,
            total: orderData.total,
            paymentMethod: orderData.paymentMethod,
            paymentStatus: 'completed', // Siempre completado en modo demo
            orderStatus: 'pending',
            isDemo: true,
            createdAt: new Date().toISOString()
        };

        this.orders.push(order);
        this.saveOrders();

        return order;
    }

    // Obtener pedidos del usuario actual
    getUserOrders() {
        if (!this.isAuthenticated()) return [];
        return this.orders.filter(o => o.userId === this.currentUser.id);
    }

    // Obtener todos los pedidos (admin)
    getAllOrders() {
        return this.orders;
    }

    // Actualizar estado del pedido (admin)
    updateOrderStatus(orderId, status) {
        const order = this.orders.find(o => o.id === orderId);
        if (order) {
            order.orderStatus = status;
            this.saveOrders();
            return true;
        }
        return false;
    }

    // Obtener todos los usuarios (admin)
    getAllUsers() {
        return this.users.map(u => {
            const user = { ...u };
            delete user.password;
            return user;
        });
    }
}

// Inicializar sistema de autenticación
const auth = new AuthSystem();
