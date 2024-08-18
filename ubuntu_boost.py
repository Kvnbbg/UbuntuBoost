import subprocess
import os
import platform
import sys
import shutil
import tkinter as tk
from tkinter import messagebox, scrolledtext, ttk
from threading import Thread
import pygame
import random

# Constants for the game
WIDTH, HEIGHT = 640, 480
BLOCK_SIZE = 20
MAX_HEALTH = 100
ZOMBIE_SPAWN_RATE = 50

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("UbuntuBoost Game - Fun Mode")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BROWN = (139, 69, 19)
GRAY = (128, 128, 128)

# Player Setup
player_x, player_y = WIDTH // 2, HEIGHT // 2
player_health = MAX_HEALTH
player_level = 1
player_experience = 0
player_blocks = []

# Enemy Setup
zombies = []
zombie_types = ["Zombie", "Unbun"]

# Utility Functions
def print_status(message, emoji="📊"):
    """Print status messages with an emoji."""
    print(f"{emoji} {message}")

def run_install_py():
    """Run the healing script install.py if something goes wrong."""
    try:
        subprocess.check_call([sys.executable, 'install.py'])
    except subprocess.CalledProcessError as e:
        print_status(f"Healing failed: {str(e)}", "❌")

def ensure_virtualenv():
    """Ensure the virtual environment is activated or set up."""
    if not os.path.exists('venv'):
        print_status("Setting up the virtual environment...", "🐍")
        subprocess.check_call([sys.executable, '-m', 'venv', 'venv'])

def check_system():
    """Check the operating system and return its name."""
    os_name = platform.system()
    print_status(f"Operating system: {os_name}", "💻")
    return os_name

def install_requirements():
    """Install the required Python packages."""
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])
    except subprocess.CalledProcessError:
        print_status("Failed to install requirements. Attempting healing...", "❌")
        run_install_py()

def mathematical_logic(value1, value2):
    """Example mathematical logic to resolve problems."""
    try:
        result = value1 / value2
        print_status(f"Mathematical Result: {result}", "➗")
        return result
    except ZeroDivisionError:
        print_status("Division by zero error. Healing...", "⚠️")
        run_install_py()
        return None

# Game Functions
def spawn_zombie():
    if random.randint(1, ZOMBIE_SPAWN_RATE) == 1:
        x = random.choice(range(0, WIDTH, BLOCK_SIZE))
        y = random.choice(range(0, HEIGHT, BLOCK_SIZE))
        z_type = random.choice(zombie_types)
        zombies.append(Zombie(x, y, z_type))

def handle_player_input(keys):
    global player_x, player_y, player_health, player_experience
    if keys[pygame.K_LEFT] and player_x > 0:
        player_x -= BLOCK_SIZE
    if keys[pygame.K_RIGHT] and player_x < WIDTH - BLOCK_SIZE:
        player_x += BLOCK_SIZE
    if keys[pygame.K_UP] and player_y > 0:
        player_y -= BLOCK_SIZE
    if keys[pygame.K_DOWN] and player_y < HEIGHT - BLOCK_SIZE:
        player_y += BLOCK_SIZE
    if keys[pygame.K_SPACE]:  # Place a block
        player_blocks.append(Block(player_x, player_y))
    if keys[pygame.K_LCTRL]:  # Shoot a laser
        for zombie in zombies[:]:
            if zombie.rect.colliderect(pygame.Rect(player_x, player_y, BLOCK_SIZE, BLOCK_SIZE)):
                zombie.health -= 10
                if zombie.health <= 0:
                    zombies.remove(zombie)
                    player_experience += 10
                    if player_experience >= 100:
                        player_level += 1
                        player_experience = 0

def draw_game():
    screen.fill(GRAY)
    for block in player_blocks:
        block.draw()
    pygame.draw.rect(screen, GREEN, (player_x, player_y, BLOCK_SIZE, BLOCK_SIZE))
    for zombie in zombies:
        zombie.move_towards_player()
        zombie.draw()
    health_text = pygame.font.SysFont(None, 24).render(f"Health: {player_health}", True, WHITE)
    screen.blit(health_text, (10, 10))
    level_text = pygame.font.SysFont(None, 24).render(f"Level: {player_level}", True, WHITE)
    screen.blit(level_text, (10, 40))
    pygame.display.flip()

def main_game_loop():
  
    running = True
    while running:
        keys = pygame.key.get_pressed()
        handle_player_input(keys)
        spawn_zombie()
        draw_game()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        pygame.time.delay(100)

# Block and Zombie Classes
class Block:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, BLOCK_SIZE, BLOCK_SIZE)

    def draw(self):
        pygame.draw.rect(screen, BROWN, self.rect)

class Zombie:
    def __init__(self, x, y, z_type):
        self.rect = pygame.Rect(x, y, BLOCK_SIZE, BLOCK_SIZE)
        self.type = z_type
        self.health = 50 if z_type == "Zombie" else 100

    def move_towards_player(self):
        if player_x > self.rect.x:
            self.rect.x += BLOCK_SIZE
        elif player_x < self.rect.x:
            self.rect.x -= BLOCK_SIZE
        if player_y > self.rect.y:
            self.rect.y += BLOCK_SIZE
        elif player_y < self.rect.y:
            self.rect.y -= BLOCK_SIZE

    def draw(self):
        color = RED if self.type == "Zombie" else BLUE
        pygame.draw.rect(screen, color, self.rect)

# GUI Functions
def create_gui():
    global output_box, current_slide

    # Initialize the root window
    root = tk.Tk()
    root.title("UbuntuBoost by Kvnbbg")

    # Create a tab control
    tab_control = ttk.Notebook(root)

    # Function to print messages with an emoji
    def print_message(message, emoji="📊"):
        """Print status messages with an emoji."""
        print(f"{emoji} {message}")

    # Function for the Fun Mode tab
    def show_next_slide():
        """Display the next slide in Fun Mode."""
        slides = [
            "Slide 1: UbuntuBoost optimizes your system for performance.",
            "Slide 2: It enhances system security.",
            "Slide 3: You can manage swap space and clean old kernels.",
            "Slide 4: Developer Mode unlocks the full power of UbuntuBoost.",
        ]
        if current_slide < len(slides):
            slide_label.config(text=slides[current_slide])
            current_slide += 1
        else:
            slide_button.config(text="Restart", command=show_next_slide)
            current_slide = 0

    # Fun Mode GUI setup
    fun_tab = ttk.Frame(tab_control)
    tab_control.add(fun_tab, text="Fun Mode")
    current_slide = 0
    slide_label = tk.Label(fun_tab, text="", wraplength=400)
    slide_label.pack(pady=20)
    slide_button = tk.Button(fun_tab, text="Start Fun Mode", command=show_next_slide)
    slide_button.pack(pady=20)

    # Function to update progress in Developer Mode
    def update_progress():
        slider_value = slider.get()
        progress_bar['value'] = slider_value
        reward_level = int(slider_value / 25)

        reward_messages = [
            "You have started your UbuntuBoost adventure!" if gui.language == "en" else "Vous avez démarré votre aventure UbuntuBoost!",
            "You have reached level 25 of UbuntuBoost!" if gui.language == "en" else "Vous avez atteint le niveau 25 de UbuntuBoost!",
            "You have reached level 50 of UbuntuBoost!" if gui.language == "en" else "Vous avez atteint le niveau 50 de UbuntuBoost!",
            "You have reached level 75 of UbuntuBoost!" if gui.language == "en" else "Vous avez atteint le niveau 75 de UbuntuBoost!",
        ]

        if reward_level < len(reward_messages):
            reward_text.insert(tk.END, reward_messages[reward_level] + "\n")

    # Developer Mode GUI setup
    dev_tab = ttk.Frame(tab_control)
    tab_control.add(dev_tab, text="Developer Mode")
    output_box = scrolledtext.ScrolledText(dev_tab, wrap=tk.WORD, width=60, height=20)
    output_box.pack(pady=20)
    start_button = tk.Button(dev_tab, text="Start Advanced User (Developer Mode)", command=lambda: Thread(target=start_advanced_mode).start())
    start_button.pack(pady=20)

    # Add a slider and progress bar to Developer Mode
    slider = ttk.Scale(dev_tab, from_=0, to=100, orient=tk.HORIZONTAL, command=lambda _: update_progress())
    slider.pack(pady=10)
    progress_bar = ttk.Progressbar(dev_tab, orient=tk.HORIZONTAL, length=400, mode='determinate')
    progress_bar.pack(pady=10)
    reward_text = tk.Text(dev_tab, wrap=tk.WORD, height=5, width=60)
    reward_text.pack(pady=10)

    # Pack the tab control and start the main loop
    tab_control.pack(expand=1, fill="both")
    root.mainloop()


def start_advanced_mode():
    """Handle the start of the advanced developer mode."""
    print_status("Starting Developer Mode...", "🔧")
    Thread(target=run_script).start()

def run_script():
    """Run the main script within the virtual environment and display output in the GUI."""
    try:
        print_status("Running the script...", "🚀")
        process = subprocess.Popen([os.path.join('venv', 'bin', 'python'), 'run.py'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        while True:
            output = process.stdout.readline()
            if process.poll() is not None and output == '':
                break
            if output:
                gui_log(output.strip())
    except Exception as e:
        print_status(f"Failed to run the script: {str(e)}", "❌")
        run_install_py()

def gui_log(message):
    """Log messages to the GUI."""
    output_box.insert(tk.END, message + '\n')
    output_box.see(tk.END)

def main():
    print_status("🔍 Checking system requirements...", "🔍")
    ensure_virtualenv()
    check_system()
    install_requirements()
    create_gui()

if __name__ == "__main__":
    main()

