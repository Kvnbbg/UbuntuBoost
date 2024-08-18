#!/usr/bin/env python3

import time
import sys
import os
import webbrowser
import subprocess

# Placeholder text animation
def placeholder(text):
    try:
        for char in text:
            sys.stdout.write(char)
            sys.stdout.flush()
            time.sleep(0.05)
        print()
    except Exception as e:
        print(f"Error displaying text: {e}")

# Simple loading animation
def loading_animation(text):
    try:
        for i in range(3):
            sys.stdout.write(f'\r{text}{"." * (i + 1)}{" " * (2 - i)}')
            sys.stdout.flush()
            time.sleep(0.5)
        print("\n")
    except Exception as e:
        print(f"Error during loading animation: {e}")

# Clear terminal screen
def clear_screen():
    try:
        os.system("cls" if os.name == "nt" else "clear")
    except Exception as e:
        print(f"Error clearing screen: {e}")

# Show credits with interactive links
def show_credits():
    try:
        clear_screen()
        print("Credits:")
        placeholder("Developed by Kevin Marville")
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
            webbrowser.open(links[link_choice])
        else:
            print("Returning to the main menu.")
        time.sleep(1)
        main_menu()
    except Exception as e:
        print(f"Error displaying credits: {e}")

# Function to execute the Ubuntu optimizer
def run_optimizer():
    try:
        clear_screen()
        confirmation = input("\nAre you sure you want to optimize your system? (yes/no): ").strip().lower()
        if confirmation in ["yes", "y"]:
            loading_animation("Starting Ubuntu Optimizer")
            from src.optimizer import main as optimizer_main
            optimizer_main()
            placeholder("\nOptimization Complete!")
        else:
            print("Optimization canceled.")
        time.sleep(1)
        main_menu()
    except Exception as e:
        print(f"Error running optimizer: {e}")

# Function to execute Sonic Pi and other programs
def run_sonic_pi():
    try:
        clear_screen()
        confirmation = input("\nAre you sure you want to run Sonic Pi and other programs? (yes/no): ").strip().lower()
        if confirmation in ["yes", "y"]:
            loading_animation("Starting Sonic Pi and other programs")
            from src.sonic_pi_init import main as sonic_pi_main  # Assuming the script is named sonic_pi_init.py
            sonic_pi_main()
            placeholder("\nSonic Pi and other programs have been executed!")
        else:
            print("Operation canceled.")
        time.sleep(1)
        main_menu()
    except Exception as e:
        print(f"Error running Sonic Pi: {e}")

# Main menu
def main_menu():
    try:
        clear_screen()
        placeholder("Welcome to UbuntuBoost!")
        time.sleep(1)

        while True:
            print("\nMain Menu:")
            print("1: Run Ubuntu Optimizer")
            print("2: Run Sonic Pi and Other Programs")
            print("3: Credits")
            print("4: Exit")
            choice = input(">> ").strip().lower()

            if choice in ["1", "optimizer", "optimize", "opt", "boost", "optimi"]:
                run_optimizer()
            elif choice == "2":
                run_sonic_pi()
            elif choice == "3":
                show_credits()
            elif choice == "4":
                print("Exiting UbuntuBoost. Goodbye!")
                sys.exit(0)
            else:
                print("Invalid choice, please try again.")
            time.sleep(1)
    except Exception as e:
        print(f"Error in main menu: {e}")

# Entry point
if __name__ == "__main__":
    try:
        main_menu()
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)
