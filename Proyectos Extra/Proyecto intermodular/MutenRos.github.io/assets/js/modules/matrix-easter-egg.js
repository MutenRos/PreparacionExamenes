/**
 * ==========================================================================
 * MUTENROS Portfolio - Matrix Easter Egg Module
 * ==========================================================================
 * 
 * Hidden easter egg triggered by the Konami Code:
 * ↑ ↑ ↓ ↓ ← → ← → B A
 * 
 * Features a Matrix-themed mini-game with:
 * - Pixel art characters (Neo, Morpheus, Keymaker)
 * - White room scene from The Matrix
 * - Hallway of doors leading to projects
 * - Typewriter dialogue system
 * 
 * @author Dario (MutenRos)
 * @version 2.0.0
 * @license MIT
 * ==========================================================================
 */

import CONFIG from '../config.js';

/**
 * MatrixEasterEgg Class
 * Manages the Matrix-themed easter egg experience
 */
class MatrixEasterEgg {
    /**
     * Initialize easter egg
     */
    constructor() {
        // Konami code sequence
        this.konamiCode = [
            'ArrowUp', 'ArrowUp', 
            'ArrowDown', 'ArrowDown', 
            'ArrowLeft', 'ArrowRight', 
            'ArrowLeft', 'ArrowRight', 
            'b', 'a'
        ];
        this.konamiIndex = 0;
        
        // Game state
        this.isActive = false;
        this.overlay = null;
        this.canvas = null;
        this.ctx = null;
        
        // Game objects
        this.gameState = 'white_room';
        this.neo = { x: 120, y: 340, direction: 1, walking: false, breathe: 0, legFrame: 0 };
        this.morpheus = { x: 700, y: 340, breathe: 0 };
        this.keymaker = { x: 0, y: 340, breathe: 0 };
        this.door = { x: 460, y: 180, visible: false, glow: 0 };
        
        this.dialogueState = 0;
        this.canInteract = true;
        this.hallwayScroll = 0;
        this.animTime = 0;
        this.currentDoorIndex = -1;
        
        this.keys = {};
        this.particles = [];
        
        this.boundHandleKeyDown = this.handleKeyDown.bind(this);
        this.boundHandleKeyUp = this.handleKeyUp.bind(this);
        this.boundGameLoop = this.gameLoop.bind(this);
        
        // Bind konami listener
        this.boundCheckKonami = this.checkKonamiCode.bind(this);
    }
    
    /**
     * Initialize konami code listener
     */
    init() {
        document.addEventListener('keydown', this.boundCheckKonami);
        this.checkUrlParams();
        console.log('[MatrixEasterEgg] Initialized - Try the Konami Code!');
    }
    
    /**
     * Check URL params for direct access
     */
    checkUrlParams() {
        const params = new URLSearchParams(window.location.search);
        if (params.get('m') === '1') {
            const doorIndex = parseInt(params.get('d')) || 1;
            window.history.replaceState({}, '', window.location.pathname);
            setTimeout(() => this.start(doorIndex), 500);
        }
    }
    
    /**
     * Check if konami code is being entered
     * @param {KeyboardEvent} e - Keyboard event
     */
    checkKonamiCode(e) {
        const key = e.key.toLowerCase();
        const expected = this.konamiCode[this.konamiIndex].toLowerCase();
        
        if (key === expected || e.key === this.konamiCode[this.konamiIndex]) {
            this.konamiIndex++;
            
            if (this.konamiIndex === this.konamiCode.length) {
                this.konamiIndex = 0;
                this.start();
            }
        } else {
            this.konamiIndex = 0;
        }
    }
    
    /**
     * Start the easter egg
     * @param {number|boolean} skipToHallway - Door index to skip to, or false
     */
    start(skipToHallway = false) {
        if (this.isActive) return;
        this.isActive = true;
        
        this.createOverlay();
        this.initParticles();
        this.resetGameState();
        
        document.body.style.overflow = 'hidden';
        document.addEventListener('keydown', this.boundHandleKeyDown);
        document.addEventListener('keyup', this.boundHandleKeyUp);
        
        // Start game after delay
        setTimeout(() => {
            if (skipToHallway !== false) {
                this.gameState = 'hallway';
                this.neo.x = 450;
                this.hallwayScroll = Math.max(0, (skipToHallway - 1) * 180);
                this.showDialogue('CERRAJERO', 'Bienvenido de vuelta.');
            } else {
                this.showDialogue('SISTEMA', 'Programa de entrenamiento cargado... Acercate a Morpheus.');
            }
            this.gameLoop();
        }, 1000);
        
        console.log('[MatrixEasterEgg] Started');
    }
    
    /**
     * Create game overlay and canvas
     */
    createOverlay() {
        this.overlay = document.createElement('div');
        this.overlay.id = 'matrix-overlay';
        this.overlay.innerHTML = this.getOverlayHTML();
        document.body.appendChild(this.overlay);
        
        this.canvas = document.getElementById('matrix-canvas');
        this.ctx = this.canvas.getContext('2d');
        
        this.dialogueBox = document.getElementById('matrix-dialogue');
        this.dialogueSpeaker = document.getElementById('matrix-speaker');
        this.dialogueText = document.getElementById('matrix-text');
        this.hint = document.getElementById('matrix-hint');
        
        document.getElementById('matrix-exit').onclick = () => this.cleanup();
    }
    
    /**
     * Get overlay HTML structure
     * @returns {string} HTML string
     */
    getOverlayHTML() {
        return `
            <style>${this.getStyles()}</style>
            <canvas id="matrix-canvas" width="1000" height="600"></canvas>
            <div id="matrix-dialogue">
                <div id="matrix-speaker"></div>
                <div id="matrix-text"></div>
            </div>
            <div id="matrix-instructions">&lt; &gt; MOVER | ESPACIO INTERACTUAR | ESC SALIR</div>
            <button id="matrix-exit">X DESPERTAR</button>
            <div class="matrix-hint" id="matrix-hint"></div>
        `;
    }
    
    /**
     * Get CSS styles for the overlay
     * @returns {string} CSS string
     */
    getStyles() {
        return `
            @import url('https://fonts.googleapis.com/css2?family=Press+Start+2P&display=swap');
            
            #matrix-overlay {
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background: #000;
                z-index: 99999;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                font-family: 'Press Start 2P', monospace;
                overflow: hidden;
            }
            
            #matrix-canvas {
                image-rendering: pixelated;
                image-rendering: crisp-edges;
                border: 4px solid #0f0;
                box-shadow: 0 0 50px rgba(0,255,0,0.3), inset 0 0 100px rgba(0,255,0,0.1);
            }
            
            #matrix-dialogue {
                position: absolute;
                bottom: 40px;
                left: 50%;
                transform: translateX(-50%);
                background: linear-gradient(180deg, rgba(0,30,0,0.97) 0%, rgba(0,15,0,0.99) 100%);
                color: #00ff41;
                padding: 20px 35px;
                border: 3px solid #00ff41;
                box-shadow: 0 0 40px rgba(0,255,65,0.4), inset 0 0 40px rgba(0,255,65,0.15);
                font-size: 11px;
                max-width: 750px;
                min-width: 600px;
                text-align: left;
                display: none;
                line-height: 1.9;
                letter-spacing: 1px;
            }
            
            #matrix-dialogue::before {
                content: '';
                position: absolute;
                top: 0;
                left: 0;
                right: 0;
                bottom: 0;
                background: repeating-linear-gradient(0deg, rgba(0,0,0,0.15) 0px, rgba(0,0,0,0.15) 1px, transparent 1px, transparent 3px);
                pointer-events: none;
                animation: scanlines 0.1s linear infinite;
            }
            
            @keyframes scanlines {
                0% { transform: translateY(0); }
                100% { transform: translateY(3px); }
            }
            
            #matrix-speaker {
                color: #fff;
                margin-bottom: 12px;
                text-shadow: 0 0 15px #00ff41;
                font-size: 13px;
            }
            
            #matrix-instructions {
                position: absolute;
                top: 12px;
                left: 50%;
                transform: translateX(-50%);
                color: #0f0;
                font-size: 8px;
                text-align: center;
                letter-spacing: 3px;
                text-shadow: 0 0 10px #0f0;
            }
            
            #matrix-exit {
                position: absolute;
                top: 12px;
                right: 15px;
                background: transparent;
                color: #f00;
                border: 2px solid #f00;
                padding: 8px 12px;
                cursor: pointer;
                font-family: inherit;
                font-size: 8px;
                transition: all 0.3s;
                text-shadow: 0 0 10px #f00;
            }
            
            #matrix-exit:hover {
                background: #f00;
                color: #000;
                box-shadow: 0 0 30px #f00;
            }
            
            .matrix-hint {
                position: absolute;
                bottom: 160px;
                left: 50%;
                transform: translateX(-50%);
                color: #0f0;
                font-size: 10px;
                text-shadow: 0 0 10px #0f0;
                animation: pulse 1.5s ease-in-out infinite;
            }
            
            @keyframes pulse {
                0%, 100% { opacity: 1; }
                50% { opacity: 0.4; }
            }
        `;
    }
    
    /**
     * Initialize matrix rain particles
     */
    initParticles() {
        this.particles = [];
        for (let i = 0; i < 50; i++) {
            this.particles.push({
                x: Math.random() * 1000,
                y: Math.random() * 600,
                speed: 1 + Math.random() * 3,
                char: String.fromCharCode(0x30A0 + Math.random() * 96),
                opacity: Math.random()
            });
        }
    }
    
    /**
     * Reset game state to initial values
     */
    resetGameState() {
        this.gameState = 'white_room';
        this.neo = { x: 120, y: 340, direction: 1, walking: false, breathe: 0, legFrame: 0 };
        this.morpheus = { x: 700, y: 340, breathe: 0 };
        this.keymaker = { x: 0, y: 340, breathe: 0 };
        this.door = { x: 460, y: 180, visible: false, glow: 0 };
        this.dialogueState = 0;
        this.canInteract = true;
        this.hallwayScroll = 0;
        this.animTime = 0;
        this.currentDoorIndex = -1;
        this.keys = {};
    }
    
    /**
     * Main game loop
     */
    gameLoop() {
        if (!this.isActive || !document.getElementById('matrix-overlay')) return;
        
        this.update();
        this.render();
        
        requestAnimationFrame(this.boundGameLoop);
    }
    
    /**
     * Update game state
     */
    update() {
        const speed = 6;
        this.animTime++;
        this.neo.breathe++;
        this.morpheus.breathe++;
        this.keymaker.breathe++;
        
        if (this.neo.walking) this.neo.legFrame++;
        if (this.door.visible) this.door.glow++;
        
        this.neo.walking = false;
        
        if (this.gameState === 'white_room') {
            this.updateWhiteRoom(speed);
        } else if (this.gameState === 'hallway') {
            this.updateHallway(speed);
        }
    }
    
    /**
     * Update white room state
     */
    updateWhiteRoom(speed) {
        if (this.keys['ArrowLeft'] || this.keys['a'] || this.keys['A']) {
            this.neo.x -= speed;
            this.neo.direction = -1;
            this.neo.walking = true;
        }
        if (this.keys['ArrowRight'] || this.keys['d'] || this.keys['D']) {
            this.neo.x += speed;
            this.neo.direction = 1;
            this.neo.walking = true;
        }
        this.neo.x = Math.max(30, Math.min(900, this.neo.x));
    }
    
    /**
     * Update hallway state
     */
    updateHallway(speed) {
        const maxScroll = CONFIG.matrixDoors.length * 200 - 200;
        
        if (this.keys['ArrowLeft'] || this.keys['a'] || this.keys['A']) {
            if (this.neo.x > 300) {
                this.neo.x -= speed;
            } else if (this.hallwayScroll > 0) {
                this.hallwayScroll -= speed;
            }
            this.neo.direction = -1;
            this.neo.walking = true;
        }
        if (this.keys['ArrowRight'] || this.keys['d'] || this.keys['D']) {
            if (this.neo.x < 700) {
                this.neo.x += speed;
            } else if (this.hallwayScroll < maxScroll) {
                this.hallwayScroll += speed;
            }
            this.neo.direction = 1;
            this.neo.walking = true;
        }
    }
    
    /**
     * Render current game state
     */
    render() {
        this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
        
        if (this.gameState === 'white_room') {
            this.renderWhiteRoom();
        } else if (this.gameState === 'hallway') {
            this.renderHallway();
        }
    }
    
    /**
     * Render white room scene
     */
    renderWhiteRoom() {
        // Background gradient
        const bgGradient = this.ctx.createRadialGradient(500, 300, 0, 500, 300, 600);
        bgGradient.addColorStop(0, '#ffffff');
        bgGradient.addColorStop(0.7, '#f5f5f5');
        bgGradient.addColorStop(1, '#e8e8e8');
        this.ctx.fillStyle = bgGradient;
        this.ctx.fillRect(0, 0, 1000, 600);
        
        // Grid
        this.ctx.strokeStyle = 'rgba(0,0,0,0.03)';
        this.ctx.lineWidth = 1;
        for (let i = 0; i < 25; i++) {
            for (let j = 0; j < 15; j++) {
                this.ctx.strokeRect(i * 50 - 25, j * 50, 50, 50);
            }
        }
        
        // Floor reflection
        this.ctx.fillStyle = 'rgba(0,0,0,0.02)';
        this.ctx.fillRect(0, 480, 1000, 120);
        
        // Door
        if (this.door.visible) {
            this.drawMysteryDoor(this.door.x, this.door.y, this.door.glow);
        }
        
        // Characters
        this.drawMorpheus(this.morpheus.x, this.morpheus.y, this.morpheus.breathe);
        this.drawNeo(this.neo.x, this.neo.y, this.neo.direction, this.neo.walking, this.neo.breathe);
        
        // Hints
        this.updateHints();
    }
    
    /**
     * Render hallway scene
     */
    renderHallway() {
        // White background
        this.ctx.fillStyle = '#f8f8f8';
        this.ctx.fillRect(0, 0, 1000, 600);
        
        // Ceiling
        this.ctx.fillStyle = '#ffffff';
        this.ctx.fillRect(0, 0, 1000, 80);
        
        // Ceiling lights
        this.ctx.fillStyle = '#e0e0e0';
        for (let i = 0; i < 15; i++) {
            const lx = i * 120 - (this.hallwayScroll * 0.5 % 120);
            this.ctx.fillRect(lx, 40, 80, 8);
        }
        
        // Walls
        this.ctx.fillStyle = '#f0f0f0';
        this.ctx.fillRect(0, 80, 1000, 40);
        this.ctx.fillRect(0, 480, 1000, 40);
        
        // Moldings
        this.ctx.fillStyle = '#e0e0e0';
        this.ctx.fillRect(0, 115, 1000, 5);
        this.ctx.fillRect(0, 475, 1000, 5);
        
        // Floor
        this.ctx.fillStyle = '#fafafa';
        this.ctx.fillRect(0, 440, 1000, 160);
        
        // Floor lines
        this.ctx.fillStyle = '#f0f0f0';
        for (let i = 0; i < 25; i++) {
            const lx = i * 80 - (this.hallwayScroll % 80);
            this.ctx.fillRect(lx, 440, 2, 160);
        }
        
        // Doors
        let nearDoorIndex = -1;
        CONFIG.matrixDoors.forEach((project, i) => {
            const doorX = 100 + i * 180 - this.hallwayScroll;
            if (doorX > -150 && doorX < 1050) {
                const isNear = Math.abs(this.neo.x + this.hallwayScroll - (140 + i * 180)) < 70;
                if (isNear) nearDoorIndex = i;
                this.drawHallwayDoor(doorX, 260, project, isNear, i + 1);
            }
        });
        
        // Show description when approaching door
        if (nearDoorIndex > 0 && nearDoorIndex !== this.currentDoorIndex && !CONFIG.matrixDoors[nearDoorIndex].mystery) {
            this.showDialogue('CERRAJERO', CONFIG.matrixDoors[nearDoorIndex].desc);
        }
        this.currentDoorIndex = nearDoorIndex;
        
        // Characters
        const kmX = this.neo.x - 80;
        this.drawKeymaker(kmX, this.neo.y + 25, this.keymaker.breathe, this.neo.direction);
        this.drawNeo(this.neo.x, this.neo.y + 10, this.neo.direction, this.neo.walking, this.neo.breathe, true);
        
        // UI
        this.ctx.fillStyle = '#333';
        this.ctx.font = '10px "Press Start 2P"';
        this.ctx.textAlign = 'left';
        this.ctx.fillText('PASILLO DE LAS PUERTAS', 15, 25);
        this.ctx.fillStyle = '#666';
        this.ctx.font = '8px "Press Start 2P"';
        this.ctx.fillText(`${Math.max(1, Math.floor((this.neo.x + this.hallwayScroll) / 180) + 1)} / ${CONFIG.matrixDoors.length}`, 15, 42);
        
        this.hint.style.display = 'none';
    }
    
    // ... (Sprite drawing methods would continue here)
    // For brevity, including essential sprite data and methods
    
    /**
     * Sprite color palette
     */
    get COLORS() {
        return {
            '1': '#0a0a0a', '2': '#1a1a1a', '3': '#2a2a2a',
            'F': '#e8c4a0', 'G': '#1a3a1a', 'B': '#050505', 'S': '#c0c0c0',
            'M': '#0a0a15', 'T': '#12121f', 'W': '#f0f0f0', 'R': '#660000',
            'K': '#6b4423', 'H': '#8b5a2b', 'L': '#888888',
            'C': '#3d3020', 'D': '#4a3d2a', 'P': '#888888', 'A': '#d4a574', 'Y': '#c0a000'
        };
    }
    
    /**
     * Pixel size constant
     */
    get PIXEL() { return 5; }
    
    /**
     * Neo sprite data
     */
    get NEO_SPRITE() {
        return [
            "    111    ", "   11111   ", "   11111   ", "   FFFFF   ", "   FG1GF   ",
            "   FFFFF   ", "    FFF    ", "    111    ", "  1111111  ", "  1211112  ",
            "  1211112  ", "  1211112  ", "  12SSS12  ", "  1211112  ", "  1211112  ",
            "  1211112  ", "   11 11   ", "   11 11   ", "   11 11   ", "   BB BB   "
        ];
    }
    
    /**
     * Morpheus sprite data
     */
    get MORPHEUS_SPRITE() {
        return [
            "    KKK    ", "   KKKKK   ", "   KKKKK   ", "   HHHHH   ", "   HLHLH   ",
            "   H L H   ", "   HHHHH   ", "    HHH    ", "    MMM    ", "  MMWRWMM  ",
            "  MTWRWTM  ", "  MTWRWTM  ", "  MMWRWMM  ", "  MMMMMMM  ", "  MMMMMMM  ",
            "  MMMMMMM  ", "   MM MM   ", "   MM MM   ", "   MM MM   ", "   BB BB   "
        ];
    }
    
    /**
     * Keymaker sprite data
     */
    get KEYMAKER_SPRITE() {
        return [
            "   PPP   ", "  PPPPP  ", "  AAAAA  ", "  A1 1A  ", "  AAAAA  ",
            "   AAA   ", "   CCC   ", "  CCDCC  ", "  CCDCC  ", "  CCDCC  ",
            " YCCCCCY ", " Y CCC Y ", "   C C   ", "   C C   ", "   B B   "
        ];
    }
    
    /**
     * Draw pixel sprite
     */
    drawPixelSprite(sprite, x, y, pixelSize, flipX = false) {
        const width = sprite[0].length;
        sprite.forEach((row, py) => {
            [...row].forEach((pixel, px) => {
                if (this.COLORS[pixel]) {
                    this.ctx.fillStyle = this.COLORS[pixel];
                    const drawX = flipX ? x + (width - 1 - px) * pixelSize : x + px * pixelSize;
                    this.ctx.fillRect(drawX, y + py * pixelSize, pixelSize, pixelSize);
                }
            });
        });
    }
    
    /**
     * Draw Neo character
     */
    drawNeo(x, y, direction, walking, breathe, inHallway = false) {
        const scale = inHallway ? 0.85 : 1;
        const pxSize = Math.floor(this.PIXEL * scale);
        const breatheOffset = Math.floor(Math.sin(breathe * 0.06) * 2);
        
        // Shadow
        this.ctx.fillStyle = 'rgba(0,0,0,0.3)';
        this.ctx.fillRect(x + pxSize, y + 20 * pxSize + breatheOffset, 10 * pxSize, 2 * pxSize);
        
        // Sprite
        this.drawPixelSprite(this.NEO_SPRITE, x, y + breatheOffset, pxSize, direction === -1);
        
        // Walking animation
        if (walking) {
            const legFrame = Math.floor(this.neo.legFrame / 5) % 2;
            this.ctx.fillStyle = this.COLORS['1'];
            const lx = legFrame === 0 
                ? (direction === -1 ? x + 5 * pxSize : x + 3 * pxSize)
                : (direction === -1 ? x + 3 * pxSize : x + 7 * pxSize);
            this.ctx.fillRect(lx, y + 17 * pxSize + breatheOffset, pxSize * 2, pxSize);
        }
    }
    
    /**
     * Draw Morpheus character
     */
    drawMorpheus(x, y, breathe) {
        const breatheOffset = Math.floor(Math.sin(breathe * 0.04) * 1.5);
        
        // Shadow
        this.ctx.fillStyle = 'rgba(0,0,0,0.3)';
        this.ctx.fillRect(x + this.PIXEL, y + 20 * this.PIXEL + breatheOffset, 10 * this.PIXEL, 2 * this.PIXEL);
        
        // Sprite
        this.drawPixelSprite(this.MORPHEUS_SPRITE, x, y + breatheOffset, this.PIXEL, false);
    }
    
    /**
     * Draw Keymaker character
     */
    drawKeymaker(x, y, breathe, direction = 1) {
        const pxSize = Math.floor(this.PIXEL * 0.8);
        const breatheOffset = Math.floor(Math.sin(breathe * 0.05) * 1.5);
        
        // Shadow
        this.ctx.fillStyle = 'rgba(0,255,0,0.15)';
        this.ctx.fillRect(x + pxSize, y + 15 * pxSize + breatheOffset, 8 * pxSize, pxSize);
        
        // Sprite
        this.drawPixelSprite(this.KEYMAKER_SPRITE, x, y + breatheOffset, pxSize, direction === -1);
        
        // Animated keys
        this.ctx.fillStyle = this.COLORS['Y'];
        const keyX = direction === -1 ? x + 8 * pxSize : x;
        for (let i = 0; i < 3; i++) {
            const keyY = y + (10 + i) * pxSize + breatheOffset + Math.sin(breathe * 0.1 + i) * 2;
            this.ctx.fillRect(keyX, keyY, pxSize, pxSize * 2);
            this.ctx.fillRect(keyX - pxSize, keyY, pxSize, pxSize);
        }
    }
    
    /**
     * Draw mystery door (green glowing)
     */
    drawMysteryDoor(x, y, glow) {
        const P = this.PIXEL;
        const glowOn = Math.floor(glow / 15) % 2 === 0;
        
        // Glow aura
        if (glowOn) {
            this.ctx.fillStyle = 'rgba(0, 255, 65, 0.15)';
            this.ctx.fillRect(x - 4*P, y - 4*P, 26*P, 38*P);
            this.ctx.fillStyle = 'rgba(0, 255, 65, 0.08)';
            this.ctx.fillRect(x - 6*P, y - 6*P, 30*P, 42*P);
        }
        
        // Door frame and panels
        this.ctx.fillStyle = '#0a0a0a';
        this.ctx.fillRect(x - 2*P, y - 2*P, 22*P, 34*P);
        this.ctx.fillStyle = '#1a1a1a';
        this.ctx.fillRect(x - P, y - P, 20*P, 32*P);
        this.ctx.fillStyle = '#0f0f0f';
        this.ctx.fillRect(x, y, 18*P, 30*P);
        
        // Panels
        this.ctx.fillStyle = '#080808';
        this.ctx.fillRect(x + 2*P, y + 2*P, 6*P, 10*P);
        this.ctx.fillRect(x + 10*P, y + 2*P, 6*P, 10*P);
        this.ctx.fillRect(x + 2*P, y + 14*P, 6*P, 10*P);
        this.ctx.fillRect(x + 10*P, y + 14*P, 6*P, 10*P);
        
        // Glowing border
        const glowColor = glowOn ? '#00ff41' : '#006618';
        this.ctx.fillStyle = glowColor;
        this.ctx.fillRect(x, y, 18*P, P);
        this.ctx.fillRect(x, y + 29*P, 18*P, P);
        this.ctx.fillRect(x, y, P, 30*P);
        this.ctx.fillRect(x + 17*P, y, P, 30*P);
        
        // Doorknob
        this.ctx.fillStyle = glowOn ? '#00ff41' : '#008822';
        this.ctx.fillRect(x + 14*P, y + 14*P, 2*P, 2*P);
        if (glowOn) {
            this.ctx.fillStyle = '#aaffaa';
            this.ctx.fillRect(x + 14*P, y + 14*P, P, P);
        }
    }
    
    /**
     * Draw hallway door
     */
    drawHallwayDoor(x, y, project, isNear, index) {
        const P = this.PIXEL;
        const doorW = 18 * P;
        const doorH = 30 * P;
        
        if (project.mystery) {
            // Red mystery door
            this.ctx.fillStyle = '#330000';
            this.ctx.fillRect(x - 2*P, y - 2*P, doorW + 4*P, doorH + 4*P);
            this.ctx.fillStyle = '#1a0000';
            this.ctx.fillRect(x, y, doorW, doorH);
            
            // Lock
            this.ctx.fillStyle = '#444444';
            this.ctx.fillRect(x + 7*P, y + 12*P, 4*P, 6*P);
            this.ctx.fillRect(x + 8*P, y + 10*P, 2*P, 2*P);
            
            // Question mark
            this.ctx.fillStyle = isNear ? '#ff0000' : '#880000';
            this.ctx.font = '30px "Press Start 2P"';
            this.ctx.textAlign = 'center';
            this.ctx.fillText('?', x + doorW/2, y + 8*P);
            
            if (isNear) {
                this.ctx.fillStyle = '#ff0000';
                this.ctx.font = '8px "Press Start 2P"';
                this.ctx.fillText('BLOQUEADA', x + doorW/2, y + doorH + 18);
            }
            return;
        }
        
        // Normal door
        this.ctx.fillStyle = '#cccccc';
        this.ctx.fillRect(x + doorW, y + P, 2*P, doorH);
        this.ctx.fillRect(x, y + doorH, doorW + 2*P, 2*P);
        
        this.ctx.fillStyle = isNear ? project.color : '#888888';
        this.ctx.fillRect(x - 2*P, y - 2*P, doorW + 4*P, doorH + 4*P);
        
        this.ctx.fillStyle = isNear ? '#ffffff' : '#e8e8e8';
        this.ctx.fillRect(x, y, doorW, doorH);
        
        // Panels
        this.ctx.fillStyle = isNear ? '#f0f0f0' : '#d8d8d8';
        this.ctx.fillRect(x + 2*P, y + 2*P, 6*P, 10*P);
        this.ctx.fillRect(x + 10*P, y + 2*P, 6*P, 10*P);
        this.ctx.fillRect(x + 2*P, y + 14*P, 6*P, 10*P);
        this.ctx.fillRect(x + 10*P, y + 14*P, 6*P, 10*P);
        
        // Golden doorknob
        this.ctx.fillStyle = isNear ? '#ffd700' : '#c0a000';
        this.ctx.fillRect(x + 14*P, y + 14*P, 2*P, 2*P);
        if (isNear) {
            this.ctx.fillStyle = '#ffff88';
            this.ctx.fillRect(x + 14*P, y + 14*P, P, P);
        }
        
        // Color border when near
        if (isNear) {
            this.ctx.fillStyle = project.color;
            this.ctx.fillRect(x, y, doorW, P);
            this.ctx.fillRect(x, y + doorH - P, doorW, P);
            this.ctx.fillRect(x, y, P, doorH);
            this.ctx.fillRect(x + doorW - P, y, P, doorH);
        }
        
        // Door number
        this.ctx.fillStyle = isNear ? '#000000' : '#666666';
        this.ctx.font = '10px "Press Start 2P"';
        this.ctx.textAlign = 'center';
        this.ctx.fillText(String(index).padStart(2, '0'), x + doorW/2, y - 8);
        
        // Project name
        this.ctx.fillStyle = isNear ? '#000000' : '#666666';
        this.ctx.font = isNear ? '9px "Press Start 2P"' : '7px "Press Start 2P"';
        this.ctx.fillText(project.name, x + doorW/2, y + doorH + 18);
    }
    
    /**
     * Update hint display
     */
    updateHints() {
        const dialogues = this.getDialogues();
        
        if (Math.abs(this.neo.x - this.morpheus.x) < 200 && this.dialogueState < dialogues.length) {
            this.hint.textContent = '[ ESPACIO ] Hablar';
            this.hint.style.display = 'block';
        } else if (this.door.visible && Math.abs(this.neo.x - this.door.x - 55) < 90) {
            this.hint.textContent = '[ ESPACIO ] Cruzar la puerta';
            this.hint.style.display = 'block';
        } else {
            this.hint.style.display = 'none';
        }
    }
    
    /**
     * Get dialogue data
     */
    getDialogues() {
        return [
            { speaker: 'MORPHEUS', text: 'Al fin nos encontramos, Neo.' },
            { speaker: 'MORPHEUS', text: 'Se por que estas aqui. Se lo que has estado buscando.' },
            { speaker: 'MORPHEUS', text: 'La pregunta que nos mueve, Neo. La conoces igual que yo.' },
            { speaker: 'NEO', text: 'Que es la Matrix?' },
            { speaker: 'MORPHEUS', text: 'La respuesta esta ahi fuera, Neo. Te esta buscando.' },
            { speaker: 'MORPHEUS', text: 'Y te encontrara... si tu quieres.' },
            { speaker: 'MORPHEUS', text: 'Alguna vez has tenido un sueno que parecia tan real...?' },
            { speaker: 'MORPHEUS', text: 'Y si no pudieras despertar de ese sueno?' },
            { speaker: 'MORPHEUS', text: 'Como distinguirias el mundo de los suenos... de la realidad?' },
            { speaker: 'NEO', text: 'Esto no puede ser real...' },
            { speaker: 'MORPHEUS', text: 'Que es real? Como defines lo real?' },
            { speaker: 'MORPHEUS', text: 'Si hablas de lo que puedes sentir, oler, saborear y ver...' },
            { speaker: 'MORPHEUS', text: '...entonces lo real son simples senales electricas interpretadas por tu cerebro.' },
            { speaker: 'MORPHEUS', text: 'Bienvenido... al desierto de lo real.' },
            { speaker: 'MORPHEUS', text: 'Hay una puerta, Neo. Solo tu puedes abrirla.' },
            { speaker: 'MORPHEUS', text: 'Yo solo puedo mostrarte el camino. Tu debes recorrerlo.' },
            { speaker: 'MORPHEUS', text: 'Buena suerte, Neo. Nos veremos del otro lado.' }
        ];
    }
    
    /**
     * Show dialogue box with typewriter effect
     */
    showDialogue(speaker, text) {
        this.dialogueBox.style.display = 'block';
        this.dialogueSpeaker.textContent = speaker + ':';
        
        // Speaker colors
        const colors = {
            'NEO': '#00aaff',
            'CERRAJERO': '#ffd700',
            'SISTEMA': '#ff0000'
        };
        this.dialogueSpeaker.style.color = colors[speaker] || '#00ff41';
        
        this.dialogueText.textContent = '';
        this.canInteract = false;
        
        let i = 0;
        const speed = speaker === 'CERRAJERO' ? 25 : 30;
        
        const typeWriter = setInterval(() => {
            if (i < text.length) {
                this.dialogueText.textContent += text[i];
                i++;
            } else {
                clearInterval(typeWriter);
                setTimeout(() => { this.canInteract = true; }, 400);
            }
        }, speed);
    }
    
    /**
     * Hide dialogue box
     */
    hideDialogue() {
        this.dialogueBox.style.display = 'none';
    }
    
    /**
     * Handle key down
     */
    handleKeyDown(e) {
        if (!this.isActive) return;
        
        this.keys[e.key] = true;
        
        if (e.key === 'Escape') {
            this.cleanup();
            return;
        }
        
        if (e.key === ' ' && this.canInteract) {
            e.preventDefault();
            this.handleInteraction();
        }
    }
    
    /**
     * Handle space bar interaction
     */
    handleInteraction() {
        const dialogues = this.getDialogues();
        
        if (this.gameState === 'white_room') {
            if (Math.abs(this.neo.x - this.morpheus.x - 40) < 150 && this.dialogueState < dialogues.length) {
                const d = dialogues[this.dialogueState];
                this.showDialogue(d.speaker, d.text);
                this.dialogueState++;
                
                if (this.dialogueState >= dialogues.length) {
                    setTimeout(() => {
                        this.door.visible = true;
                        this.hideDialogue();
                    }, 2500);
                }
            } else if (this.door.visible && Math.abs(this.neo.x - this.door.x - 55) < 90) {
                this.transitionToHallway();
            }
        } else if (this.gameState === 'hallway') {
            if (this.currentDoorIndex >= 0) {
                const project = CONFIG.matrixDoors[this.currentDoorIndex];
                if (project.mystery) {
                    this.showDialogue('CERRAJERO', 'No tengo llave para esta puerta.');
                } else if (project.url) {
                    this.showDialogue('CERRAJERO', 'Esta es.');
                    setTimeout(() => {
                        window.open(project.url, '_blank');
                    }, 800);
                }
            }
        }
    }
    
    /**
     * Transition to hallway scene
     */
    transitionToHallway() {
        this.canvas.style.transition = 'filter 0.8s';
        this.canvas.style.filter = 'brightness(3) blur(10px)';
        
        setTimeout(() => {
            this.gameState = 'hallway';
            this.neo.x = 450;
            this.neo.y = 320;
            this.hallwayScroll = 0;
            this.hideDialogue();
            this.canvas.style.filter = 'brightness(1) blur(0)';
            
            setTimeout(() => {
                this.showDialogue('CERRAJERO', 'Bienvenido. Cada puerta lleva a un proyecto diferente.');
            }, 500);
        }, 800);
    }
    
    /**
     * Handle key up
     */
    handleKeyUp(e) {
        this.keys[e.key] = false;
    }
    
    /**
     * Cleanup and exit
     */
    cleanup() {
        document.removeEventListener('keydown', this.boundHandleKeyDown);
        document.removeEventListener('keyup', this.boundHandleKeyUp);
        
        if (this.overlay) {
            this.overlay.remove();
            this.overlay = null;
        }
        
        document.body.style.overflow = '';
        this.isActive = false;
        
        console.log('[MatrixEasterEgg] Cleanup complete');
    }
    
    /**
     * Destroy and remove all listeners
     */
    destroy() {
        document.removeEventListener('keydown', this.boundCheckKonami);
        this.cleanup();
    }
}

// Create singleton instance
const matrixEasterEgg = new MatrixEasterEgg();

export default matrixEasterEgg;
export { MatrixEasterEgg };
