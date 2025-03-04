import pygame
import sys
import math
import numpy as np

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ball Bouncing in a Spinning Hexagon")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Physics parameters
GRAVITY = 0.5
FRICTION = 0.98
RESTITUTION = 0.8  # Bounciness

# Ball properties
ball_radius = 15
ball_pos = np.array([WIDTH // 2, HEIGHT // 3], dtype=float)
ball_vel = np.array([2.0, 0.0], dtype=float)

# Hexagon properties
hexagon_radius = 200
hexagon_center = np.array([WIDTH // 2, HEIGHT // 2])
hexagon_rotation = 0
hexagon_rotation_speed = 0.01

# Clock for controlling frame rate
clock = pygame.time.Clock()

def rotate_point(point, center, angle):
    """Rotate a point around a center by an angle (in radians)"""
    s, c = math.sin(angle), math.cos(angle)
    point = point - center
    rotated_point = np.array([
        point[0] * c - point[1] * s,
        point[0] * s + point[1] * c
    ])
    return rotated_point + center

def get_hexagon_vertices():
    """Get the vertices of the hexagon after rotation"""
    vertices = []
    for i in range(6):
        angle = hexagon_rotation + i * (2 * math.pi / 6)
        x = hexagon_center[0] + hexagon_radius * math.cos(angle)
        y = hexagon_center[1] + hexagon_radius * math.sin(angle)
        vertices.append(np.array([x, y]))
    return vertices

def get_hexagon_edges():
    """Get the edges (line segments) of the hexagon"""
    vertices = get_hexagon_vertices()
    edges = []
    for i in range(6):
        edges.append((vertices[i], vertices[(i + 1) % 6]))
    return edges

def distance_point_to_line(point, line_start, line_end):
    """Calculate the distance from a point to a line segment"""
    line_vec = line_end - line_start
    point_vec = point - line_start
    line_len = np.linalg.norm(line_vec)
    line_unitvec = line_vec / line_len
    point_vec_scaled = point_vec / line_len
    t = np.clip(np.dot(line_unitvec, point_vec_scaled), 0, 1)
    nearest = line_start + t * line_vec
    dist = np.linalg.norm(nearest - point)
    return dist, nearest

def reflect_velocity(velocity, normal):
    """Reflect velocity vector across a normal vector"""
    normal = normal / np.linalg.norm(normal)  # Ensure normal is a unit vector
    return velocity - 2 * np.dot(velocity, normal) * normal

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_SPACE:
                # Reset ball position
                ball_pos = np.array([WIDTH // 2, HEIGHT // 3], dtype=float)
                ball_vel = np.array([2.0, 0.0], dtype=float)
            elif event.key == pygame.K_UP:
                hexagon_rotation_speed += 0.005
            elif event.key == pygame.K_DOWN:
                hexagon_rotation_speed -= 0.005

    # Update hexagon rotation
    hexagon_rotation += hexagon_rotation_speed

    # Apply gravity to ball velocity
    ball_vel[1] += GRAVITY

    # Update ball position
    ball_pos += ball_vel

    # Check for collisions with hexagon edges
    edges = get_hexagon_edges()
    for edge_start, edge_end in edges:
        distance, nearest = distance_point_to_line(ball_pos, edge_start, edge_end)
        
        if distance <= ball_radius:
            # Calculate normal vector (perpendicular to the edge)
            edge_vec = edge_end - edge_start
            normal = np.array([-edge_vec[1], edge_vec[0]])
            normal = normal / np.linalg.norm(normal)
            
            # Make sure normal points toward the ball
            if np.dot(normal, ball_pos - nearest) < 0:
                normal = -normal
                
            # Move ball outside the edge
            overlap = ball_radius - distance
            ball_pos += overlap * normal
            
            # Reflect velocity with some energy loss
            ball_vel = reflect_velocity(ball_vel, normal) * RESTITUTION
            
            # Apply friction to the component of velocity parallel to the edge
            parallel = np.array([normal[1], -normal[0]])
            parallel_component = np.dot(ball_vel, parallel) * parallel
            perpendicular_component = ball_vel - parallel_component
            ball_vel = perpendicular_component + parallel_component * FRICTION

    # Clear the screen
    screen.fill(BLACK)
    
    # Draw the hexagon
    vertices = get_hexagon_vertices()
    pygame.draw.polygon(screen, WHITE, vertices, 2)
    
    # Draw the ball
    pygame.draw.circle(screen, RED, ball_pos.astype(int), ball_radius)
    
    # Update the display
    pygame.display.flip()
    
    # Cap the frame rate
    clock.tick(60)

pygame.quit()
sys.exit() 