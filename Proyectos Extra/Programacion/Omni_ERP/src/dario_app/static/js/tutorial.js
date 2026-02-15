/**
 * Tutorial System - Interactive ERP Onboarding
 * Estilo videojuego con popups, highlights y navegación fluida
 */

class ERPTutorial {
    constructor() {
        this.currentStep = 1;
        this.totalSteps = 0;
        this.isPlaying = false;
        this.autoplayDelay = 500;
        this.steps = [];

        // Elementos del DOM
        this.overlay = null;
        this.popup = null;
        this.highlightBox = null;

        this.init();
    }

    /**
     * Inicializar el tutorial
     */
    async init() {
        try {
            // Obtener estado del tutorial
            const status = await this.getTutorialStatus();

            // Si ya completó el tutorial, no mostrar
            if (status.has_completed) {
                console.log("✓ Tutorial ya completado");
                return;
            }

            // Cargar pasos
            this.steps = await this.getTutorialSteps();
            this.totalSteps = this.steps.length || 0;

            // Crear elementos visuales
            this.createTutorialElements();

            // Escuchar teclas
            document.addEventListener("keydown", (e) => this.handleKeyPress(e));

            // Mostrar botón flotante de ayuda
            this.createHelpButton();

            // Auto-iniciar para usuarios nuevos
            if (status.current_step === 0) {
                console.log("🎮 Iniciando tutorial...");
                this.showStartModal();
            }
        } catch (error) {
            console.error("Error inicializando tutorial:", error);
        }
    }

    /**
     * Crear elementos visuales del tutorial
     */
    createTutorialElements() {
        // Overlay oscuro
        this.overlay = document.createElement("div");
        this.overlay.id = "tutorial-overlay";
        this.overlay.className = "tutorial-overlay hidden";
        document.body.appendChild(this.overlay);

        // Caja de highlight
        this.highlightBox = document.createElement("div");
        this.highlightBox.id = "tutorial-highlight";
        this.highlightBox.className = "tutorial-highlight hidden";
        document.body.appendChild(this.highlightBox);

        // Popup principal
        this.popup = document.createElement("div");
        this.popup.id = "tutorial-popup";
        this.popup.className = "tutorial-popup hidden";
        document.body.appendChild(this.popup);

        // Indicador de progreso
        this.progressBar = document.createElement("div");
        this.progressBar.id = "tutorial-progress";
        this.progressBar.className = "tutorial-progress hidden";
        document.body.appendChild(this.progressBar);
    }

    /**
     * Mostrar modal inicial
     */
    showStartModal() {
        const modal = document.createElement("div");
        modal.className = "tutorial-start-modal";
        modal.innerHTML = `
            <div class="tutorial-modal-content">
                <h1>🎮 Bienvenido al ERP Dario</h1>
                <p>Te mostraremos todas las funciones principales en un tour interactivo de 2 minutos.</p>
                <div class="tutorial-modal-features">
                    <div class="feature">📊 Dashboard en tiempo real</div>
                    <div class="feature">💳 Gestión de ventas y compras</div>
                    <div class="feature">📦 Control de inventario</div>
                    <div class="feature">🤖 Automatizaciones sin código</div>
                </div>
                <div class="tutorial-modal-buttons">
                    <button class="btn btn-primary" id="start-tutorial-btn">
                        Iniciar Tour 🚀
                    </button>
                    <button class="btn btn-secondary" id="skip-tutorial-btn">
                        Saltar
                    </button>
                </div>
            </div>
        `;
        document.body.appendChild(modal);

        document.getElementById("start-tutorial-btn").addEventListener("click", () => {
            modal.remove();
            this.startTutorial();
        });

        document.getElementById("skip-tutorial-btn").addEventListener("click", () => {
            modal.remove();
            this.skipTutorial();
        });
    }

    /**
     * Iniciar el tutorial
     */
    async startTutorial() {
        this.isPlaying = true;
        await this.updateTutorialStep(1);
        this.showStep(1);
    }

    /**
     * Mostrar un paso específico
     */
    async showStep(stepNumber) {
        if (stepNumber < 1 || stepNumber > this.totalSteps) return;

        this.currentStep = stepNumber;
        const step = this.steps[stepNumber - 1];

        if (!step) return;

        // Actualizar progreso en servidor
        await this.updateTutorialStep(stepNumber);

        // Mostrar overlay y popup
        this.showOverlay();

        // Si hay un selector válido, destacarlo
        if (step.highlight && step.selector !== "body") {
            this.highlightElement(step.selector);
        } else {
            this.hideHighlight();
        }

        // Mostrar popup
        this.showPopup(step, stepNumber);

        // Actualizar barra de progreso
        this.updateProgressBar(stepNumber);
    }

    /**
     * Destacar elemento
     */
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

            this.highlightBox.style.top = rect.top - padding + "px";
            this.highlightBox.style.left = rect.left - padding + "px";
            this.highlightBox.style.width = rect.width + padding * 2 + "px";
            this.highlightBox.style.height = rect.height + padding * 2 + "px";
            this.highlightBox.classList.remove("hidden");

            // Scroll suave al elemento
            element.scrollIntoView({ behavior: "smooth", block: "center" });
        } catch (error) {
            console.error("Error destacando elemento:", error);
            this.hideHighlight();
        }
    }

    /**
     * Ocultar highlight
     */
    hideHighlight() {
        this.highlightBox.classList.add("hidden");
    }

    /**
     * Mostrar overlay
     */
    showOverlay() {
        this.overlay.classList.remove("hidden");
    }

    /**
     * Ocultar overlay
     */
    hideOverlay() {
        this.overlay.classList.add("hidden");
    }

    /**
     * Mostrar popup con contenido del paso
     */
    showPopup(step, stepNumber) {
        const isLast = stepNumber === this.totalSteps;
        const isFinal = stepNumber === this.totalSteps;

        const actionButtonText = isFinal ? "Finalizar 🎉" : "Siguiente →";
        const actionButtonClass = isFinal ? "btn-success" : "btn-primary";

        let popupHTML = `
            <div class="tutorial-popup-header">
                <span class="tutorial-popup-number">Paso ${stepNumber}/${this.totalSteps}</span>
                <button class="tutorial-popup-close" onclick="window.tutorial.closeTutorial()">✕</button>
            </div>
            <div class="tutorial-popup-body">
                <h2>${step.title}</h2>
                <p>${step.description.replace(/\n/g, "<br>")}</p>
        `;

        if (step.image_url) {
            popupHTML += `<img src="${step.image_url}" class="tutorial-popup-image" />`;
        }

        popupHTML += `
            </div>
            <div class="tutorial-popup-footer">
                <button class="btn btn-secondary" onclick="window.tutorial.previousStep()">
                    ← Anterior
                </button>
                <button class="btn ${actionButtonClass}" onclick="window.tutorial.nextStep()">
                    ${actionButtonText}
                </button>
            </div>
        `;

        this.popup.innerHTML = popupHTML;
        this.popup.classList.remove("hidden");

        // Posicionar popup
        this.positionPopup(step.position);
    }

    /**
     * Posicionar popup según posición especificada
     */
    positionPopup(position) {
        const popup = this.popup;
        popup.className = "tutorial-popup hidden";
        popup.classList.remove("hidden");
        popup.classList.add(`tutorial-popup-${position}`);
    }

    /**
     * Actualizar barra de progreso
     */
    updateProgressBar(stepNumber) {
        const percentage = (stepNumber / this.totalSteps) * 100;

        if (!this.progressBar.innerHTML) {
            this.progressBar.innerHTML = `<div class="progress-fill"></div>`;
        }

        const progressFill = this.progressBar.querySelector(".progress-fill");
        progressFill.style.width = percentage + "%";
        this.progressBar.classList.remove("hidden");
    }

    /**
     * Siguiente paso
     */
    async nextStep() {
        if (this.currentStep < this.totalSteps) {
            this.showStep(this.currentStep + 1);
        } else {
            await this.completeTutorial();
        }
    }

    /**
     * Paso anterior
     */
    previousStep() {
        if (this.currentStep > 1) {
            this.showStep(this.currentStep - 1);
        }
    }

    /**
     * Completar tutorial
     */
    async completeTutorial() {
        try {
            await fetch("/api/tutorial/complete", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ completed: true, final_step: this.totalSteps }),
            });

            this.showCompletionModal();
            this.closeTutorial();
        } catch (error) {
            console.error("Error completando tutorial:", error);
        }
    }

    /**
     * Mostrar modal de finalización
     */
    showCompletionModal() {
        const modal = document.createElement("div");
        modal.className = "tutorial-completion-modal";
        modal.innerHTML = `
            <div class="completion-content">
                <h1>🎉 ¡Tutorial Completado!</h1>
                <p>Ya conoces todas las funciones principales del ERP.</p>
                <p style="font-size: 2em; margin: 20px 0;">Ahora a conquistar el mundo 🚀</p>
                <button class="btn btn-primary" onclick="this.parentElement.parentElement.remove()">
                    Comenzar a usar
                </button>
            </div>
        `;
        document.body.appendChild(modal);

        setTimeout(() => {
            modal.style.animation = "fadeOut 0.5s forwards";
            setTimeout(() => modal.remove(), 500);
        }, 3000);
    }

    /**
     * Cerrar tutorial
     */
    closeTutorial() {
        this.isPlaying = false;
        this.hideOverlay();
        this.hideHighlight();
        this.popup.classList.add("hidden");
        this.progressBar.classList.add("hidden");
    }

    /**
     * Saltar tutorial
     */
    async skipTutorial() {
        try {
            await fetch("/api/tutorial/skip", { method: "POST" });
            this.closeTutorial();
            console.log("✓ Tutorial saltado");
        } catch (error) {
            console.error("Error saltando tutorial:", error);
        }
    }

    /**
     * Crear botón flotante de ayuda
     */
    createHelpButton() {
        const button = document.createElement("button");
        button.id = "tutorial-help-button";
        button.className = "tutorial-help-button";
        button.innerHTML = "❓";
        button.title = "Reiniciar tutorial (o presiona '?')";
        button.classList.add("hidden-taskbar");
        button.style.display = "none";
        button.addEventListener("click", () => this.restartTutorial());
        document.body.appendChild(button);
    }

    /**
     * Reiniciar tutorial
     */
    async restartTutorial() {
        try {
            await fetch("/api/tutorial/reset", { method: "DELETE" });
            this.currentStep = 1;
            this.startTutorial();
        } catch (error) {
            console.error("Error reiniciando tutorial:", error);
        }
    }

    /**
     * Manejar pulsación de teclas
     */
    handleKeyPress(e) {
        if (!this.isPlaying) return;

        switch (e.key) {
            case "Escape":
                e.preventDefault();
                this.closeTutorial();
                break;
            case "ArrowRight":
            case " ":
                e.preventDefault();
                this.nextStep();
                break;
            case "ArrowLeft":
                e.preventDefault();
                this.previousStep();
                break;
            case "?":
                e.preventDefault();
                this.restartTutorial();
                break;
        }
    }

    /**
     * API: Obtener estado del tutorial
     */
    async getTutorialStatus() {
        try {
            const response = await fetch("/api/tutorial/status");
            return await response.json();
        } catch (error) {
            console.error("Error obteniendo estado:", error);
            return { has_completed: false, current_step: 0 };
        }
    }

    /**
     * API: Obtener todos los pasos
     */
    async getTutorialSteps() {
        try {
            const response = await fetch("/api/tutorial/steps");
            return await response.json();
        } catch (error) {
            console.error("Error obteniendo pasos:", error);
            return [];
        }
    }

    /**
     * API: Actualizar paso actual
     */
    async updateTutorialStep(stepNumber) {
        try {
            await fetch(`/api/tutorial/step/${stepNumber}`, { method: "POST" });
        } catch (error) {
            console.error("Error actualizando paso:", error);
        }
    }
}

// Inicializar cuando el documento esté listo
if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", () => {
        window.tutorial = new ERPTutorial();
    });
} else {
    window.tutorial = new ERPTutorial();
}
