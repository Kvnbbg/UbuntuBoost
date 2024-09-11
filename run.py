#!/usr/bin/env python3

import time
import sys
import os
import subprocess
import webbrowser
import logging
from math import exp

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Placeholder text animation with adaptive speed using math calculation
def placeholder(text, delay_base=0.05):
    try:
        for i, char in enumerate(text):
            sys.stdout.write(char)
            sys.stdout.flush()
            time.sleep(delay_base * exp(-0.01 * i))  # Adaptive delay based on exp decay
        print()
    except Exception as e:
        logger.error(f"⚠️ Error displaying text: {e}")

# Loading animation optimized for speed and smoothness
def loading_animation(text):
    try:
        for i in range(3):
            sys.stdout.write(f'\r{text}{"." * (i + 1)}{" " * (2 - i)}')
            sys.stdout.flush()
            time.sleep(0.3)  # Reduced delay for faster animations
        print("\n")
    except Exception as e:
        logger.error(f"⚠️ Error during loading animation: {e}")

# Clear terminal screen
def clear_screen():
    try:
        os.system("cls" if os.name == "nt" else "clear")
    except Exception as e:
        logger.error(f"⚠️ Error clearing screen: {e}")

# Check if install.py was executed successfully by validating virtual environment and dependencies
def check_installation():
    venv_exists = os.path.exists(".venv")
    if not venv_exists:
        logger.error("🚨 Installation not detected! Please run install.py before proceeding.")
        sys.exit(1)

    try:
        result = subprocess.run([sys.executable, "-m", "pip", "freeze"], capture_output=True, text=True, check=True)
        installed_packages = result.stdout
        if 'pygame' not in installed_packages:
            raise Exception("🚨 pygame not found!")
        if 'pyinstaller' not in installed_packages:
            raise Exception("🚨 pyinstaller not found!")
    except subprocess.CalledProcessError as e:
        logger.error(f"⚠️ Dependency check failed. Please ensure all dependencies are installed.")
        logger.info("💡 Tip: Run `pip install -r requirements.txt` to install dependencies.")
        sys.exit(1)
    except Exception as e:
        logger.error(f"⚠️ {str(e)}. Dependencies missing.")
        logger.info("🔗 Tip: Visit https://pip.pypa.io/en/stable/installation/ for installation help.")
        sys.exit(1)

# Show credits with interactive links and additional info for troubleshooting
def show_credits():
    try:
        clear_screen()
        logger.info("👨‍💻 Showing credits.")
        placeholder("Developed by Kevin Marville 🚀")
        print("\nFollow me on:")
        print("1: GitHub - https://github.com/kvnbbg")
        print("2: Blog - https://kvnbbg.fr")
        print("3: Portfolio - https://kvnbbg-creations.io")
        print("4: Instagram - @techandstream")
        print("5: LinkedIn - https://linkedin.com/in/kevin-marville")
        
        link_choice = input("\nEnter the number of the link you'd like to open, or press Enter to skip: ").strip()
        links = {
            "1": "https://github.com/kvnbbg",
            "2": "https://kvnbbg.fr",
            "3": "https://kvnbbg-creations.io",
            "4": "https://www.instagram.com/techandstream/",
            "5": "https://linkedin.com/in/kevin-marville"
        }
        
        if link_choice in links:
            logger.info(f"🌐 Opening {links[link_choice]}")
            webbrowser.open(links[link_choice])
        else:
            logger.info("⏩ Returning to the main menu.")
        time.sleep(1)
        main_menu()
    except Exception as e:
        logger.error(f"⚠️ Error displaying credits: {e}")

# Delegate optimizer management to src/__init__.py and handle execution smartly
def run_optimizer():
    try:
        clear_screen()
        confirmation = input("\nAre you sure you want to optimize your system? (yes/no): ").strip().lower()
        if confirmation in ["yes", "y"]:
            loading_animation("⚙️ Starting Optimizer")
            from src import main as optimizer_main
            optimizer_main()  # This will decide which optimizer to run based on OS
            placeholder("\n✅ Optimization Complete! 🎉")
        else:
            logger.info("❌ Optimization canceled.")
        time.sleep(1)
        main_menu()
    except Exception as e:
        logger.error(f"⚠️ Error running optimizer: {e}")
        logger.info("🔗 Tip: Check the logs for more details or visit https://support.com/troubleshooting for help.")

# Main menu - smarter and more user-friendly
def main_menu():
    try:
        clear_screen()
        placeholder("✨ Welcome to UbuntuBoost! ✨")
        time.sleep(1)

        menu_options = {
            "1": "Run System Optimizer",
            "2": "Show Credits",
            "3": "Exit"
        }

        while True:
            print("\nMain Menu:")
            for key, value in menu_options.items():
                print(f"{key}: {value}")
                
            choice = input(">> ").strip().lower()

            if choice == "1":
                run_optimizer()
            elif choice == "2":
                show_credits()
            elif choice == "3":
                logger.info("👋 Exiting UbuntuBoost. Goodbye!")
                sys.exit(0)
            else:
                logger.warning("❌ Invalid choice, please try again.")
            time.sleep(1)
    except Exception as e:
        logger.error(f"⚠️ Error in main menu: {e}")
        sys.exit(1)

# Entry point
if __name__ == "__main__":
    try:
        check_installation()  # Ensure install.py has been executed and dependencies are present
        main_menu()
    except Exception as e:
        logger.error(f"⚠️ Unexpected error: {e}")
        sys.exit(1)
