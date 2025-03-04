import pygame
import sys
import os
import importlib.util
import threading
import subprocess

# -----------------------------------------------------------------------------
# Constants
# -----------------------------------------------------------------------------
WIDTH, HEIGHT = 800, 600      # Screen dimensions
FPS = 60                      # Frames per second
BUTTON_HEIGHT = 80            # Height of the button panel
BUTTON_MARGIN = 10            # Margin between buttons
BUTTON_PADDING = 15           # Padding inside buttons
FONT_SIZE = 24                # Font size for button text

# Colors
BACKGROUND_COLOR = (30, 30, 30)
BUTTON_COLOR = (70, 70, 70)
BUTTON_HOVER_COLOR = (100, 100, 100)
BUTTON_TEXT_COLOR = (255, 255, 255)
TITLE_COLOR = (200, 200, 200)
BACK_BUTTON_COLOR = (150, 50, 50)
BACK_BUTTON_HOVER_COLOR = (200, 70, 70)

# Game files to launch
GAME_FILES = [
    {"name": "GPT o1", "file": "o1.py"},
    {"name": "Sonnet 3.5", "file": "sonnet-35.py"},
    {"name": "Sonnet 3.7", "file": "sonnet-37.py"},
    {"name": "Sonnet 3.7t", "file": "sonnet-37-thinking.py"}
]

class Button:
    def __init__(self, x, y, width, height, text, action, color=BUTTON_COLOR, hover_color=BUTTON_HOVER_COLOR):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.action = action
        self.hovered = False
        self.color = color
        self.hover_color = hover_color
    
    def draw(self, surface, font):
        # Draw button background
        color = self.hover_color if self.hovered else self.color
        pygame.draw.rect(surface, color, self.rect, border_radius=5)
        
        # Draw button text
        text_surf = font.render(self.text, True, BUTTON_TEXT_COLOR)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)
    
    def update(self, mouse_pos):
        self.hovered = self.rect.collidepoint(mouse_pos)
    
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.hovered:
                return self.action()
        return False

class GameLauncher:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("PyGame Launcher")
        self.clock = pygame.time.Clock()
        
        # Create fonts
        self.button_font = pygame.font.SysFont(None, FONT_SIZE)
        self.title_font = pygame.font.SysFont(None, FONT_SIZE * 2)
        
        # Calculate button dimensions
        button_area_width = WIDTH - (2 * BUTTON_MARGIN)
        self.button_width = (button_area_width - (len(GAME_FILES) - 1) * BUTTON_MARGIN) // len(GAME_FILES)
        
        # Create buttons
        self.buttons = []
        for i, game in enumerate(GAME_FILES):
            x = BUTTON_MARGIN + i * (self.button_width + BUTTON_MARGIN)
            y = HEIGHT - BUTTON_HEIGHT + BUTTON_MARGIN
            button = Button(
                x, y, 
                self.button_width, BUTTON_HEIGHT - (2 * BUTTON_MARGIN),
                game["name"],
                lambda g=game: self.launch_game(g)
            )
            self.buttons.append(button)
        
        # State variables
        self.running = True
        self.current_process = None
        
    def launch_game(self, game):
        """Launch a game in a separate process"""
        try:
            # Use the same Python interpreter that's running this script
            python_executable = sys.executable
            
            # Start the game in a new process
            self.current_process = subprocess.Popen([python_executable, game["file"]])
            
            # Start a thread to monitor the process
            monitor_thread = threading.Thread(target=self.monitor_game_process)
            monitor_thread.daemon = True  # Thread will exit when main program exits
            monitor_thread.start()
            
            return True
        except Exception as e:
            print(f"Error launching {game['file']}: {e}")
            self.current_process = None
            return False
    
    def monitor_game_process(self):
        """Monitor the game process and handle its completion"""
        if self.current_process:
            # Wait for the process to complete
            self.current_process.wait()
            # Reset current process
            self.current_process = None
            # Bring launcher window to front
            pygame.display.set_caption("PyGame Launcher")  # Refresh caption to help with focus
    
    def draw(self):
        """Draw the launcher interface"""
        self.screen.fill(BACKGROUND_COLOR)
        
        # Draw title
        title_surf = self.title_font.render("PyGame Launcher", True, TITLE_COLOR)
        title_rect = title_surf.get_rect(center=(WIDTH // 2, HEIGHT // 3))
        self.screen.blit(title_surf, title_rect)
        
        # Draw instructions
        instructions = self.button_font.render("Click a button below to launch a game", True, TITLE_COLOR)
        instructions_rect = instructions.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        self.screen.blit(instructions, instructions_rect)
        
        # Draw button panel background
        pygame.draw.rect(self.screen, (50, 50, 50), 
                         pygame.Rect(0, HEIGHT - BUTTON_HEIGHT, WIDTH, BUTTON_HEIGHT))
        
        # Draw buttons
        for button in self.buttons:
            button.draw(self.screen, self.button_font)
    
    def run(self):
        """Main loop for the launcher"""
        while self.running:
            mouse_pos = pygame.mouse.get_pos()
            
            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                
                # Handle button clicks
                for button in self.buttons:
                    if button.handle_event(event):
                        # Game launched successfully, continue running launcher
                        pass
            
            # Update button states
            for button in self.buttons:
                button.update(mouse_pos)
            
            # Draw the launcher interface
            self.draw()
            
            pygame.display.flip()
            self.clock.tick(FPS)
        
        # Clean up
        pygame.quit()

def main():
    launcher = GameLauncher()
    launcher.run()

if __name__ == "__main__":
    main() 