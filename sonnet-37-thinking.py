import pygame
import sys
import math
from pygame.locals import *
import random

# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GRAVITY = 0.5
FRICTION = 0.99
BALL_RADIUS = 15
HEX_RADIUS = 200
HEX_ROTATION_SPEED = 0.5  # degrees per frame

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ball Bouncing in a Spinning Hexagon")
clock = pygame.time.Clock()

class Ball:
    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.radius = radius
        self.vx = 0
        self.vy = 0
        self.color = RED
    
    def update(self):
        # Apply gravity
        self.vy += GRAVITY
        
        # Apply friction
        self.vx *= FRICTION
        self.vy *= FRICTION
        
        # Update position
        self.x += self.vx
        self.y += self.vy
    
    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.radius)

class Hexagon:
    def __init__(self, center_x, center_y, radius):
        self.center_x = center_x
        self.center_y = center_y
        self.radius = radius
        self.rotation = 0
        self.rotation_speed = HEX_ROTATION_SPEED
        self.color = BLUE
        self.vertices = self.calculate_vertices()
        
    def calculate_vertices(self):
        vertices = []
        for i in range(6):
            angle_rad = math.radians(self.rotation + i * 60)
            x = self.center_x + self.radius * math.cos(angle_rad)
            y = self.center_y + self.radius * math.sin(angle_rad)
            vertices.append((x, y))
        return vertices
    
    def update(self):
        self.rotation += self.rotation_speed
        self.vertices = self.calculate_vertices()
    
    def draw(self, surface):
        pygame.draw.polygon(surface, self.color, self.vertices, 3)

def get_line_equation(p1, p2):
    """Return A, B, C for line equation Ax + By + C = 0"""
    A = p2[1] - p1[1]  # y2 - y1
    B = p1[0] - p2[0]  # x1 - x2
    C = p2[0] * p1[1] - p1[0] * p2[1]  # x2*y1 - x1*y2
    return A, B, C

def distance_to_line(point, line_params):
    """Calculate distance from a point to a line given by Ax + By + C = 0"""
    A, B, C = line_params
    x, y = point
    return abs(A * x + B * y + C) / math.sqrt(A**2 + B**2)

def check_collision(ball, hexagon):
    """Check collision between ball and hexagon sides"""
    for i in range(6):
        # Get the hexagon side (line segment)
        p1 = hexagon.vertices[i]
        p2 = hexagon.vertices[(i + 1) % 6]
        
        # Get line equation parameters
        line_params = get_line_equation(p1, p2)
        
        # Calculate distance to line
        dist = distance_to_line((ball.x, ball.y), line_params)
        
        # Check if collision with line
        if dist <= ball.radius:
            # Project ball's position onto the line
            A, B, C = line_params
            
            # Check if point is between endpoints (on the segment)
            # Vector from p1 to p2
            v_line = (p2[0] - p1[0], p2[1] - p1[1])
            # Vector from p1 to ball
            v_ball = (ball.x - p1[0], ball.y - p1[1])
            
            # Dot product to determine if ball is within segment endpoints
            dot_product = v_line[0] * v_ball[0] + v_line[1] * v_ball[1]
            line_length_squared = v_line[0]**2 + v_line[1]**2
            
            if 0 <= dot_product <= line_length_squared:
                # Normal vector to the line (normalized)
                normal = (A / math.sqrt(A**2 + B**2), B / math.sqrt(A**2 + B**2))
                
                # Calculate reflection of velocity vector
                dot_product_vel = ball.vx * normal[0] + ball.vy * normal[1]
                
                # Adjust position to prevent sticking
                overlap = ball.radius - dist
                ball.x += normal[0] * overlap
                ball.y += normal[1] * overlap
                
                # Bounce with some energy loss
                ball.vx = ball.vx - 2 * dot_product_vel * normal[0]
                ball.vy = ball.vy - 2 * dot_product_vel * normal[1]
                
                # Reduce velocity (energy loss in collision)
                ball.vx *= 0.8
                ball.vy *= 0.8
                
                return True
    return False

# Create ball and hexagon
ball = Ball(WIDTH // 2, HEIGHT // 3, BALL_RADIUS)
hexagon = Hexagon(WIDTH // 2, HEIGHT // 2, HEX_RADIUS)

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        elif event.type == KEYDOWN:
            if event.key == K_SPACE:
                # Reset the ball position
                ball.x = WIDTH // 2
                ball.y = HEIGHT // 3
                ball.vx = 0
                ball.vy = 0
            elif event.key == K_UP:
                # Increase hexagon rotation speed
                hexagon.rotation_speed += 0.1
            elif event.key == K_DOWN:
                # Decrease hexagon rotation speed
                hexagon.rotation_speed -= 0.1
            elif event.key == K_ESCAPE:
                # Quit the program
                running = False
    
    # Update
    ball.update()
    hexagon.update()
    
    # Check for collision
    check_collision(ball, hexagon)
    
    # Drawing
    screen.fill(BLACK)
    ball.draw(screen)
    hexagon.draw(screen)
    
    # Update the display
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit() 