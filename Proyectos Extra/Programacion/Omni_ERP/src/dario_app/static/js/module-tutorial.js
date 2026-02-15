/**
 * Module-specific Tutorial System
 * Extends the main tutorial with contextual guides for each module
 */

class ModuleTutorial {
    constructor(moduleName) {
        this.moduleName = moduleName;
        this.currentStep = 1;
        this.totalSteps = 0;
        this.isPlaying = false;
        this.steps = [];
        
        this.overlay = null;
        this.popup = null;
        this.highlightBox = null;
        this.progressBar = null;
        
        this.init();
    }

    async init() {
        try {
            // Check if user has completed this module tutorial
            const status = await this.getModuleStatus();
            
            // Load module steps
            this.steps = await this.getModuleSteps();
            this.totalSteps = this.steps.length;
            
            if (this.totalSteps === 0) {
                console.log(`No tutorial available for ${this.moduleName}`);
                return;
            }

            // Create UI elements
            this.createTutorialElements();
            
            // Add keyboard listeners
            document.addEventListener('keydown', (e) => this.handleKeyPress(e));
            
            // Create help button
            this.createHelpButton();
            
            // Auto-start for first-time visitors
            if (!status.has_completed && status.current_step === 0) {
                console.log(`🎮 Iniciando tutorial de ${this.moduleName}...`);
                setTimeout(() => this.showStartModal(), 800);
            }
        } catch (error) {
            console.error('Error inicializando tutorial de módulo:', error);
        }
    }

    createTutorialElements() {
        // Overlay
        this.overlay = document.createElement('div');
        this.overlay.id = `module-tutorial-overlay-${this.moduleName}`;
        this.overlay.className = 'tutorial-overlay hidden';
        document.body.appendChild(this.overlay);

        // Highlight box
        this.highlightBox = document.createElement('div');
        this.highlightBox.id = `module-tutorial-highlight-${this.moduleName}`;
        this.highlightBox.className = 'tutorial-highlight hidden';
        document.body.appendChild(this.highlightBox);

        // Popup
        this.popup = document.createElement('div');
        this.popup.id = `module-tutorial-popup-${this.moduleName}`;
        this.popup.className = 'tutorial-popup hidden';
        document.body.appendChild(this.popup);

        // Progress bar
        this.progressBar = document.createElement('div');
        this.progressBar.id = `module-tutorial-progress-${this.moduleName}`;
        this.progressBar.className = 'tutorial-progress hidden';
        this.progressBar.innerHTML = '<div class="progress-fill"></div>';
        document.body.appendChild(this.progressBar);
    }

    showStartModal() {
        const modal = document.createElement('div');
        modal.className = 'tutorial-start-modal';
        modal.innerHTML = `
            <div class="tutorial-modal-content">
                <h1>🎯 Tutorial: ${this.getModuleTitle()}</h1>
                <p>Aprende las funciones principales de este módulo en ${this.totalSteps} pasos rápidos.</p>
                <div class="tutorial-modal-buttons">
                    <button class="btn btn-primary" id="start-module-tutorial-btn">
                        Comenzar 🚀
                    </button>
                    <button class="btn btn-secondary" id="skip-module-tutorial-btn">
                        Omitir
                    </button>
                </div>
            </div>
        `;
        document.body.appendChild(modal);

        document.getElementById('start-module-tutorial-btn').addEventListener('click', () => {
            modal.remove();
            this.startTutorial();
        });

        document.getElementById('skip-module-tutorial-btn').addEventListener('click', () => {
            modal.remove();
            this.skipTutorial();
        });
    }

    getModuleTitle() {
        const titles = {
            'pos': 'Punto de Venta',
            'inventario': 'Inventario',
            'logistica': 'Logística',
            'produccion': 'Producción',
            'ventas': 'Ventas',
            'compras': 'Compras',
            'hr': 'Recursos Humanos',
            'financial': 'Finanzas',
            'marketing': 'Marketing',
        };
        return titles[this.moduleName] || this.moduleName;
    }

    async startTutorial() {
        this.isPlaying = true;
        await fetch(`/api/tutorial/modules/${this.moduleName}/start`, { method: 'POST' });
        this.showStep(1);
    }

    async showStep(stepNumber) {
        if (stepNumber < 1 || stepNumber > this.totalSteps) return;

        this.currentStep = stepNumber;
        const step = this.steps[stepNumber - 1];

        if (!step) return;

        // Update backend
        await fetch(`/api/tutorial/modules/${this.moduleName}/step/${stepNumber}`, {
            method: 'POST'
        });

        // Show overlay
        this.showOverlay();

        // Highlight element if needed
        if (step.highlight && step.selector !== 'body') {
            this.highlightElement(step.selector);
        } else {
            this.hideHighlight();
        }

        // Show popup
        this.showPopup(step, stepNumber);
        
        // Update progress bar
        this.updateProgressBar(stepNumber);
    }

    highlightElement(selector) {
        try {
            const element = document.querySelector(selector);
            if (!element) {
                console.warn(`Elemento no encontrado: ${selector}`);
                this.hideHighlight();
                return;
            }

            const rect = element.getBoundingClientRect();
            const padding = 8;

            this.highlightBox.style.top = rect.top - padding + 'px';
            this.highlightBox.style.left = rect.left - padding + 'px';
            this.highlightBox.style.width = rect.width + padding * 2 + 'px';
            this.highlightBox.style.height = rect.height + padding * 2 + 'px';
            this.highlightBox.classList.remove('hidden');

            element.scrollIntoView({ behavior: 'smooth', block: 'center' });
        } catch (error) {
            console.error('Error destacando elemento:', error);
            this.hideHighlight();
        }
    }

    hideHighlight() {
        this.highlightBox.classList.add('hidden');
    }

    showOverlay() {
        this.overlay.classList.remove('hidden');
    }

    hideOverlay() {
        this.overlay.classList.add('hidden');
    }

    showPopup(step, stepNumber) {
        const isLast = stepNumber === this.totalSteps;
        const actionText = isLast ? 'Finalizar 🎉' : 'Siguiente →';
        const actionClass = isLast ? 'btn-success' : 'btn-primary';

        this.popup.innerHTML = `
            <div class="tutorial-popup-header">
                <span class="tutorial-popup-number">Paso ${stepNumber}/${this.totalSteps}</span>
                <button class="tutorial-popup-close" onclick="window.moduleTutorial_${this.moduleName}.closeTutorial()">✕</button>
            </div>
            <div class="tutorial-popup-body">
                <h2>${step.title}</h2>
                <p>${step.description}</p>
            </div>
            <div class="tutorial-popup-footer">
                <button class="btn btn-secondary" onclick="window.moduleTutorial_${this.moduleName}.previousStep()">
                    ← Anterior
                </button>
                <button class="btn ${actionClass}" onclick="window.moduleTutorial_${this.moduleName}.nextStep()">
                    ${actionText}
                </button>
            </div>
        `;
        
        this.popup.classList.remove('hidden');
        this.positionPopup(step.position);
    }

    positionPopup(position) {
        this.popup.className = 'tutorial-popup';
        this.popup.classList.add(`tutorial-popup-${position}`);
    }

    updateProgressBar(stepNumber) {
        const percentage = (stepNumber / this.totalSteps) * 100;
        const progressFill = this.progressBar.querySelector('.progress-fill');
        progressFill.style.width = percentage + '%';
        this.progressBar.classList.remove('hidden');
    }

    async nextStep() {
        if (this.currentStep < this.totalSteps) {
            this.showStep(this.currentStep + 1);
        } else {
            await this.completeTutorial();
        }
    }

    previousStep() {
        if (this.currentStep > 1) {
            this.showStep(this.currentStep - 1);
        }
    }

    async completeTutorial() {
        try {
            await fetch(`/api/tutorial/modules/${this.moduleName}/complete`, {
                method: 'POST'
            });
            this.showCompletionModal();
            this.closeTutorial();
        } catch (error) {
            console.error('Error completando tutorial:', error);
        }
    }

    showCompletionModal() {
        const modal = document.createElement('div');
        modal.className = 'tutorial-completion-modal';
        modal.innerHTML = `
            <div class="completion-content">
                <h1>🎉 ¡Tutorial Completado!</h1>
                <p>Ya dominas las funciones principales de ${this.getModuleTitle()}.</p>
                <button class="btn btn-primary" onclick="this.parentElement.parentElement.remove()">
                    Continuar
                </button>
            </div>
        `;
        document.body.appendChild(modal);

        setTimeout(() => {
            modal.style.animation = 'fadeOut 0.5s forwards';
            setTimeout(() => modal.remove(), 500);
        }, 2500);
    }

    closeTutorial() {
        this.isPlaying = false;
        this.hideOverlay();
        this.hideHighlight();
        this.popup.classList.add('hidden');
        this.progressBar.classList.add('hidden');
    }

    async skipTutorial() {
        try {
            await fetch(`/api/tutorial/modules/${this.moduleName}/complete`, { method: 'POST' });
            this.closeTutorial();
        } catch (error) {
            console.error('Error saltando tutorial:', error);
        }
    }

    createHelpButton() {
        const button = document.createElement('button');
        button.id = `module-tutorial-help-${this.moduleName}`;
        button.className = 'tutorial-help-button hidden-taskbar';
        button.innerHTML = '❓';
        button.title = `Tutorial de ${this.getModuleTitle()} (presiona '?')`;
        button.style.display = 'none'; // Hide by default, use taskbar instead
        button.addEventListener('click', () => this.restartTutorial());
        document.body.appendChild(button);
    }

    async restartTutorial() {
        try {
            await fetch(`/api/tutorial/modules/${this.moduleName}/reset`, { method: 'DELETE' });
            this.currentStep = 1;
            this.startTutorial();
        } catch (error) {
            console.error('Error reiniciando tutorial:', error);
        }
    }

    handleKeyPress(e) {
        if (!this.isPlaying) return;

        switch (e.key) {
            case 'Escape':
                e.preventDefault();
                this.closeTutorial();
                break;
            case 'ArrowRight':
            case ' ':
                e.preventDefault();
                this.nextStep();
                break;
            case 'ArrowLeft':
                e.preventDefault();
                this.previousStep();
                break;
            case '?':
                if (!this.isPlaying) {
                    e.preventDefault();
                    this.restartTutorial();
                }
                break;
        }
    }

    async getModuleStatus() {
        try {
            const response = await fetch(`/api/tutorial/modules/${this.moduleName}/status`);
            return await response.json();
        } catch (error) {
            console.error('Error obteniendo estado del módulo:', error);
            return { has_completed: false, current_step: 0 };
        }
    }

    async getModuleSteps() {
        try {
            const response = await fetch(`/api/tutorial/modules/${this.moduleName}/steps`);
            return await response.json();
        } catch (error) {
            console.error('Error obteniendo pasos del módulo:', error);
            return [];
        }
    }
}

// Auto-initialize based on current page
(function() {
    // Detect module from URL path
    const path = window.location.pathname;
    const moduleMatch = path.match(/\/app\/([^\/]+)/);
    
    if (moduleMatch) {
        const moduleName = moduleMatch[1];
        const validModules = ['pos', 'inventario', 'logistica', 'produccion', 'produccion-ordenes', 
                             'ventas', 'compras', 'hr', 'financial', 'marketing'];
        
        if (validModules.includes(moduleName)) {
            // Wait for DOM to be ready
            const init = () => {
                const instance = new ModuleTutorial(moduleName);
                window[`moduleTutorial_${moduleName}`] = instance;
                window.tutorial = instance; // Assign to window.tutorial for taskbar compatibility
            };

            if (document.readyState === 'loading') {
                document.addEventListener('DOMContentLoaded', init);
            } else {
                init();
            }
        }
    }
})();
