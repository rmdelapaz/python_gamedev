console.log('ECS Visualizer starting...');

// Component Types
class Component {
    constructor() {
        this.enabled = true;
    }
}

class TransformComponent extends Component {
    constructor(x = 0, y = 0) {
        super();
        this.x = x;
        this.y = y;
        this.rotation = 0;
        this.scale = 1;
    }
}

class VelocityComponent extends Component {
    constructor(vx = 0, vy = 0) {
        super();
        this.vx = vx;
        this.vy = vy;
        this.friction = 0.98;
    }
}

class HealthComponent extends Component {
    constructor(maxHealth = 100) {
        super();
        this.maxHealth = maxHealth;
        this.currentHealth = maxHealth;
    }
    
    takeDamage(amount) {
        this.currentHealth = Math.max(0, this.currentHealth - amount);
    }
    
    heal(amount) {
        this.currentHealth = Math.min(this.maxHealth, this.currentHealth + amount);
    }
}

class SpriteComponent extends Component {
    constructor(color = '#ffffff', shape = 'circle', size = 10) {
        super();
        this.color = color;
        this.shape = shape;
        this.size = size;
    }
}

class ColliderComponent extends Component {
    constructor(radius = 10) {
        super();
        this.radius = radius;
        this.isColliding = false;
    }
}

class AIComponent extends Component {
    constructor(behavior = 'wander') {
        super();
        this.behavior = behavior;
        this.target = null;
        this.state = 'idle';
    }
}

class InputComponent extends Component {
    constructor() {
        super();
        this.keys = {};
        this.mouse = { x: 0, y: 0, pressed: false };
    }
}

class ParticleComponent extends Component {
    constructor(lifetime = 2) {
        super();
        this.lifetime = lifetime;
        this.age = 0;
        this.fadeRate = 1;
    }
}

// Entity class
class Entity {
    constructor(id) {
        this.id = id;
        this.components = new Map();
        this.active = true;
    }
    
    addComponent(component) {
        const componentType = component.constructor.name;
        this.components.set(componentType, component);
        return this;
    }
    
    getComponent(componentType) {
        return this.components.get(componentType);
    }
    
    hasComponent(componentType) {
        return this.components.has(componentType);
    }
    
    removeComponent(componentType) {
        this.components.delete(componentType);
    }
}

// System base class
class System {
    constructor() {
        this.requiredComponents = [];
    }
    
    update(entities, dt) {
        const validEntities = entities.filter(entity => 
            this.requiredComponents.every(comp => entity.hasComponent(comp))
        );
        
        this.process(validEntities, dt);
    }
    
    process(entities, dt) {
        // Override in derived systems
    }
}

// Movement System
class MovementSystem extends System {
    constructor() {
        super();
        this.requiredComponents = ['TransformComponent', 'VelocityComponent'];
    }
    
    process(entities, dt) {
        entities.forEach(entity => {
            const transform = entity.getComponent('TransformComponent');
            const velocity = entity.getComponent('VelocityComponent');
            
            if (transform && velocity) {
                transform.x += velocity.vx * dt;
                transform.y += velocity.vy * dt;
                
                // Apply friction
                velocity.vx *= velocity.friction;
                velocity.vy *= velocity.friction;
                
                // Bounce off walls
                if (transform.x < 20 || transform.x > 580) {
                    velocity.vx *= -1;
                    transform.x = Math.max(20, Math.min(580, transform.x));
                }
                if (transform.y < 20 || transform.y > 380) {
                    velocity.vy *= -1;
                    transform.y = Math.max(20, Math.min(380, transform.y));
                }
            }
        });
    }
}

// Render System
class RenderSystem extends System {
    constructor(ctx) {
        super();
        this.ctx = ctx;
        this.requiredComponents = ['TransformComponent', 'SpriteComponent'];
    }
    
    process(entities, dt) {
        entities.forEach(entity => {
            const transform = entity.getComponent('TransformComponent');
            const sprite = entity.getComponent('SpriteComponent');
            
            if (transform && sprite) {
                this.ctx.save();
                this.ctx.translate(transform.x, transform.y);
                this.ctx.rotate(transform.rotation);
                this.ctx.scale(transform.scale, transform.scale);
                
                this.ctx.fillStyle = sprite.color;
                this.ctx.strokeStyle = sprite.color;
                this.ctx.lineWidth = 2;
                
                switch(sprite.shape) {
                    case 'circle':
                        this.ctx.beginPath();
                        this.ctx.arc(0, 0, sprite.size, 0, Math.PI * 2);
                        this.ctx.fill();
                        break;
                    case 'square':
                        this.ctx.fillRect(-sprite.size, -sprite.size, sprite.size * 2, sprite.size * 2);
                        break;
                    case 'triangle':
                        this.ctx.beginPath();
                        this.ctx.moveTo(0, -sprite.size);
                        this.ctx.lineTo(-sprite.size, sprite.size);
                        this.ctx.lineTo(sprite.size, sprite.size);
                        this.ctx.closePath();
                        this.ctx.fill();
                        break;
                    case 'star':
                        this.drawStar(0, 0, 5, sprite.size, sprite.size * 0.5);
                        this.ctx.fill();
                        break;
                }
                
                this.ctx.restore();
                
                // Draw health bar if entity has health
                const health = entity.getComponent('HealthComponent');
                if (health) {
                    this.drawHealthBar(transform.x, transform.y - sprite.size - 10, health);
                }
                
                // Draw collision indicator
                const collider = entity.getComponent('ColliderComponent');
                if (collider && window.showComponents) {
                    this.ctx.strokeStyle = collider.isColliding ? '#ff0000' : 'rgba(255, 255, 255, 0.2)';
                    this.ctx.lineWidth = 1;
                    this.ctx.beginPath();
                    this.ctx.arc(transform.x, transform.y, collider.radius, 0, Math.PI * 2);
                    this.ctx.stroke();
                }
            }
        });
    }
    
    drawStar(cx, cy, spikes, outerRadius, innerRadius) {
        let rot = Math.PI / 2 * 3;
        let x = cx;
        let y = cy;
        const step = Math.PI / spikes;
        
        this.ctx.beginPath();
        this.ctx.moveTo(cx, cy - outerRadius);
        
        for (let i = 0; i < spikes; i++) {
            x = cx + Math.cos(rot) * outerRadius;
            y = cy + Math.sin(rot) * outerRadius;
            this.ctx.lineTo(x, y);
            rot += step;
            
            x = cx + Math.cos(rot) * innerRadius;
            y = cy + Math.sin(rot) * innerRadius;
            this.ctx.lineTo(x, y);
            rot += step;
        }
        
        this.ctx.lineTo(cx, cy - outerRadius);
        this.ctx.closePath();
    }
    
    drawHealthBar(x, y, health) {
        const width = 30;
        const height = 4;
        const percentage = health.currentHealth / health.maxHealth;
        
        // Background
        this.ctx.fillStyle = 'rgba(255, 0, 0, 0.3)';
        this.ctx.fillRect(x - width/2, y, width, height);
        
        // Health
        this.ctx.fillStyle = percentage > 0.3 ? '#00ff00' : '#ff0000';
        this.ctx.fillRect(x - width/2, y, width * percentage, height);
    }
}

// AI System
class AISystem extends System {
    constructor() {
        super();
        this.requiredComponents = ['TransformComponent', 'AIComponent'];
    }
    
    process(entities, dt) {
        entities.forEach(entity => {
            const transform = entity.getComponent('TransformComponent');
            const ai = entity.getComponent('AIComponent');
            const velocity = entity.getComponent('VelocityComponent');
            
            if (transform && ai && velocity) {
                switch(ai.behavior) {
                    case 'wander':
                        // Random movement
                        if (Math.random() < 0.02) {
                            velocity.vx += (Math.random() - 0.5) * 100;
                            velocity.vy += (Math.random() - 0.5) * 100;
                        }
                        break;
                    case 'seek':
                        // Move toward target
                        if (ai.target) {
                            const dx = ai.target.x - transform.x;
                            const dy = ai.target.y - transform.y;
                            const dist = Math.sqrt(dx * dx + dy * dy);
                            if (dist > 1) {
                                velocity.vx += (dx / dist) * 50 * dt;
                                velocity.vy += (dy / dist) * 50 * dt;
                            }
                        }
                        break;
                    case 'flee':
                        // Move away from target
                        if (ai.target) {
                            const dx = transform.x - ai.target.x;
                            const dy = transform.y - ai.target.y;
                            const dist = Math.sqrt(dx * dx + dy * dy);
                            if (dist > 1 && dist < 100) {
                                velocity.vx += (dx / dist) * 100 * dt;
                                velocity.vy += (dy / dist) * 100 * dt;
                            }
                        }
                        break;
                }
            }
        });
    }
}

// Particle System
class ParticleSystem extends System {
    constructor() {
        super();
        this.requiredComponents = ['ParticleComponent'];
    }
    
    process(entities, dt) {
        entities.forEach(entity => {
            const particle = entity.getComponent('ParticleComponent');
            const sprite = entity.getComponent('SpriteComponent');
            
            if (particle) {
                particle.age += dt;
                
                if (particle.age >= particle.lifetime) {
                    entity.active = false;
                }
                
                // Fade out
                if (sprite) {
                    const alpha = 1 - (particle.age / particle.lifetime);
                    const rgb = sprite.color.match(/\d+/g);
                    if (rgb) {
                        sprite.color = `rgba(${rgb[0]}, ${rgb[1]}, ${rgb[2]}, ${alpha})`;
                    }
                }
            }
        });
    }
}

// Collision System
class CollisionSystem extends System {
    constructor() {
        super();
        this.requiredComponents = ['TransformComponent', 'ColliderComponent'];
    }
    
    process(entities, dt) {
        // Reset collision states
        entities.forEach(entity => {
            const collider = entity.getComponent('ColliderComponent');
            if (collider) collider.isColliding = false;
        });
        
        // Check collisions
        for (let i = 0; i < entities.length; i++) {
            for (let j = i + 1; j < entities.length; j++) {
                this.checkCollision(entities[i], entities[j]);
            }
        }
    }
    
    checkCollision(entity1, entity2) {
        const transform1 = entity1.getComponent('TransformComponent');
        const transform2 = entity2.getComponent('TransformComponent');
        const collider1 = entity1.getComponent('ColliderComponent');
        const collider2 = entity2.getComponent('ColliderComponent');
        
        if (transform1 && transform2 && collider1 && collider2) {
            const dx = transform2.x - transform1.x;
            const dy = transform2.y - transform1.y;
            const distance = Math.sqrt(dx * dx + dy * dy);
            
            if (distance < collider1.radius + collider2.radius) {
                collider1.isColliding = true;
                collider2.isColliding = true;
                
                // Separate entities
                const overlap = collider1.radius + collider2.radius - distance;
                const separationX = (dx / distance) * overlap * 0.5;
                const separationY = (dy / distance) * overlap * 0.5;
                
                transform1.x -= separationX;
                transform1.y -= separationY;
                transform2.x += separationX;
                transform2.y += separationY;
            }
        }
    }
}

// ECS World
class World {
    constructor(canvas, ctx) {
        this.canvas = canvas;
        this.ctx = ctx;
        this.entities = [];
        this.systems = [];
        this.nextEntityId = 0;
        
        // Initialize systems
        this.movementSystem = new MovementSystem();
        this.renderSystem = new RenderSystem(ctx);
        this.aiSystem = new AISystem();
        this.particleSystem = new ParticleSystem();
        this.collisionSystem = new CollisionSystem();
        
        this.systems.push(this.movementSystem);
        this.systems.push(this.collisionSystem);
        this.systems.push(this.aiSystem);
        this.systems.push(this.particleSystem);
        this.systems.push(this.renderSystem);
    }
    
    createEntity() {
        const entity = new Entity(this.nextEntityId++);
        this.entities.push(entity);
        return entity;
    }
    
    removeEntity(entity) {
        const index = this.entities.indexOf(entity);
        if (index > -1) {
            this.entities.splice(index, 1);
        }
    }
    
    update(dt) {
        // Remove inactive entities
        this.entities = this.entities.filter(e => e.active);
        
        // Update all systems
        this.systems.forEach(system => {
            system.update(this.entities, dt);
        });
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
        
        // Component labels if enabled
        if (window.showComponents) {
            this.drawComponentLabels();
        }
    }
    
    drawComponentLabels() {
        this.ctx.fillStyle = 'rgba(255, 255, 255, 0.7)';
        this.ctx.font = '10px Arial';
        
        this.entities.forEach(entity => {
            const transform = entity.getComponent('TransformComponent');
            if (transform) {
                const components = Array.from(entity.components.keys())
                    .map(c => c.replace('Component', ''))
                    .join(', ');
                
                this.ctx.fillText(
                    `[${components}]`,
                    transform.x - 30,
                    transform.y + 30
                );
            }
        });
    }
}

// Initialize ECS
const ecsCanvas = document.getElementById('ecsCanvas');
const ctx = ecsCanvas.getContext('2d');
const world = new World(ecsCanvas, ctx);

window.showSystems = true;
window.showComponents = true;

// Entity factory functions
window.createEntity = function(type) {
    let entity;
    
    switch(type) {
        case 'player':
            entity = world.createEntity();
            entity.addComponent(new TransformComponent(300, 200))
                  .addComponent(new VelocityComponent(0, 0))
                  .addComponent(new SpriteComponent('#00ff00', 'triangle', 15))
                  .addComponent(new HealthComponent(100))
                  .addComponent(new ColliderComponent(15))
                  .addComponent(new InputComponent());
            break;
            
        case 'enemy':
            entity = world.createEntity();
            entity.addComponent(new TransformComponent(
                Math.random() * 500 + 50,
                Math.random() * 300 + 50
            ))
            .addComponent(new VelocityComponent(
                (Math.random() - 0.5) * 100,
                (Math.random() - 0.5) * 100
            ))
            .addComponent(new SpriteComponent('#ff0000', 'square', 12))
            .addComponent(new HealthComponent(50))
            .addComponent(new ColliderComponent(12))
            .addComponent(new AIComponent('wander'));
            break;
            
        case 'powerup':
            entity = world.createEntity();
            entity.addComponent(new TransformComponent(
                Math.random() * 500 + 50,
                Math.random() * 300 + 50
            ))
            .addComponent(new SpriteComponent('#ffff00', 'star', 10))
            .addComponent(new ColliderComponent(10));
            // Slow rotation
            const transform = entity.getComponent('TransformComponent');
            setInterval(() => {
                if (transform) transform.rotation += 0.02;
            }, 16);
            break;
            
        case 'particle':
            entity = world.createEntity();
            entity.addComponent(new TransformComponent(
                Math.random() * 500 + 50,
                Math.random() * 300 + 50
            ))
            .addComponent(new VelocityComponent(
                (Math.random() - 0.5) * 200,
                (Math.random() - 0.5) * 200
            ))
            .addComponent(new SpriteComponent(
                `rgb(${Math.random() * 255}, ${Math.random() * 255}, ${Math.random() * 255})`,
                'circle',
                Math.random() * 5 + 2
            ))
            .addComponent(new ParticleComponent(Math.random() * 2 + 1));
            break;
    }
    
    updateEntityCount();
}

window.createCustomEntity = function() {
    const entity = world.createEntity();
    
    // Always add transform
    entity.addComponent(new TransformComponent(
        Math.random() * 500 + 50,
        Math.random() * 300 + 50
    ));
    
    // Add selected components
    if (document.getElementById('comp-velocity').checked) {
        entity.addComponent(new VelocityComponent(
            (Math.random() - 0.5) * 150,
            (Math.random() - 0.5) * 150
        ));
    }
    
    if (document.getElementById('comp-health').checked) {
        entity.addComponent(new HealthComponent(75));
    }
    
    if (document.getElementById('comp-sprite').checked) {
        const shapes = ['circle', 'square', 'triangle', 'star'];
        entity.addComponent(new SpriteComponent(
            `rgb(${Math.random() * 255}, ${Math.random() * 255}, ${Math.random() * 255})`,
            shapes[Math.floor(Math.random() * shapes.length)],
            Math.random() * 10 + 8
        ));
    }
    
    if (document.getElementById('comp-collider').checked) {
        entity.addComponent(new ColliderComponent(10));
    }
    
    if (document.getElementById('comp-ai').checked) {
        const behaviors = ['wander', 'seek', 'flee'];
        entity.addComponent(new AIComponent(
            behaviors[Math.floor(Math.random() * behaviors.length)]
        ));
    }
    
    if (document.getElementById('comp-input').checked) {
        entity.addComponent(new InputComponent());
    }
    
    if (document.getElementById('comp-particle').checked) {
        entity.addComponent(new ParticleComponent(3));
    }
    
    updateEntityCount();
}

window.clearAllEntities = function() {
    world.entities = [];
    updateEntityCount();
}

window.toggleSystems = function() {
    window.showSystems = document.getElementById('showSystems').checked;
    updateSystemsDisplay();
}

window.toggleComponents = function() {
    window.showComponents = document.getElementById('showComponents').checked;
}

function updateEntityCount() {
    document.getElementById('entityCount').textContent = world.entities.length;
}

function updateSystemsDisplay() {
    const display = document.getElementById('activeSystems');
    if (window.showSystems) {
        const systemNames = world.systems.map(s => s.constructor.name.replace('System', '')).join(', ');
        display.textContent = systemNames;
    } else {
        display.textContent = 'Hidden';
    }
}

// Animation loop
let lastTime = performance.now();
let frameCount = 0;
let fpsTime = 0;

function animate(currentTime) {
    const dt = (currentTime - lastTime) / 1000;
    lastTime = currentTime;
    
    // Update FPS
    frameCount++;
    fpsTime += dt;
    if (fpsTime >= 1) {
        document.getElementById('fpsDisplay').textContent = Math.round(frameCount / fpsTime);
        frameCount = 0;
        fpsTime = 0;
    }
    
    // Update and draw
    world.update(dt);
    world.draw();
    
    requestAnimationFrame(animate);
}

// Create some initial entities
window.createEntity('player');
window.createEntity('enemy');
window.createEntity('enemy');
window.createEntity('powerup');

// Initialize displays
updateSystemsDisplay();

// Start animation
animate(performance.now());

console.log('ECS Visualizer initialized successfully!');