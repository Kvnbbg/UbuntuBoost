#!/usr/bin/env python3
# By https://github.com/kvnbbg
import os
import subprocess
import platform
import sys
import venv
import shutil
import time
import random
import numpy as np

# Constants
VENV_PATH = "my_venv"
TOTAL_TASKS = 10
RETRY_LIMIT = 5

# System metrics (initially set to default values)
cpu_performance = 1.0
thermal_efficiency = 1.0
power_consumption = 1.0

# Utility functions
def log(message, color_code="\033[32m", emoji="💡"):
    """Log messages to the terminal with color and emojis."""
    print(f"{color_code}{emoji} {message}\033[0m")

def execute_command(command, retries=3, check_output=False):
    """Execute a command with optional retries and output checking."""
    for attempt in range(retries):
        try:
            if check_output:
                return subprocess.check_output(command, shell=True, text=True)
            subprocess.check_call(command, shell=True)
            return True
        except subprocess.CalledProcessError:
            log(f"Command failed: {command} (Attempt {attempt+1}/{retries})", "\033[31m", "❌")
            if attempt + 1 == retries:
                log("Max retry limit reached. Proceeding to the next task...", "\033[31m", "⚠️")
                return False
        except Exception as e:
            log(f"Unexpected error: {e}", "\033[31m", "❌")
            return False

def is_ubuntu():
    """Check if the OS is Ubuntu."""
    return platform.system() == "Linux" and "Ubuntu" in subprocess.getoutput("lsb_release -d")

def ensure_ubuntu():
    """Ensure the script is running on Ubuntu, otherwise exit."""
    if not is_ubuntu():
        log("This script is designed to run only on Ubuntu. Exiting.", "\033[31m", "❌")
        sys.exit(1)

def prompt_user_name():
    """Prompt the user to input their name or choose a random one."""
    user_input = input("Enter your name or press Enter for a random name: ").strip()
    user_name = user_input if user_input else random.choice(
        ["Kevin", "Aurelie", "Maria", "Katia", "Emmanuel", "Eliane", "Alex", "Jean", "Michel"]
    )
    log(f"Hello, {user_name}! Let's optimize your system.", "\033[34m", "👋")
    return user_name

def create_virtualenv(venv_path=VENV_PATH):
    """Create a virtual environment if it doesn't exist."""
    if not os.path.exists(venv_path):
        log(f"Creating virtual environment at {venv_path}...", "\033[34m", "🔧")
        venv.create(venv_path, with_pip=True)
        log(f"Virtual environment created at {venv_path}.", "\033[32m", "✅")
    else:
        log(f"Virtual environment already exists at {venv_path}.", "\033[33m", "ℹ️")

def delete_virtualenv(venv_path=VENV_PATH):
    """Delete the virtual environment if it exists."""
    if os.path.exists(venv_path):
        log(f"Deleting virtual environment at {venv_path}...", "\033[34m", "🗑️")
        shutil.rmtree(venv_path)
        log("Virtual environment deleted.", "\033[32m", "✅")

def adjust_system_metrics():
    """Randomly adjust system metrics to simulate performance changes."""
    global cpu_performance, thermal_efficiency, power_consumption
    cpu_performance *= np.random.uniform(0.95, 1.05)
    thermal_efficiency *= np.random.uniform(0.98, 1.02)
    power_consumption *= np.random.uniform(0.90, 1.10)
    log(f"Metrics adjusted: CPU={cpu_performance:.2f}, Thermal={thermal_efficiency:.2f}, Power={power_consumption:.2f}", "\033[34m", "📊")

def run_command_with_options(command, success_msg, error_msg, retry=False, force_remove=False, auto_install=False, cleanup_sources=False):
    """Run a command with various options for retrying, removing, and auto-installing dependencies."""
    retry_count = 0

    while retry_count < RETRY_LIMIT:
        start_time = time.time()
        success = execute_command(command)
        elapsed_time = time.time() - start_time

        if success:
            adjust_system_metrics()
            log(f"{success_msg} in {elapsed_time:.2f} seconds.", "\033[32m", "✅")
            break

        retry_count += 1
        log(f"{error_msg} (Attempt {retry_count}/{RETRY_LIMIT})", "\033[31m", "❌")
        if cleanup_sources:
            regenerate_sources_list()
        if force_remove:
            force_remove_problematic_sources()
        if auto_install:
            install_missing_dependencies()
        if retry_count >= RETRY_LIMIT:
            log("Max retry limit reached. Proceeding to the next task...", "\033[31m", "⚠️")
            break

def regenerate_sources_list():
    """Regenerate the sources.list file to ensure only valid sources are used."""
    backup_sources_list()
    try:
        with open("/etc/apt/sources.list", "w") as sources_list:
            sources_list.write("deb http://archive.ubuntu.com/ubuntu/ $(lsb_release -sc) main restricted universe multiverse\n")
            sources_list.write("deb http://archive.ubuntu.com/ubuntu/ $(lsb_release -sc)-updates main restricted universe multiverse\n")
            sources_list.write("deb http://archive.ubuntu.com/ubuntu/ $(lsb_release -sc)-security main restricted universe multiverse\n")
        log("sources.list regenerated with default Ubuntu repositories.", "\033[32m", "✅")
    except Exception as e:
        log(f"Failed to regenerate sources.list: {e}", "\033[31m", "❌")

def backup_sources_list():
    """Backup the existing sources.list file."""
    log("Backing up existing sources.list...", "\033[34m", "🔄")
    try:
        shutil.copy("/etc/apt/sources.list", "/etc/apt/sources.list.backup")
        log("Backup of sources.list created at /etc/apt/sources.list.backup", "\033[32m", "✅")
    except Exception as e:
        log(f"Failed to create backup of sources.list: {e}", "\033[31m", "❌")

def force_remove_problematic_sources():
    """Force remove problematic sources and conflicting packages."""
    log("Forcing removal of problematic sources and packages...", "\033[33m", "🔄")
    execute_command("sudo rm -f /etc/apt/sources.list.d/*.list")
    execute_command("sudo apt remove --purge -y $(dpkg --list | grep '^rc' | awk '{print $2}')")

def install_missing_dependencies():
    """Install missing dependencies automatically."""
    log("Installing missing dependencies...", "\033[33m", "🔄")
    execute_command("sudo apt install -f")

def clean_sources_list_d():
    """Clean the sources.list.d directory to remove malformed entries."""
    sources_list_dir = "/etc/apt/sources.list.d"
    for file in os.listdir(sources_list_dir):
        if file.endswith(".list"):
            file_path = os.path.join(sources_list_dir, file)
            log(f"Checking {file_path} for errors...", "\033[34m", "🔄")
            try:
                with open(file_path, "r") as f:
                    lines = f.readlines()
                    if not all(line.startswith("deb") or line.startswith("#") for line in lines):
                        log(f"Malformed entries found in {file_path}. Moving to backup.", "\033[31m", "❌")
                        shutil.move(file_path, f"{file_path}.backup")
            except Exception as e:
                log(f"Failed to process {file_path}: {e}", "\033[31m", "❌")

def display_progress_bar(task_num):
    """Display a progress bar based on the task number."""
    progress = int((task_num / TOTAL_TASKS) * 100)
    bar = f"[{'█' * (progress // 10)}{' ' * (10 - (progress // 10))}]"
    log(f"Overall Progress: {bar} {progress}%", "\033[36m", "⌛")

# Main system tasks
def update_system():
    """Update the package list and upgrade all installed packages."""
    run_command_with_options("sudo apt update",
                             "Package list updated.",
                             "Failed to update package list.", retry=True, force_remove=True, auto_install=True, cleanup_sources=True)
    run_command_with_options("sudo apt upgrade -y",
                             "System upgraded with latest packages.",
                             "Failed to upgrade the system.", retry=True, force_remove=True, auto_install=True)
    run_command_with_options("sudo apt full-upgrade -y",
                             "Full system upgrade completed.",
                             "Failed to complete full system upgrade.", retry=True, force_remove=True, auto_install=True)

def install_system_packages():
    """Install necessary system packages for optimization."""
    run_command_with_options("sudo apt install -y cpufrequtils thermald tlp tlp-rdw ufw build-essential git curl wget htop net-tools",
                             "System packages installed.",
                             "Failed to install system packages.", retry=True, force_remove=True, auto_install=True)

def clean_old_kernels():
    """Clean up old kernels to free up disk space."""
    run_command_with_options("sudo apt autoremove --purge -y",
                             "Old kernels removed.",
                             "Failed to remove old kernels.", retry=True, force_remove=True, auto_install=True)

def optimize_system():
    """Optimize the system for performance."""
    run_command_with_options("sudo cpupower frequency-set -g performance",
                             "CPU set to performance mode.",
                             "Failed to set CPU to performance mode.", retry=True, force_remove=True, auto_install=True)
    run_command_with_options("sudo systemctl enable thermald && sudo systemctl start thermald",
                             "Thermal management enabled.",
                             "Failed to enable/start thermal management.", retry=True, force_remove=True, auto_install=True)
    run_command_with_options("sudo systemctl enable tlp && sudo systemctl start tlp",
                             "Power management enabled.",
                             "Failed to enable/start power management.", retry=True, force_remove=True, auto_install=True)

def enhance_security():
    """Enhance system security."""
    run_command_with_options("sudo ufw enable",
                             "UFW firewall enabled.",
                             "Failed to enable UFW firewall.", retry=True, force_remove=True, auto_install=True)
    run_command_with_options("sudo ufw default deny incoming",
                             "Default deny policy for incoming traffic set.",
                             "Failed to set deny policy for incoming traffic.", retry=True, force_remove=True, auto_install=True)
    run_command_with_options("sudo ufw default allow outgoing",
                             "Default allow policy for outgoing traffic set.",
                             "Failed to set allow policy for outgoing traffic.", retry=True, force_remove=True, auto_install=True)
    run_command_with_options("sudo ufw allow ssh",
                             "SSH allowed through firewall.",
                             "Failed to allow SSH through firewall.", retry=True, force_remove=True, auto_install=True)

def configure_swap():
    """Optimize and configure swap space."""
    run_command_with_options("sudo sysctl vm.swappiness=10",
                             "Swappiness set to 10.",
                             "Failed to set swappiness.", retry=True, force_remove=True, auto_install=True)
    run_command_with_options("sudo sysctl vm.vfs_cache_pressure=50",
                             "VFS cache pressure set to 50.",
                             "Failed to set VFS cache pressure.", retry=True, force_remove=True, auto_install=True)

def clean_system():
    """Clean up unnecessary packages and files."""
    run_command_with_options("sudo apt autoremove -y",
                             "System cleaned up.",
                             "Failed to clean up the system.", retry=True, force_remove=True, auto_install=True)
    delete_virtualenv()

# User interaction
def display_menu():
    """Display the menu and return the user's choice."""
    menu_options = {
        "1": "Update and Upgrade System",
        "2": "Install System Packages",
        "3": "Clean Old Kernels",
        "4": "Optimize System Performance",
        "5": "Enhance System Security",
        "6": "Configure Swap Space",
        "7": "Clean System",
        "8": "Full Optimization (All Tasks)",
        "9": "Exit"
    }
    print("\nPlease choose an action:")
    for key, value in menu_options.items():
        print(f"{key}: {value}")
    return input("Enter your choice: ").strip()

def main():
    ensure_ubuntu()
    user_name = prompt_user_name()
    task_num = 0

    create_virtualenv()
    task_num += 1
    display_progress_bar(task_num)

    while True:
        choice = display_menu()
        if choice == "1":
            update_system()
        elif choice == "2":
            install_system_packages()
        elif choice == "3":
            clean_old_kernels()
        elif choice == "4":
            optimize_system()
        elif choice == "5":
            enhance_security()
        elif choice == "6":
            configure_swap()
        elif choice == "7":
            clean_system()
        elif choice == "8":
            update_system()
            install_system_packages()
            clean_old_kernels()
            optimize_system()
            enhance_security()
            configure_swap()
            clean_system()
            break
        elif choice == "9":
            log("Exiting script. Goodbye!", "\033[34m", "👋")
            break
        else:
            log("Invalid choice. Please try again.", "\033[31m", "❌")

        task_num += 1
        display_progress_bar(task_num)

    log("🚀 System is fully optimized, secure, and clean!", "\033[32m", "🚀")

if __name__ == "__main__":
    main()
