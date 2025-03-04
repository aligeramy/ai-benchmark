import pygame
import math

# -----------------------------------------------------------------------------
# Constants
# -----------------------------------------------------------------------------
WIDTH, HEIGHT = 800, 600      # Screen dimensions
FPS = 60                      # Frames per second

HEX_RADIUS = 150             # "Radius" of the hexagon (distance from center to a vertex)
HEX_ROTATION_SPEED = 0.01    # Speed of hexagon rotation (in radians per frame)

GRAVITY = 0.2                # Gravitational acceleration
FRICTION = 0.0005            # A simple friction factor
RESTITUTION = 0.9            # Bounciness of collisions

BALL_RADIUS = 15
INIT_BALL_POS = (WIDTH // 2, HEIGHT // 4)
INIT_BALL_VEL = (1, 0)

# -----------------------------------------------------------------------------
# Helper Functions
# -----------------------------------------------------------------------------
def rotate_point(px, py, cx, cy, angle):
    """
    Rotate point (px, py) around center (cx, cy) by 'angle' radians.
    Returns the rotated point (rx, ry).
    """
    # Translate point to origin (based on center)
    temp_x = px - cx
    temp_y = py - cy

    # Apply rotation
    rotated_x = temp_x * math.cos(angle) - temp_y * math.sin(angle)
    rotated_y = temp_x * math.sin(angle) + temp_y * math.cos(angle)

    # Translate back
    rx = rotated_x + cx
    ry = rotated_y + cy
    return rx, ry

def create_hexagon_vertices(center_x, center_y, radius, angle_offset):
    """
    Create the 6 vertices of a regular hexagon centered at (center_x, center_y)
    with distance 'radius' from center to any vertex. The hexagon is rotated
    by 'angle_offset'.
    """
    # Each interior angle in a regular hexagon is 120 degrees, but for
    # constructing vertices we just step through 2π in increments of π/3.
    vertices = []
    for i in range(6):
        theta = angle_offset + i * (2 * math.pi / 6)
        x = center_x + radius * math.cos(theta)
        y = center_y + radius * math.sin(theta)
        vertices.append((x, y))
    return vertices

def vector_from_points(p1, p2):
    """Return the vector (dx, dy) going from p1 -> p2."""
    return (p2[0] - p1[0], p2[1] - p1[1])

def dot(v1, v2):
    """Dot product of two 2D vectors."""
    return v1[0]*v2[0] + v1[1]*v2[1]

def vector_length(v):
    """Length (magnitude) of 2D vector v."""
    return math.sqrt(v[0]*v[0] + v[1]*v[1])

def normalize(v):
    """Normalize vector v to unit length. Returns (0,0) if v is (0,0)."""
    length = vector_length(v)
    if length == 0:
        return (0, 0)
    return (v[0]/length, v[1]/length)

def line_collision_with_circle(p1, p2, center, radius):
    """
    Check collision of a circle with line segment p1 -> p2.
    Return:
      (False, None) if no collision,
      (True, (collision point x, collision point y, normal nx, ny)) if collision.
    """
    # Segment vector
    seg_v = vector_from_points(p1, p2)
    # Vector from p1 to circle center
    center_v = vector_from_points(p1, center)

    # Project center_v onto seg_v to find the closest point on the line
    seg_len_sq = dot(seg_v, seg_v)
    if seg_len_sq == 0:
        # p1 and p2 are the same points
        dist = vector_length(vector_from_points(p1, center))
        if dist < radius:
            # Collision at that point, normal can be from p1 to center
            n = normalize(vector_from_points(p1, center))
            return True, (p1[0], p1[1], n[0], n[1])
        else:
            return False, None

    t = dot(center_v, seg_v) / seg_len_sq
    # Clamp t to the range [0..1], so we stay within the segment
    t = max(0, min(1, t))

    closest_x = p1[0] + seg_v[0] * t
    closest_y = p1[1] + seg_v[1] * t
    # Distance from circle center to this closest point on line
    dist_v = vector_from_points((closest_x, closest_y), center)
    dist = vector_length(dist_v)

    if dist <= radius:
        # There is a collision
        if dist != 0:
            n = normalize(dist_v)  # normal is from collision point to center
        else:
            # circle center is exactly on the line
            n = normalize(vector_from_points(p1, p2))
        return True, (closest_x, closest_y, n[0], n[1])
    else:
        return False, None

# -----------------------------------------------------------------------------
# Main Program
# -----------------------------------------------------------------------------
def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Bouncing Ball in Spinning Hexagon")
    clock = pygame.time.Clock()

    # Ball properties
    ball_x, ball_y = WIDTH // 2, HEIGHT // 2 - 50   # Moved ball inside
    ball_vx, ball_vy = INIT_BALL_VEL

    # Hexagon rotation
    hex_angle = 0.0

    running = True
    while running:
        dt = clock.tick(FPS) / 1000.0  # delta time in seconds

        # -------------------------------------
        # Event handling
        # -------------------------------------
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # -------------------------------------
        # Update physics
        # -------------------------------------
        # Apply gravity
        ball_vy += GRAVITY

        # Apply friction
        speed = math.sqrt(ball_vx*ball_vx + ball_vy*ball_vy)
        if speed != 0:
            fric_factor = 1 - FRICTION
            ball_vx *= fric_factor
            ball_vy *= fric_factor

        # Update ball position
        ball_x += ball_vx
        ball_y += ball_vy

        # Rotate the hexagon
        hex_angle += HEX_ROTATION_SPEED

        # Check collision with hexagon edges
        center_x, center_y = WIDTH // 2, HEIGHT // 2
        vertices = create_hexagon_vertices(center_x, center_y, HEX_RADIUS, hex_angle)

        for i in range(len(vertices)):
            p1 = vertices[i]
            p2 = vertices[(i + 1) % len(vertices)]

            collision, info = line_collision_with_circle(p1, p2, (ball_x, ball_y), BALL_RADIUS)
            if collision:
                cx, cy, nx, ny = info
                overlap = BALL_RADIUS - math.sqrt((ball_x - cx)**2 + (ball_y - cy)**2)
                ball_x += nx * overlap
                ball_y += ny * overlap

                vel_dot_n = dot((ball_vx, ball_vy), (nx, ny))
                ball_vx -= 2 * vel_dot_n * nx
                ball_vy -= 2 * vel_dot_n * ny

                ball_vx *= RESTITUTION
                ball_vy *= RESTITUTION

        # -------------------------------------
        # Drawing
        # -------------------------------------
        screen.fill((30, 30, 30))
        pygame.draw.polygon(screen, (200, 200, 200), vertices, width=2)
        pygame.draw.circle(screen, (255, 0, 0), (int(ball_x), int(ball_y)), BALL_RADIUS)
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
