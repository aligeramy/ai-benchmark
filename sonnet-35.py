import pygame
import math
import sys
from pygame import Vector2

# Initialize Pygame
pygame.init()

# Constants
WIDTH = 800
HEIGHT = 600
FPS = 60
GRAVITY = 0.5
FRICTION = 0.98
BALL_RADIUS = 15
HEXAGON_RADIUS = 200
ROTATION_SPEED = 0.5  # degrees per frame

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bouncing Ball in Rotating Hexagon")
clock = pygame.time.Clock()

class Ball:
    def __init__(self):
        self.pos = Vector2(WIDTH // 2, HEIGHT // 2)
        self.vel = Vector2(5, 0)
        self.radius = BALL_RADIUS

    def update(self):
        # Apply gravity
        self.vel.y += GRAVITY
        
        # Apply friction
        self.vel *= FRICTION
        
        # Update position
        self.pos += self.vel

    def draw(self):
        pygame.draw.circle(screen, RED, (int(self.pos.x), int(self.pos.y)), self.radius)

class Hexagon:
    def __init__(self):
        self.center = Vector2(WIDTH // 2, HEIGHT // 2)
        self.radius = HEXAGON_RADIUS
        self.rotation = 0
        self.vertices = self.calculate_vertices()

    def calculate_vertices(self):
        vertices = []
        for i in range(6):
            angle = math.radians(self.rotation + i * 60)
            x = self.center.x + self.radius * math.cos(angle)
            y = self.center.y + self.radius * math.sin(angle)
            vertices.append(Vector2(x, y))
        return vertices

    def update(self):
        self.rotation += ROTATION_SPEED
        self.vertices = self.calculate_vertices()

    def draw(self):
        # Draw the hexagon
        vertices = [(int(v.x), int(v.y)) for v in self.vertices]
        pygame.draw.polygon(screen, WHITE, vertices, 2)

def check_collision(ball, hexagon):
    for i in range(6):
        # Get two consecutive vertices to form a line segment
        p1 = hexagon.vertices[i]
        p2 = hexagon.vertices[(i + 1) % 6]
        
        # Vector from p1 to p2
        wall = p2 - p1
        # Vector from p1 to ball
        to_ball = ball.pos - p1
        
        # Project ball's position onto the wall vector
        wall_length = wall.length()
        if wall_length == 0:
            continue
            
        wall_normalized = wall / wall_length
        projection_length = to_ball.dot(wall_normalized)
        
        # Find closest point on wall to ball
        if projection_length < 0:
            closest = Vector2(p1)
        elif projection_length > wall_length:
            closest = Vector2(p2)
        else:
            closest = p1 + wall_normalized * projection_length
        
        # Check if ball collides with the line segment
        distance = (ball.pos - closest).length()
        if distance < ball.radius:
            # Calculate normal vector
            normal = (ball.pos - closest).normalize()
            
            # Move ball out of collision
            ball.pos = closest + normal * ball.radius
            
            # Reflect velocity vector
            ball.vel = ball.vel.reflect(normal) * 0.8  # Add some energy loss

def main():
    ball = Ball()
    hexagon = Hexagon()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Update
        ball.update()
        hexagon.update()
        check_collision(ball, hexagon)

        # Draw
        screen.fill(BLACK)
        hexagon.draw()
        ball.draw()
        
        # Update display
        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()
