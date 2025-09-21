console.log('Event System Visualizer starting...');

// Event class
class GameEvent {
    constructor(type, data = {}) {
        this.id = Math.random().toString(36).substr(2, 9);
        this.type = type;
        this.data = data;
        this.timestamp = Date.now();
        this.priority = data.priority || 5;
        this.processed = false;
    }
}

// Visual representation of an event
class EventVisual {
    constructor(event, x, y) {
        this.event = event;
        this.x = x;
        this.y = y;
        this.targetX = x;
        this.targetY = y;
        this.radius = 8;
        this.color = this.getEventColor(event.type);
        this.alpha = 1;
        this.trail = [];
        this.maxTrailLength = 10;
        this.delivered = false;
        this.lifetime = 3; // seconds
        this.age = 0;
    }
    
    getEventColor(type) {
        const colors = {
            'player_jump': '#00ff00',
            'enemy_spawn': '#ff0000',
            'item_collected': '#ffff00',
            'level_complete': '#00ffff',
            'damage_dealt': '#ff00ff',
            'achievement_unlocked': '#ffa500'
        };
        return colors[type] || '#ffffff';
    }
    
    moveTo(x, y) {
        this.targetX = x;
        this.targetY = y;
    }
    
    update(dt) {
        // Add current position to trail
        this.trail.push({ x: this.x, y: this.y, alpha: this.alpha });
        if (this.trail.length > this.maxTrailLength) {
            this.trail.shift();
        }
        
        // Move toward target
        const dx = this.targetX - this.x;
        const dy = this.targetY - this.y;
        const distance = Math.sqrt(dx * dx + dy * dy);
        
        if (distance > 1) {
            const speed = 200 * window.eventSpeed; // pixels per second
            const moveDistance = speed * dt;
            const ratio = Math.min(moveDistance / distance, 1);
            
            this.x += dx * ratio;
            this.y += dy * ratio;
        } else if (!this.delivered) {
            this.delivered = true;
        }
        
        // Age and fade
        this.age += dt;
        if (this.age > this.lifetime) {
            this.alpha = Math.max(0, this.alpha - dt * 2);
        }
        
        // Update trail alpha
        this.trail.forEach((point, i) => {
            point.alpha = (i / this.trail.length) * this.alpha * 0.5;
        });
    }
    
    draw(ctx) {
        // Draw trail
        this.trail.forEach(point => {
            ctx.fillStyle = this.color + Math.floor(point.alpha * 255).toString(16).padStart(2, '0');
            ctx.beginPath();
            ctx.arc(point.x, point.y, this.radius * 0.5, 0, Math.PI * 2);
            ctx.fill();
        });
        
        // Draw event
        ctx.save();
        ctx.globalAlpha = this.alpha;
        
        // Glow effect
        const gradient = ctx.createRadialGradient(this.x, this.y, 0, this.x, this.y, this.radius * 2);
        gradient.addColorStop(0, this.color);
        gradient.addColorStop(1, 'transparent');
        ctx.fillStyle = gradient;
        ctx.beginPath();
        ctx.arc(this.x, this.y, this.radius * 2, 0, Math.PI * 2);
        ctx.fill();
        
        // Core
        ctx.fillStyle = this.color;
        ctx.beginPath();
        ctx.arc(this.x, this.y, this.radius, 0, Math.PI * 2);
        ctx.fill();
        
        // Border
        ctx.strokeStyle = '#ffffff';
        ctx.lineWidth = 2;
        ctx.stroke();
        
        ctx.restore();
    }
}

// System subscriber visual
class SystemNode {
    constructor(name, x, y) {
        this.name = name;
        this.x = x;
        this.y = y;
        this.width = 100;
        this.height = 40;
        this.active = true;
        this.receivedEvents = [];
        this.pulsePhase = Math.random() * Math.PI * 2;
        this.color = this.getSystemColor(name);
    }
    
    getSystemColor(name) {
        const colors = {
            'AudioSystem': '#4CAF50',
            'UISystem': '#2196F3',
            'AchievementSystem': '#FF9800',
            'ParticleSystem': '#9C27B0',
            'AnalyticsSystem': '#00BCD4',
            'SaveSystem': '#FFC107'
        };
        return colors[name] || '#888888';
    }
    
    receiveEvent(event) {
        this.receivedEvents.push({
            event: event,
            time: Date.now(),
            alpha: 1
        });
        
        // Keep only recent events
        const now = Date.now();
        this.receivedEvents = this.receivedEvents.filter(e => 
            now - e.time < 2000
        );
    }
    
    update(dt) {
        this.pulsePhase += dt * 2;
        
        // Update received events
        this.receivedEvents.forEach(e => {
            e.alpha = Math.max(0, e.alpha - dt);
        });
        
        // Remove old events
        this.receivedEvents = this.receivedEvents.filter(e => e.alpha > 0);
    }
    
    draw(ctx) {
        if (!this.active) {
            ctx.globalAlpha = 0.3;
        }
        
        // Draw pulse if receiving events
        if (this.receivedEvents.length > 0) {
            const pulseSize = Math.sin(this.pulsePhase) * 10 + 5;
            ctx.fillStyle = this.color + '33';
            ctx.fillRect(
                this.x - pulseSize,
                this.y - pulseSize,
                this.width + pulseSize * 2,
                this.height + pulseSize * 2
            );
        }
        
        // Draw system box
        ctx.fillStyle = this.active ? this.color : '#444444';
        ctx.fillRect(this.x, this.y, this.width, this.height);
        
        ctx.strokeStyle = this.active ? '#ffffff' : '#666666';
        ctx.lineWidth = 2;
        ctx.strokeRect(this.x, this.y, this.width, this.height);
        
        // Draw name
        ctx.fillStyle = '#ffffff';
        ctx.font = '12px Arial';
        ctx.textAlign = 'center';
        ctx.textBaseline = 'middle';
        ctx.fillText(this.name, this.x + this.width/2, this.y + this.height/2);
        
        // Draw event count
        if (this.receivedEvents.length > 0) {
            ctx.fillStyle = '#ffff00';
            ctx.font = '10px Arial';
            ctx.fillText(`(${this.receivedEvents.length})`, this.x + this.width/2, this.y + this.height + 15);
        }
        
        ctx.globalAlpha = 1;
    }
}

// Event Bus Visual
class EventBusVisual {
    constructor(x, y, width, height) {
        this.x = x;
        this.y = y;
        this.width = width;
        this.height = height;
        this.events = [];
        this.queuedEvents = [];
        this.pulsePhase = 0;
    }
    
    addEvent(event) {
        if (window.queueMode === 'queued' || window.queueMode === 'priority') {
            this.queuedEvents.push(event);
            if (window.queueMode === 'priority') {
                this.queuedEvents.sort((a, b) => a.priority - b.priority);
            }
        } else {
            this.events.push(event);
        }
    }
    
    processQueue(dt) {
        if (this.queuedEvents.length > 0 && Math.random() < dt * 2) {
            const event = this.queuedEvents.shift();
            this.events.push(event);
        }
    }
    
    update(dt) {
        this.pulsePhase += dt * 3;
        this.processQueue(dt);
    }
    
    draw(ctx) {
        // Draw bus background
        const gradient = ctx.createLinearGradient(this.x, this.y, this.x, this.y + this.height);
        gradient.addColorStop(0, 'rgba(0, 100, 200, 0.2)');
        gradient.addColorStop(1, 'rgba(0, 50, 100, 0.2)');
        ctx.fillStyle = gradient;
        ctx.fillRect(this.x, this.y, this.width, this.height);
        
        // Draw border with pulse
        const pulse = Math.sin(this.pulsePhase) * 0.5 + 0.5;
        ctx.strokeStyle = `rgba(0, 200, 255, ${0.5 + pulse * 0.5})`;
        ctx.lineWidth = 2;
        ctx.strokeRect(this.x, this.y, this.width, this.height);
        
        // Draw label
        ctx.fillStyle = '#ffffff';
        ctx.font = '14px Arial';
        ctx.textAlign = 'center';
        ctx.fillText('Event Bus', this.x + this.width/2, this.y - 10);
        
        // Draw queue size
        if (this.queuedEvents.length > 0) {
            ctx.fillStyle = '#ffff00';
            ctx.font = '12px Arial';
            ctx.fillText(`Queue: ${this.queuedEvents.length}`, this.x + this.width/2, this.y + this.height + 20);
        }
    }
}

// Event System Manager
class EventSystemManager {
    constructor(canvas, ctx) {
        this.canvas = canvas;
        this.ctx = ctx;
        this.eventBus = new EventBusVisual(250, 180, 100, 40);
        this.systems = [];
        this.events = [];
        this.eventCount = 0;
        this.eventLog = [];
        
        this.initializeSystems();
    }
    
    initializeSystems() {
        // Create system nodes in a circle around the event bus
        const systemNames = ['AudioSystem', 'UISystem', 'AchievementSystem', 
                           'ParticleSystem', 'AnalyticsSystem', 'SaveSystem'];
        const centerX = 300;
        const centerY = 200;
        const radius = 150;
        
        systemNames.forEach((name, i) => {
            const angle = (i / systemNames.length) * Math.PI * 2 - Math.PI / 2;
            const x = centerX + Math.cos(angle) * radius - 50;
            const y = centerY + Math.sin(angle) * radius - 20;
            this.systems.push(new SystemNode(name, x, y));
        });
    }
    
    emitEvent(type) {
        const event = new GameEvent(type);
        this.eventCount++;
        
        // Create visual at emit position (left side)
        const eventVisual = new EventVisual(event, 50, 200);
        
        // Move to event bus
        eventVisual.moveTo(300, 200);
        
        this.events.push(eventVisual);
        this.eventBus.addEvent(event);
        
        // Log event
        this.logEvent(`Emitted: ${type}`, event.id);
        
        // Schedule delivery to subscribers
        setTimeout(() => {
            this.deliverEvent(eventVisual);
        }, 1000 / window.eventSpeed);
        
        this.updateDisplays();
    }
    
    deliverEvent(eventVisual) {
        // Deliver to active systems
        const activeSystems = this.systems.filter(s => s.active);
        
        activeSystems.forEach((system, i) => {
            setTimeout(() => {
                // Clone visual for each system
                const clone = new EventVisual(eventVisual.event, eventVisual.x, eventVisual.y);
                clone.moveTo(system.x + system.width/2, system.y + system.height/2);
                this.events.push(clone);
                
                system.receiveEvent(eventVisual.event);
                this.logEvent(`  → ${system.name}`, eventVisual.event.id);
            }, i * 100 / window.eventSpeed);
        });
    }
    
    toggleSubscription(systemName) {
        const system = this.systems.find(s => s.name === systemName);
        if (system) {
            system.active = !system.active;
            this.logEvent(system.active ? 
                `${systemName} subscribed` : 
                `${systemName} unsubscribed`);
        }
    }
    
    logEvent(message, eventId = null) {
        const timestamp = new Date().toLocaleTimeString();
        const logEntry = `[${timestamp}] ${message}`;
        this.eventLog.unshift(logEntry);
        
        // Keep only recent logs
        if (this.eventLog.length > 10) {
            this.eventLog.pop();
        }
        
        this.updateLogDisplay();
    }
    
    updateLogDisplay() {
        const logDiv = document.getElementById('eventLog');
        if (logDiv) {
            logDiv.innerHTML = this.eventLog.join('<br>');
        }
    }
    
    updateDisplays() {
        document.getElementById('eventCount').textContent = this.eventCount;
        document.getElementById('queueSize').textContent = this.eventBus.queuedEvents.length;
    }
    
    update(dt) {
        // Update event bus
        this.eventBus.update(dt);
        
        // Update systems
        this.systems.forEach(system => system.update(dt));
        
        // Update events
        this.events.forEach(event => event.update(dt));
        
        // Remove dead events
        this.events = this.events.filter(e => e.alpha > 0);
        
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
        
        // Draw connections from bus to systems
        this.ctx.strokeStyle = 'rgba(255, 255, 255, 0.1)';
        this.ctx.lineWidth = 1;
        this.systems.forEach(system => {
            if (system.active) {
                this.ctx.beginPath();
                this.ctx.moveTo(300, 200);
                this.ctx.lineTo(system.x + system.width/2, system.y + system.height/2);
                this.ctx.stroke();
            }
        });
        
        // Draw event bus
        this.eventBus.draw(this.ctx);
        
        // Draw systems
        this.systems.forEach(system => system.draw(this.ctx));
        
        // Draw events
        this.events.forEach(event => event.draw(this.ctx));
        
        // Draw labels
        this.ctx.fillStyle = '#ffffff';
        this.ctx.font = '12px Arial';
        this.ctx.textAlign = 'left';
        this.ctx.fillText('Publisher', 20, 190);
        
        // Draw queue mode
        this.ctx.textAlign = 'center';
        this.ctx.fillText(`Mode: ${window.queueMode}`, 300, 250);
    }
}

// Initialize
const eventCanvas = document.getElementById('eventCanvas');
const ctx = eventCanvas.getContext('2d');
const eventSystem = new EventSystemManager(eventCanvas, ctx);

// Global settings
window.queueMode = 'immediate';
window.eventSpeed = 1;

// Global functions
window.emitEvent = function(type) {
    eventSystem.emitEvent(type);
};

window.toggleSubscription = function(systemName) {
    eventSystem.toggleSubscription(systemName);
};

window.setQueueMode = function(mode) {
    window.queueMode = mode;
    eventSystem.logEvent(`Queue mode: ${mode}`);
};

window.setEventSpeed = function(speed) {
    window.eventSpeed = parseFloat(speed);
};

// Animation loop
let lastTime = performance.now();

function animate(currentTime) {
    const dt = (currentTime - lastTime) / 1000;
    lastTime = currentTime;
    
    eventSystem.update(dt);
    eventSystem.draw();
    
    requestAnimationFrame(animate);
}

// Start animation
animate(performance.now());

console.log('Event System Visualizer initialized successfully!');