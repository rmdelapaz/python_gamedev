console.log('Save/Load System Demo starting...');

// Game State Class
class GameState {
    constructor() {
        this.score = 0;
        this.level = 1;
        this.items = 0;
        this.playerX = 300;
        this.playerY = 200;
        this.enemies = [];
        this.achievements = [];
        this.playTime = 0;
        this.startTime = Date.now();
        
        // Visual elements
        this.particles = [];
    }
    
    update(dt) {
        this.playTime += dt;
        
        // Update particles
        this.particles.forEach(p => p.update(dt));
        this.particles = this.particles.filter(p => p.alive);
    }
    
    toJSON() {
        return {
            version: '1.0.0',
            timestamp: Date.now(),
            score: this.score,
            level: this.level,
            items: this.items,
            playerPosition: {
                x: this.playerX,
                y: this.playerY
            },
            enemies: this.enemies.map(e => ({
                x: e.x,
                y: e.y,
                type: e.type
            })),
            achievements: this.achievements,
            playTime: this.playTime
        };
    }
    
    fromJSON(data) {
        this.score = data.score || 0;
        this.level = data.level || 1;
        this.items = data.items || 0;
        
        if (data.playerPosition) {
            this.playerX = data.playerPosition.x;
            this.playerY = data.playerPosition.y;
        }
        
        this.enemies = (data.enemies || []).map(e => new Enemy(e.x, e.y, e.type));
        this.achievements = data.achievements || [];
        this.playTime = data.playTime || 0;
    }
}

// Enemy Class
class Enemy {
    constructor(x, y, type = 'basic') {
        this.x = x;
        this.y = y;
        this.type = type;
        this.color = type === 'basic' ? '#ff0000' : '#ff00ff';
        this.size = 15;
    }
    
    draw(ctx) {
        ctx.fillStyle = this.color;
        ctx.fillRect(this.x - this.size/2, this.y - this.size/2, this.size, this.size);
    }
}

// Particle Class
class Particle {
    constructor(x, y, color) {
        this.x = x;
        this.y = y;
        this.vx = (Math.random() - 0.5) * 200;
        this.vy = (Math.random() - 0.5) * 200;
        this.color = color;
        this.size = Math.random() * 5 + 2;
        this.lifetime = 1;
        this.age = 0;
        this.alive = true;
    }
    
    update(dt) {
        this.x += this.vx * dt;
        this.y += this.vy * dt;
        this.age += dt;
        
        if (this.age >= this.lifetime) {
            this.alive = false;
        }
    }
    
    draw(ctx) {
        const alpha = 1 - (this.age / this.lifetime);
        ctx.fillStyle = this.color + Math.floor(alpha * 255).toString(16).padStart(2, '0');
        ctx.beginPath();
        ctx.arc(this.x, this.y, this.size * (1 - this.age / this.lifetime), 0, Math.PI * 2);
        ctx.fill();
    }
}

// Save Slot Class
class SaveSlot {
    constructor(id) {
        this.id = id;
        this.data = null;
        this.isEmpty = true;
    }
    
    save(gameState) {
        this.data = gameState.toJSON();
        this.isEmpty = false;
        this.updateDisplay();
    }
    
    load() {
        return this.data;
    }
    
    clear() {
        this.data = null;
        this.isEmpty = true;
        this.updateDisplay();
    }
    
    updateDisplay() {
        const slotDiv = document.getElementById(`slot-${this.id}`);
        if (!slotDiv) return;
        
        if (this.isEmpty) {
            slotDiv.innerHTML = `
                <div style="background-color: #333; padding: 5px; border-radius: 3px;">
                    <strong>Slot ${this.id}</strong>: Empty
                </div>
            `;
        } else {
            const date = new Date(this.data.timestamp);
            slotDiv.innerHTML = `
                <div style="background-color: #2a4a2a; padding: 5px; border-radius: 3px;">
                    <strong>Slot ${this.id}</strong><br>
                    Level: ${this.data.level} | Score: ${this.data.score}<br>
                    ${date.toLocaleTimeString()}
                </div>
            `;
        }
    }
}

// Save Manager Class
class SaveManager {
    constructor() {
        this.slots = {};
        this.quickSaveSlot = null;
        this.autoSaveSlot = null;
        this.saveFormat = 'json';
        this.encrypt = false;
        this.cloudSync = false;
        
        // Initialize slots
        for (let i = 1; i <= 3; i++) {
            this.slots[i] = new SaveSlot(i);
        }
        
        // Load from localStorage if available
        this.loadFromStorage();
    }
    
    save(slotId, gameState) {
        const slot = this.slots[slotId];
        if (!slot) return false;
        
        slot.save(gameState);
        this.saveToStorage();
        this.showNotification(`Game saved to Slot ${slotId}`);
        
        // Create save effect
        this.createSaveEffect();
        
        return true;
    }
    
    load(slotId, gameState) {
        const slot = this.slots[slotId];
        if (!slot || slot.isEmpty) {
            this.showNotification(`Slot ${slotId} is empty`);
            return false;
        }
        
        const data = slot.load();
        gameState.fromJSON(data);
        this.showNotification(`Game loaded from Slot ${slotId}`);
        
        // Create load effect
        this.createLoadEffect();
        
        return true;
    }
    
    quickSave(gameState) {
        this.quickSaveSlot = gameState.toJSON();
        this.saveToStorage();
        this.showNotification('Quick save complete');
        this.createSaveEffect();
    }
    
    quickLoad(gameState) {
        if (!this.quickSaveSlot) {
            this.showNotification('No quick save available');
            return false;
        }
        
        gameState.fromJSON(this.quickSaveSlot);
        this.showNotification('Quick load complete');
        this.createLoadEffect();
        return true;
    }
    
    autoSave(gameState) {
        this.autoSaveSlot = gameState.toJSON();
        this.saveToStorage();
        this.showNotification('Auto-save complete');
    }
    
    exportSave(gameState) {
        const data = gameState.toJSON();
        const jsonStr = JSON.stringify(data, null, 2);
        
        // Create download
        const blob = new Blob([jsonStr], { type: 'application/json' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `savegame_${Date.now()}.json`;
        a.click();
        
        this.showNotification('Save exported');
    }
    
    importSave(gameState) {
        const input = document.createElement('input');
        input.type = 'file';
        input.accept = '.json';
        
        input.onchange = (e) => {
            const file = e.target.files[0];
            const reader = new FileReader();
            
            reader.onload = (event) => {
                try {
                    const data = JSON.parse(event.target.result);
                    gameState.fromJSON(data);
                    this.showNotification('Save imported successfully');
                    this.createLoadEffect();
                } catch (error) {
                    this.showNotification('Failed to import save');
                }
            };
            
            reader.readAsText(file);
        };
        
        input.click();
    }
    
    saveToStorage() {
        try {
            const saveData = {
                slots: {},
                quickSave: this.quickSaveSlot,
                autoSave: this.autoSaveSlot
            };
            
            for (const [id, slot] of Object.entries(this.slots)) {
                saveData.slots[id] = slot.data;
            }
            
            let dataStr = JSON.stringify(saveData);
            
            if (this.encrypt) {
                // Simple XOR encryption for demo
                dataStr = this.simpleEncrypt(dataStr);
            }
            
            localStorage.setItem('gameSaves', dataStr);
            
            if (this.cloudSync) {
                this.syncToCloud(dataStr);
            }
        } catch (e) {
            console.error('Failed to save to storage:', e);
        }
    }
    
    loadFromStorage() {
        try {
            let dataStr = localStorage.getItem('gameSaves');
            if (!dataStr) return;
            
            if (this.encrypt) {
                dataStr = this.simpleDecrypt(dataStr);
            }
            
            const saveData = JSON.parse(dataStr);
            
            for (const [id, data] of Object.entries(saveData.slots || {})) {
                if (data && this.slots[id]) {
                    this.slots[id].data = data;
                    this.slots[id].isEmpty = false;
                    this.slots[id].updateDisplay();
                }
            }
            
            this.quickSaveSlot = saveData.quickSave;
            this.autoSaveSlot = saveData.autoSave;
        } catch (e) {
            console.error('Failed to load from storage:', e);
        }
    }
    
    simpleEncrypt(str) {
        // Very simple XOR encryption for demonstration
        const key = 42;
        return str.split('').map(c => 
            String.fromCharCode(c.charCodeAt(0) ^ key)
        ).join('');
    }
    
    simpleDecrypt(str) {
        // XOR is symmetric
        return this.simpleEncrypt(str);
    }
    
    syncToCloud(data) {
        // Simulated cloud sync
        console.log('Syncing to cloud...', data.length, 'bytes');
    }
    
    showNotification(message) {
        // Could implement a proper notification system
        console.log(message);
        
        // Update preview
        const preview = document.getElementById('saveDataPreview');
        if (preview) {
            const timestamp = new Date().toLocaleTimeString();
            preview.innerHTML = `[${timestamp}] ${message}<br>` + preview.innerHTML;
            
            // Keep only recent messages
            const lines = preview.innerHTML.split('<br>');
            if (lines.length > 10) {
                preview.innerHTML = lines.slice(0, 10).join('<br>');
            }
        }
    }
    
    createSaveEffect() {
        // Visual effect for saving
        for (let i = 0; i < 20; i++) {
            gameManager.gameState.particles.push(
                new Particle(
                    Math.random() * 600,
                    Math.random() * 400,
                    '#00ff00'
                )
            );
        }
    }
    
    createLoadEffect() {
        // Visual effect for loading
        for (let i = 0; i < 20; i++) {
            gameManager.gameState.particles.push(
                new Particle(
                    Math.random() * 600,
                    Math.random() * 400,
                    '#00ffff'
                )
            );
        }
    }
    
    updateDisplay() {
        // Update save slots display
        const slotsDiv = document.getElementById('saveSlots');
        if (!slotsDiv) return;
        
        slotsDiv.innerHTML = '';
        for (const [id, slot] of Object.entries(this.slots)) {
            const slotDiv = document.createElement('div');
            slotDiv.id = `slot-${id}`;
            slotsDiv.appendChild(slotDiv);
            slot.updateDisplay();
        }
    }
}

// Game Manager
class GameManager {
    constructor(canvas, ctx) {
        this.canvas = canvas;
        this.ctx = ctx;
        this.gameState = new GameState();
        this.saveManager = new SaveManager();
        
        this.saveManager.updateDisplay();
    }
    
    update(dt) {
        this.gameState.update(dt);
        this.updateDisplays();
    }
    
    draw() {
        // Clear canvas
        this.ctx.fillStyle = '#1a1a1a';
        this.ctx.fillRect(0, 0, this.canvas.width, this.canvas.height);
        
        // Draw grid
        this.ctx.strokeStyle = 'rgba(255, 255, 255, 0.05)';
        this.ctx.lineWidth = 1;
        for (let x = 0; x <= this.canvas.width; x += 50) {
            this.ctx.beginPath();
            this.ctx.moveTo(x, 0);
            this.ctx.lineTo(x, this.canvas.height);
            this.ctx.stroke();
        }
        for (let y = 0; y <= this.canvas.height; y += 50) {
            this.ctx.beginPath();
            this.ctx.moveTo(0, y);
            this.ctx.lineTo(this.canvas.width, y);
            this.ctx.stroke();
        }
        
        // Draw player
        this.ctx.fillStyle = '#00ff00';
        this.ctx.beginPath();
        this.ctx.arc(this.gameState.playerX, this.gameState.playerY, 15, 0, Math.PI * 2);
        this.ctx.fill();
        
        // Draw enemies
        this.gameState.enemies.forEach(enemy => enemy.draw(this.ctx));
        
        // Draw items
        for (let i = 0; i < this.gameState.items; i++) {
            const x = 50 + (i % 10) * 30;
            const y = 50 + Math.floor(i / 10) * 30;
            
            this.ctx.fillStyle = '#ffff00';
            this.ctx.beginPath();
            this.ctx.arc(x, y, 5, 0, Math.PI * 2);
            this.ctx.fill();
        }
        
        // Draw particles
        this.gameState.particles.forEach(p => p.draw(this.ctx));
        
        // Draw UI
        this.drawUI();
    }
    
    drawUI() {
        // Score
        this.ctx.fillStyle = '#ffffff';
        this.ctx.font = '20px Arial';
        this.ctx.textAlign = 'left';
        this.ctx.fillText(`Score: ${this.gameState.score}`, 10, 30);
        
        // Level
        this.ctx.fillText(`Level: ${this.gameState.level}`, 10, 60);
        
        // Save format indicator
        this.ctx.font = '12px Arial';
        this.ctx.fillText(`Format: ${this.saveManager.saveFormat}`, 10, 390);
        
        if (this.saveManager.encrypt) {
            this.ctx.fillText('🔒 Encrypted', 100, 390);
        }
        
        if (this.saveManager.cloudSync) {
            this.ctx.fillText('☁️ Cloud Sync', 200, 390);
        }
    }
    
    updateDisplays() {
        document.getElementById('score').textContent = this.gameState.score;
        document.getElementById('level').textContent = this.gameState.level;
        document.getElementById('items').textContent = this.gameState.items;
        document.getElementById('playerX').textContent = Math.round(this.gameState.playerX);
        document.getElementById('playerY').textContent = Math.round(this.gameState.playerY);
        document.getElementById('enemies').textContent = this.gameState.enemies.length;
        document.getElementById('achievements').textContent = this.gameState.achievements.length;
        
        const minutes = Math.floor(this.gameState.playTime / 60);
        const seconds = Math.floor(this.gameState.playTime % 60);
        document.getElementById('playTime').textContent = `${minutes}:${seconds.toString().padStart(2, '0')}`;
    }
    
    updateSavePreview() {
        const preview = document.getElementById('saveDataPreview');
        if (preview && this.saveManager.quickSaveSlot) {
            const data = this.saveManager.quickSaveSlot;
            preview.innerHTML += `<pre>${JSON.stringify(data, null, 2)}</pre>`;
        }
    }
}

// Initialize
const saveCanvas = document.getElementById('saveCanvas');
const ctx = saveCanvas.getContext('2d');
const gameManager = new GameManager(saveCanvas, ctx);

// Global functions
window.movePlayer = function() {
    gameManager.gameState.playerX = Math.random() * 500 + 50;
    gameManager.gameState.playerY = Math.random() * 300 + 50;
    
    // Add movement particles
    for (let i = 0; i < 5; i++) {
        gameManager.gameState.particles.push(
            new Particle(
                gameManager.gameState.playerX,
                gameManager.gameState.playerY,
                '#00ff00'
            )
        );
    }
};

window.collectItem = function() {
    gameManager.gameState.items++;
    gameManager.gameState.score += 10;
    
    // Add collection particles
    for (let i = 0; i < 10; i++) {
        gameManager.gameState.particles.push(
            new Particle(
                Math.random() * 600,
                Math.random() * 400,
                '#ffff00'
            )
        );
    }
};

window.spawnEnemy = function() {
    const enemy = new Enemy(
        Math.random() * 500 + 50,
        Math.random() * 300 + 50,
        Math.random() > 0.5 ? 'basic' : 'elite'
    );
    gameManager.gameState.enemies.push(enemy);
};

window.increaseScore = function() {
    gameManager.gameState.score += 100;
};

window.unlockAchievement = function() {
    const achievement = `Achievement_${gameManager.gameState.achievements.length + 1}`;
    gameManager.gameState.achievements.push(achievement);
    gameManager.saveManager.showNotification(`Unlocked: ${achievement}`);
};

window.completeLevel = function() {
    gameManager.gameState.level++;
    gameManager.gameState.score += 500;
    gameManager.saveManager.showNotification(`Level ${gameManager.gameState.level} reached!`);
};

window.saveGame = function(slot) {
    gameManager.saveManager.save(slot, gameManager.gameState);
};

window.loadGame = function(slot) {
    gameManager.saveManager.load(slot, gameManager.gameState);
};

window.quickSave = function() {
    gameManager.saveManager.quickSave(gameManager.gameState);
};

window.quickLoad = function() {
    gameManager.saveManager.quickLoad(gameManager.gameState);
};

window.autoSave = function() {
    gameManager.saveManager.autoSave(gameManager.gameState);
};

window.exportSave = function() {
    gameManager.saveManager.exportSave(gameManager.gameState);
};

window.importSave = function() {
    gameManager.saveManager.importSave(gameManager.gameState);
};

window.resetGame = function() {
    gameManager.gameState = new GameState();
    gameManager.saveManager.showNotification('Game reset');
};

window.setSaveFormat = function(format) {
    gameManager.saveManager.saveFormat = format;
    gameManager.saveManager.showNotification(`Save format: ${format}`);
};

window.toggleEncryption = function() {
    gameManager.saveManager.encrypt = document.getElementById('encryptSaves').checked;
    gameManager.saveManager.showNotification(
        gameManager.saveManager.encrypt ? 'Encryption enabled' : 'Encryption disabled'
    );
};

window.toggleCloudSync = function() {
    gameManager.saveManager.cloudSync = document.getElementById('cloudSync').checked;
    gameManager.saveManager.showNotification(
        gameManager.saveManager.cloudSync ? 'Cloud sync enabled' : 'Cloud sync disabled'
    );
};

// Keyboard shortcuts
document.addEventListener('keydown', (e) => {
    if (e.key === 'F5') {
        e.preventDefault();
        quickSave();
    } else if (e.key === 'F9') {
        e.preventDefault();
        quickLoad();
    }
});

// Animation loop
let lastTime = performance.now();

function animate(currentTime) {
    const dt = (currentTime - lastTime) / 1000;
    lastTime = currentTime;
    
    gameManager.update(dt);
    gameManager.draw();
    
    requestAnimationFrame(animate);
}

// Start animation
animate(performance.now());

console.log('Save/Load System Demo initialized successfully!');