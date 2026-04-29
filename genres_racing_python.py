"""
Racing Game Physics Implementation
A complete racing game with realistic physics, AI opponents, and multiple tracks
"""

import pygame
import math
import random
from typing import List, Tuple, Dict, Optional
from dataclasses import dataclass
from enum import Enum

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
FPS = 60

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GRAY = (128, 128, 128)
DARK_GRAY = (64, 64, 64)

class CarStats:
    """Car performance characteristics"""
    def __init__(self, name: str = "Default"):
        self.name = name
        self.max_speed = 250.0  # km/h
        self.acceleration = 150.0  # m/s²
        self.braking = 200.0  # m/s²
        self.handling = 2.5  # Turn rate
        self.weight = 1200.0  # kg
        self.drag_coefficient = 0.3
        self.downforce = 0.5
        
        # Tire characteristics
        self.tire_grip = 1.0
        self.optimal_slip_angle = 8.0  # degrees

@dataclass
class Vector2:
    """2D Vector for physics calculations"""
    x: float
    y: float
    
    def __add__(self, other):
        return Vector2(self.x + other.x, self.y + other.y)
    
    def __sub__(self, other):
        return Vector2(self.x - other.x, self.y - other.y)
    
    def __mul__(self, scalar):
        return Vector2(self.x * scalar, self.y * scalar)
    
    def magnitude(self):
        return math.sqrt(self.x ** 2 + self.y ** 2)
    
    def normalize(self):
        mag = self.magnitude()
        if mag > 0:
            return Vector2(self.x / mag, self.y / mag)
        return Vector2(0, 0)
    
    def dot(self, other):
        return self.x * other.x + self.y * other.y

class Car:
    """Racing car with physics simulation"""
    
    def __init__(self, x: float, y: float, color: Tuple[int, int, int], 
                 stats: CarStats = None):
        # Position and movement
        self.position = Vector2(x, y)
        self.velocity = Vector2(0, 0)
        self.angle = 0  # Heading angle in radians
        self.angular_velocity = 0
        
        # Car properties
        self.stats = stats if stats else CarStats()
        self.color = color
        self.width = 20
        self.length = 35
        
        # Control inputs
        self.throttle = 0  # -1 to 1
        self.brake = 0  # 0 to 1
        self.steering = 0  # -1 to 1
        self.handbrake = False
        self.nitro = False
        self.nitro_amount = 100.0
        
        # Physics state
        self.speed = 0
        self.slip_angle = 0
        self.drift_angle = 0
        self.lateral_velocity = 0
        self.longitudinal_velocity = 0
        
        # Tire state
        self.front_slip = 0
        self.rear_slip = 0
        self.tire_smoke = []
        
        # Race data
        self.lap = 0
        self.checkpoint = 0
        self.lap_times = []
        self.best_lap_time = None
        self.current_lap_time = 0
        
        # Visual effects
        self.skid_marks = []
        
    def update(self, dt: float):
        """Update car physics"""
        # Calculate forces
        self._update_forces(dt)
        
        # Update position
        self.position.x += self.velocity.x * dt
        self.position.y += self.velocity.y * dt
        
        # Update angle
        self.angle += self.angular_velocity * dt
        
        # Update visual effects
        self._update_effects(dt)
        
        # Update race time
        self.current_lap_time += dt
        
    def _update_forces(self, dt: float):
        """Calculate and apply forces"""
        # Get forward and right vectors
        forward = Vector2(math.cos(self.angle), math.sin(self.angle))
        right = Vector2(math.cos(self.angle + math.pi/2), 
                       math.sin(self.angle + math.pi/2))
        
        # Calculate current speed components
        self.longitudinal_velocity = self.velocity.dot(forward)
        self.lateral_velocity = self.velocity.dot(right)
        self.speed = self.velocity.magnitude()
        
        # Engine force
        engine_force = 0
        if self.throttle != 0:
            # Forward/reverse force
            engine_force = self.throttle * self.stats.acceleration
            
            # Apply nitro boost
            if self.nitro and self.nitro_amount > 0:
                engine_force *= 1.5
                self.nitro_amount -= dt * 30
                self.nitro_amount = max(0, self.nitro_amount)
        
        # Braking force
        if self.brake > 0:
            brake_force = -self.brake * self.stats.braking * \
                         math.copysign(1, self.longitudinal_velocity)
            engine_force += brake_force
        
        # Calculate traction
        if self.handbrake:
            rear_traction = 0.5
        else:
            # Traction based on slip angle
            self.slip_angle = math.atan2(self.lateral_velocity, 
                                        abs(self.longitudinal_velocity) + 0.1)
            rear_traction = max(0.6, 1.0 - abs(self.slip_angle) * 0.3)
        
        front_traction = max(0.8, 1.0 - abs(self.slip_angle) * 0.2)
        
        # Apply longitudinal force
        acceleration = forward * (engine_force * rear_traction)
        self.velocity = self.velocity + acceleration * dt
        
        # Drag force
        drag = self.velocity * (-self.stats.drag_coefficient * self.speed * 0.001)
        self.velocity = self.velocity + drag * dt
        
        # Friction/Rolling resistance
        if self.handbrake:
            friction_coeff = 0.88
        else:
            friction_coeff = 0.95
        
        self.velocity = self.velocity * math.pow(friction_coeff, dt)
        
        # Lateral forces (cornering)
        if abs(self.speed) > 5:
            # Steering influence
            steer_angle = self.steering * 0.5  # Max steering angle
            
            # Turn radius based on speed
            if abs(steer_angle) > 0.01:
                turn_radius = self.stats.weight / (abs(steer_angle) * self.stats.handling)
                self.angular_velocity = (self.speed / turn_radius) * math.copysign(1, steer_angle)
            else:
                self.angular_velocity *= 0.9  # Damping
            
            # Limit angular velocity at low speeds
            speed_factor = min(1.0, abs(self.speed) / 50)
            self.angular_velocity *= speed_factor
            
            # Apply lateral grip
            lateral_force = right * (-self.lateral_velocity * front_traction * 5)
            self.velocity = self.velocity + lateral_force * dt
        else:
            self.angular_velocity *= 0.8
        
        # Limit max speed
        if self.speed > self.stats.max_speed:
            self.velocity = self.velocity.normalize() * self.stats.max_speed
        
        # Recharge nitro
        if not self.nitro and self.nitro_amount < 100:
            self.nitro_amount += dt * 10
            self.nitro_amount = min(100, self.nitro_amount)
    
    def _update_effects(self, dt: float):
        """Update visual effects"""
        # Create skid marks when drifting
        if self.handbrake and abs(self.speed) > 30:
            self.skid_marks.append({
                'x': self.position.x - math.cos(self.angle) * self.length/2,
                'y': self.position.y - math.sin(self.angle) * self.length/2,
                'alpha': 1.0
            })
        
        # Fade old skid marks
        for mark in self.skid_marks:
            mark['alpha'] -= dt * 0.5
        
        # Remove faded marks
        self.skid_marks = [m for m in self.skid_marks if m['alpha'] > 0]
        
        # Limit skid marks
        if len(self.skid_marks) > 100:
            self.skid_marks.pop(0)
    
    def draw(self, screen: pygame.Surface, camera_x: float, camera_y: float):
        """Draw the car"""
        # Draw skid marks
        for mark in self.skid_marks:
            alpha = int(mark['alpha'] * 100)
            color = (50, 50, 50, alpha) if len(self.color) == 3 else (50, 50, 50)
            pygame.draw.circle(screen, color,
                             (int(mark['x'] - camera_x), int(mark['y'] - camera_y)),
                             3)
        
        # Create car surface
        car_surface = pygame.Surface((self.length, self.width), pygame.SRCALPHA)
        
        # Draw car body
        pygame.draw.rect(car_surface, self.color, (0, 0, self.length, self.width))
        
        # Draw windows
        window_color = (50, 50, 50)
        pygame.draw.rect(car_surface, window_color,
                        (self.length//4, self.width//4, self.length//2, self.width//2))
        
        # Draw headlights
        if self.nitro and self.nitro_amount > 0:
            headlight_color = (0, 255, 255)
        else:
            headlight_color = (255, 255, 200)
        
        pygame.draw.rect(car_surface, headlight_color,
                        (self.length - 5, 2, 5, self.width//3 - 2))
        pygame.draw.rect(car_surface, headlight_color,
                        (self.length - 5, self.width - self.width//3, 5, self.width//3 - 2))
        
        # Rotate car surface
        rotated = pygame.transform.rotate(car_surface, -math.degrees(self.angle))
        
        # Position on screen
        rect = rotated.get_rect()
        rect.center = (self.position.x - camera_x, self.position.y - camera_y)
        
        screen.blit(rotated, rect)
        
    def get_bounds(self) -> pygame.Rect:
        """Get car bounding box for collision"""
        return pygame.Rect(self.position.x - self.length/2,
                          self.position.y - self.width/2,
                          self.length, self.width)

class Track:
    """Race track with checkpoints and boundaries"""
    
    def __init__(self, name: str):
        self.name = name
        self.checkpoints = []
        self.walls = []
        self.start_positions = []
        self.track_surface = None
        
        self._build_track()
    
    def _build_track(self):
        """Build track layout"""
        if self.name == "Circuit":
            self._build_circuit()
        elif self.name == "Sprint":
            self._build_sprint()
        else:
            self._build_circuit()
    
    def _build_circuit(self):
        """Build a circuit track"""
        # Starting grid
        self.start_positions = [
            {'x': 400, 'y': 500, 'angle': 0},
            {'x': 430, 'y': 500, 'angle': 0},
            {'x': 400, 'y': 530, 'angle': 0},
            {'x': 430, 'y': 530, 'angle': 0}
        ]
        
        # Checkpoints
        self.checkpoints = [
            pygame.Rect(350, 480, 100, 60),  # Start/Finish
            pygame.Rect(650, 380, 60, 100),
            pygame.Rect(650, 180, 60, 100),
            pygame.Rect(400, 80, 100, 60),
            pygame.Rect(150, 180, 60, 100),
            pygame.Rect(150, 380, 60, 100)
        ]
        
        # Track walls
        self.walls = [
            # Outer walls
            pygame.Rect(50, 50, 700, 10),
            pygame.Rect(50, 540, 700, 10),
            pygame.Rect(50, 50, 10, 500),
            pygame.Rect(740, 50, 10, 500),
            
            # Inner walls
            pygame.Rect(200, 150, 350, 10),
            pygame.Rect(200, 440, 350, 10),
            pygame.Rect(200, 150, 10, 300),
            pygame.Rect(540, 150, 10, 300)
        ]
    
    def _build_sprint(self):
        """Build a sprint track"""
        # Starting grid
        self.start_positions = [
            {'x': 100, 'y': 300, 'angle': 0},
            {'x': 100, 'y': 330, 'angle': 0},
            {'x': 70, 'y': 300, 'angle': 0},
            {'x': 70, 'y': 330, 'angle': 0}
        ]
        
        # Checkpoints for straight track
        self.checkpoints = [
            pygame.Rect(50, 280, 80, 60),
            pygame.Rect(200, 280, 80, 60),
            pygame.Rect(400, 280, 80, 60),
            pygame.Rect(600, 280, 80, 60),
            pygame.Rect(800, 280, 80, 60)
        ]
        
        # Simple walls
        self.walls = [
            pygame.Rect(10, 250, 900, 10),
            pygame.Rect(10, 370, 900, 10)
        ]
    
    def check_checkpoint(self, car: Car) -> bool:
        """Check if car passed checkpoint"""
        if car.checkpoint < len(self.checkpoints):
            checkpoint = self.checkpoints[car.checkpoint]
            
            if checkpoint.collidepoint(car.position.x, car.position.y):
                car.checkpoint += 1
                
                # Lap completed
                if car.checkpoint >= len(self.checkpoints):
                    car.checkpoint = 0
                    car.lap += 1
                    
                    # Record lap time
                    if car.current_lap_time > 0:
                        car.lap_times.append(car.current_lap_time)
                        if car.best_lap_time is None or car.current_lap_time < car.best_lap_time:
                            car.best_lap_time = car.current_lap_time
                        car.current_lap_time = 0
                    
                    return True  # Lap completed
        
        return False
    
    def check_collision(self, car: Car) -> Optional[pygame.Rect]:
        """Check collision with track walls"""
        car_rect = car.get_bounds()
        
        for wall in self.walls:
            if car_rect.colliderect(wall):
                return wall
        
        return None
    
    def draw(self, screen: pygame.Surface, camera_x: float, camera_y: float):
        """Draw the track"""
        # Draw track surface (dark gray)
        screen.fill(DARK_GRAY)
        
        # Draw track boundaries
        for wall in self.walls:
            pygame.draw.rect(screen, GRAY,
                           (wall.x - camera_x, wall.y - camera_y,
                            wall.width, wall.height))
        
        # Draw checkpoints (debug view)
        for i, checkpoint in enumerate(self.checkpoints):
            color = YELLOW if i == 0 else (255, 255, 0, 50)
            
            # Start/finish line
            if i == 0:
                # Checkered pattern
                for x in range(0, checkpoint.width, 10):
                    for y in range(0, 10, 10):
                        if (x // 10 + y // 10) % 2 == 0:
                            pygame.draw.rect(screen, WHITE,
                                           (checkpoint.x + x - camera_x,
                                            checkpoint.y - camera_y,
                                            10, 10))

class AIDriver:
    """AI controller for computer-controlled cars"""
    
    def __init__(self, car: Car, track: Track, skill: float = 0.7):
        self.car = car
        self.track = track
        self.skill = skill  # 0.0 to 1.0
        self.target_checkpoint = 0
        self.racing_line = self._calculate_racing_line()
    
    def _calculate_racing_line(self) -> List[Vector2]:
        """Calculate optimal racing line"""
        # Simple racing line through checkpoint centers
        line = []
        for checkpoint in self.track.checkpoints:
            line.append(Vector2(checkpoint.centerx, checkpoint.centery))
        return line
    
    def update(self, dt: float):
        """Update AI car controls"""
        # Get target position
        target_idx = self.car.checkpoint % len(self.racing_line)
        target = self.racing_line[target_idx]
        
        # Calculate direction to target
        dx = target.x - self.car.position.x
        dy = target.y - self.car.position.y
        distance = math.sqrt(dx * dx + dy * dy)
        
        # Calculate target angle
        target_angle = math.atan2(dy, dx)
        
        # Calculate angle difference
        angle_diff = target_angle - self.car.angle
        
        # Normalize angle
        while angle_diff > math.pi:
            angle_diff -= 2 * math.pi
        while angle_diff < -math.pi:
            angle_diff += 2 * math.pi
        
        # Set steering based on angle difference
        self.car.steering = max(-1, min(1, angle_diff * 3)) * self.skill
        
        # Speed control
        target_speed = self._calculate_target_speed(distance, abs(angle_diff))
        
        if self.car.speed < target_speed:
            self.car.throttle = self.skill
            self.car.brake = 0
        else:
            self.car.throttle = 0
            self.car.brake = (self.car.speed - target_speed) / 100 * self.skill
        
        # Use handbrake for sharp turns
        self.car.handbrake = abs(angle_diff) > math.pi/3 and self.car.speed > 80
        
        # Use nitro on straights
        self.car.nitro = (abs(angle_diff) < 0.1 and distance > 200 and 
                         self.car.nitro_amount > 50 and random.random() < 0.01 * self.skill)
    
    def _calculate_target_speed(self, distance: float, angle_diff: float) -> float:
        """Calculate target speed based on conditions"""
        base_speed = self.car.stats.max_speed * self.skill
        
        # Reduce speed for turns
        turn_factor = max(0.3, 1.0 - abs(angle_diff) / math.pi)
        
        # Reduce speed when close to checkpoint
        distance_factor = min(1.0, distance / 200)
        
        return base_speed * turn_factor * distance_factor

class RaceManager:
    """Manages race logic and rules"""
    
    def __init__(self, track: Track, num_laps: int = 3):
        self.track = track
        self.num_laps = num_laps
        self.cars = []
        self.race_started = False
        self.race_finished = False
        self.race_time = 0
        self.standings = []
    
    def add_car(self, car: Car):
        """Add car to race"""
        self.cars.append(car)
    
    def start_race(self):
        """Start the race"""
        self.race_started = True
        self.race_time = 0
        
        for car in self.cars:
            car.lap = 0
            car.checkpoint = 0
            car.current_lap_time = 0
            car.lap_times = []
    
    def update(self, dt: float):
        """Update race state"""
        if not self.race_started:
            return
        
        self.race_time += dt
        
        # Check for race completion
        for car in self.cars:
            if car.lap >= self.num_laps:
                if not self.race_finished:
                    self.race_finished = True
                    self._calculate_final_standings()
        
        # Update standings
        self._update_standings()
    
    def _update_standings(self):
        """Update current race standings"""
        self.standings = sorted(self.cars, key=lambda c: (
            -c.lap,  # Higher lap count first
            -c.checkpoint,  # Higher checkpoint first
            c.current_lap_time  # Lower time first
        ))
    
    def _calculate_final_standings(self):
        """Calculate final race results"""
        # Sort by laps completed and total time
        self.standings = sorted(self.cars, key=lambda c: (
            -c.lap,
            sum(c.lap_times) if c.lap_times else float('inf')
        ))
    
    def get_position(self, car: Car) -> int:
        """Get car's current position"""
        try:
            return self.standings.index(car) + 1
        except (ValueError, IndexError):
            return len(self.cars)

class RacingGame:
    """Main racing game class"""
    
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Racing Game - Python Implementation")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        
        # Create track
        self.track = Track("Circuit")
        
        # Create race manager
        self.race_manager = RaceManager(self.track)
        
        # Create player car
        player_start = self.track.start_positions[0]
        self.player_car = Car(player_start['x'], player_start['y'], BLUE)
        self.player_car.angle = player_start['angle']
        self.race_manager.add_car(self.player_car)
        
        # Create AI cars
        self.ai_drivers = []
        ai_colors = [RED, GREEN, YELLOW]
        ai_skills = [0.9, 0.7, 0.5]
        
        for i in range(1, min(4, len(self.track.start_positions))):
            start = self.track.start_positions[i]
            ai_car = Car(start['x'], start['y'], ai_colors[i-1])
            ai_car.angle = start['angle']
            
            ai_driver = AIDriver(ai_car, self.track, ai_skills[i-1])
            self.ai_drivers.append(ai_driver)
            self.race_manager.add_car(ai_car)
        
        # Camera
        self.camera_x = 0
        self.camera_y = 0
        
        # Game state
        self.running = True
    
    def handle_input(self):
        """Handle player input"""
        keys = pygame.key.get_pressed()
        
        # Reset controls
        self.player_car.throttle = 0
        self.player_car.brake = 0
        self.player_car.steering = 0
        
        # Acceleration/Brake
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.player_car.throttle = 1.0
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.player_car.brake = 1.0
        
        # Steering
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.player_car.steering = -1.0
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.player_car.steering = 1.0
        
        # Handbrake
        self.player_car.handbrake = keys[pygame.K_SPACE]
        
        # Nitro
        self.player_car.nitro = keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]
    
    def update_camera(self):
        """Update camera to follow player"""
        # Smooth camera follow with look-ahead
        target_x = self.player_car.position.x - SCREEN_WIDTH / 2
        target_y = self.player_car.position.y - SCREEN_HEIGHT / 2
        
        # Add velocity-based look-ahead
        look_ahead_x = self.player_car.velocity.x * 0.5
        look_ahead_y = self.player_car.velocity.y * 0.5
        
        # Smooth interpolation
        self.camera_x += ((target_x + look_ahead_x) - self.camera_x) * 0.1
        self.camera_y += ((target_y + look_ahead_y) - self.camera_y) * 0.1
    
    def handle_collisions(self):
        """Handle all collision detection and response"""
        cars = self.race_manager.cars
        
        # Car vs Wall collisions
        for car in cars:
            wall = self.track.check_collision(car)
            if wall:
                # Simple bounce response
                car.velocity = car.velocity * -0.5
                
                # Push car away from wall
                car_center_x = car.position.x
                car_center_y = car.position.y
                wall_center_x = wall.centerx
                wall_center_y = wall.centery
                
                push_x = car_center_x - wall_center_x
                push_y = car_center_y - wall_center_y
                push_dist = math.sqrt(push_x ** 2 + push_y ** 2)
                
                if push_dist > 0:
                    car.position.x += (push_x / push_dist) * 5
                    car.position.y += (push_y / push_dist) * 5
        
        # Car vs Car collisions
        for i in range(len(cars)):
            for j in range(i + 1, len(cars)):
                car1 = cars[i]
                car2 = cars[j]
                
                # Check collision
                dx = car2.position.x - car1.position.x
                dy = car2.position.y - car1.position.y
                distance = math.sqrt(dx ** 2 + dy ** 2)
                min_distance = 35  # Approximate car size
                
                if distance < min_distance:
                    # Collision response
                    nx = dx / distance if distance > 0 else 1
                    ny = dy / distance if distance > 0 else 0
                    
                    # Separate cars
                    overlap = min_distance - distance
                    car1.position.x -= nx * overlap * 0.5
                    car1.position.y -= ny * overlap * 0.5
                    car2.position.x += nx * overlap * 0.5
                    car2.position.y += ny * overlap * 0.5
                    
                    # Exchange velocities (simplified)
                    relative_velocity_x = car2.velocity.x - car1.velocity.x
                    relative_velocity_y = car2.velocity.y - car1.velocity.y
                    impulse = (relative_velocity_x * nx + relative_velocity_y * ny) * 0.5
                    
                    car1.velocity.x += impulse * nx
                    car1.velocity.y += impulse * ny
                    car2.velocity.x -= impulse * nx
                    car2.velocity.y -= impulse * ny
    
    def draw_ui(self):
        """Draw user interface elements"""
        # Speed
        speed_text = self.font.render(f"Speed: {int(abs(self.player_car.speed))} km/h", 
                                     True, WHITE)
        self.screen.blit(speed_text, (10, 10))
        
        # Lap counter
        current_lap = min(self.player_car.lap + 1, self.race_manager.num_laps)
        lap_text = self.font.render(f"Lap: {current_lap}/{self.race_manager.num_laps}", 
                                    True, WHITE)
        self.screen.blit(lap_text, (10, 50))
        
        # Position
        position = self.race_manager.get_position(self.player_car)
        position_text = self.font.render(f"Position: {position}/{len(self.race_manager.cars)}", 
                                        True, WHITE)
        self.screen.blit(position_text, (10, 90))
        
        # Lap time
        lap_minutes = int(self.player_car.current_lap_time // 60)
        lap_seconds = self.player_car.current_lap_time % 60
        time_text = self.small_font.render(f"Lap Time: {lap_minutes:02d}:{lap_seconds:05.2f}", 
                                          True, WHITE)
        self.screen.blit(time_text, (10, 130))
        
        # Best lap
        if self.player_car.best_lap_time:
            best_minutes = int(self.player_car.best_lap_time // 60)
            best_seconds = self.player_car.best_lap_time % 60
            best_text = self.small_font.render(f"Best Lap: {best_minutes:02d}:{best_seconds:05.2f}", 
                                              True, YELLOW)
            self.screen.blit(best_text, (10, 160))
        
        # Nitro gauge
        nitro_width = int(self.player_car.nitro_amount * 2)
        pygame.draw.rect(self.screen, GRAY, (10, 200, 204, 24))
        pygame.draw.rect(self.screen, (0, 255, 255), (12, 202, nitro_width, 20))
        nitro_text = self.small_font.render("NITRO", True, WHITE)
        self.screen.blit(nitro_text, (220, 200))
        
        # Controls help
        if not self.race_manager.race_started:
            help_text = [
                "Press ENTER to Start Race",
                "Arrow Keys or WASD - Drive",
                "SPACE - Handbrake",
                "SHIFT - Nitro Boost",
                "ESC - Exit"
            ]
            
            y = SCREEN_HEIGHT // 2 - 60
            for line in help_text:
                text = self.font.render(line, True, WHITE)
                rect = text.get_rect(center=(SCREEN_WIDTH // 2, y))
                self.screen.blit(text, rect)
                y += 40
        
        # Race finished
        if self.race_manager.race_finished:
            finish_text = self.font.render("RACE FINISHED!", True, GREEN)
            rect = finish_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            self.screen.blit(finish_text, rect)
            
            # Show final position
            position = self.race_manager.get_position(self.player_car)
            pos_text = self.font.render(f"Final Position: {position}", True, WHITE)
            rect = pos_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
            self.screen.blit(pos_text, rect)
    
    def run(self):
        """Main game loop"""
        while self.running:
            dt = self.clock.tick(FPS) / 1000.0  # Convert to seconds
            
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        if not self.race_manager.race_started:
                            self.race_manager.start_race()
                    elif event.key == pygame.K_ESCAPE:
                        self.running = False
                    elif event.key == pygame.K_r:
                        # Reset race
                        self.__init__()
            
            # Update game state
            if self.race_manager.race_started:
                # Handle input
                self.handle_input()
                
                # Update AI
                for ai_driver in self.ai_drivers:
                    ai_driver.update(dt)
                
                # Update cars
                for car in self.race_manager.cars:
                    car.update(dt)
                
                # Check checkpoints
                for car in self.race_manager.cars:
                    self.track.check_checkpoint(car)
                
                # Handle collisions
                self.handle_collisions()
                
                # Update race manager
                self.race_manager.update(dt)
                
                # Update camera
                self.update_camera()
            
            # Draw everything
            self.track.draw(self.screen, self.camera_x, self.camera_y)
            
            # Draw cars (sorted by Y position for depth)
            cars_sorted = sorted(self.race_manager.cars, key=lambda c: c.position.y)
            for car in cars_sorted:
                car.draw(self.screen, self.camera_x, self.camera_y)
            
            # Draw UI
            self.draw_ui()
            
            # Update display
            pygame.display.flip()
        
        pygame.quit()

if __name__ == "__main__":
    game = RacingGame()
    game.run()
