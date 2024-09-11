import os
import platform
import shutil
import subprocess
import sys
import tkinter as tk
from tkinter import messagebox

VENV_DIR = ".venv"
MAX_RETRIES = 3

# Assign complexity scores to dependencies
DEPENDENCIES = {
    "python3": 1,
    "pip3": 1,
    "pygame": 2,
    "pyinstaller": 3,
}

def print_status(message, emoji="ℹ️"):
    """Print status messages with an emoji."""
    print(f"{emoji} {message}")

def check_command(command):
    """Check if a command exists on the system."""
    return shutil.which(command) is not None

def execute_with_retries(command, description, retries=MAX_RETRIES, alternative_method=None):
    """Execute a command with retry logic and an alternative method if available."""
    for attempt in range(retries):
        try:
            subprocess.check_call(command, shell=True)
            print_status(f"{description} completed successfully.", "✅")
            return True
        except subprocess.CalledProcessError:
            print_status(f"❌ {description} failed. Attempt {attempt + 1}/{retries}.", "❌")
            if attempt == retries - 1 and alternative_method:
                print_status("Attempting alternative method...", "⚠️")
                alternative_method()
        if not alternative_method:
            break
    sys.exit(1)

def ensure_dependency_installed(dependency, install_command, description, alternative_method=None):
    """Ensure a dependency is installed based on its complexity."""
    if not check_command(dependency):
        print_status(f"{description} not found. Installing...", "🔍")
        execute_with_retries(install_command, f"{description} installation", alternative_method=alternative_method)

def create_virtual_env():
    """Create and activate a virtual environment if it doesn't exist."""
    if not os.path.exists(VENV_DIR):
        print_status("Creating virtual environment...", "🔧")
        subprocess.check_call([sys.executable, "-m", "venv", VENV_DIR])
    
    activate_script = os.path.join(VENV_DIR, "bin", "activate")
    if platform.system() == "Windows":
        activate_script += ".bat"
    
    print_status(f"Activating virtual environment: {activate_script}", "🔧")
    exec(open(activate_script).read(), dict(__file__=activate_script))

def ensure_python_and_pip():
    """Ensure Python3 and pip3 are installed depending on the operating system."""
    system = platform.system()
    
    if system == "Darwin":  # macOS
        ensure_dependency_installed("python3", "brew install python3", "Python3")
        ensure_dependency_installed("pip3", "python3 -m ensurepip --upgrade", "pip3")
    elif system == "Linux":
        ensure_dependency_installed("python3", "sudo apt install -y python3", "Python3")
        ensure_dependency_installed("pip3", "sudo apt install -y python3-pip", "pip3")

def install_pygame():
    """Ensure Pygame is installed."""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pygame"])
        print_status("Pygame installed successfully.", "✅")
    except subprocess.CalledProcessError as e:
        print_status("Attempting to bypass 'externally-managed-environment' error...", "⚠️")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "--break-system-packages", "pygame"])
            print_status("Pygame installed successfully with --break-system-packages.", "✅")
        except subprocess.CalledProcessError as e:
            print(f"Failed to install Pygame even with --break-system-packages: {str(e)}")
            sys.exit(1)

def install_pyinstaller():
    """Ensure PyInstaller is installed."""
    try:
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", "pyinstaller"]
        )
        print_status("PyInstaller installed successfully.", "✅")
    except subprocess.CalledProcessError as e:
        print_status("Attempting to bypass 'externally-managed-environment' error...", "⚠️")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "--break-system-packages", "pyinstaller"])
            print_status("PyInstaller installed successfully with --break-system-packages.", "✅")
        except subprocess.CalledProcessError as e:
            print(f"Failed to install PyInstaller even with --break-system-packages: {str(e)}")
            sys.exit(1)

def install_dependencies_in_order():
    """Install all dependencies based on their complexity score."""
    sorted_dependencies = sorted(DEPENDENCIES.items(), key=lambda item: item[1])
    for dep, __complexity in sorted_dependencies:
        if dep == "python3":
            ensure_python_and_pip()
        elif dep == "pip3":
            ensure_python_and_pip()  # pip3 is handled with Python
        elif dep == "pygame":
            install_pygame()
        elif dep == "pyinstaller":
            install_pyinstaller()

def create_executable():
    """Create the executable using PyInstaller."""
    system = platform.system()
    try:
        subprocess.check_call(
            ["pyinstaller", "--onefile", "--windowed", "ubuntu_boost.py"]
        )
        dist_path = os.path.join("dist", "ubuntu_boost")
        if system == "Windows":
            print_status("Executable created for Windows (ubuntu_boost.exe) in the 'dist/' folder.", "✅")
        elif system == "Darwin":
            print_status("Executable created for macOS (ubuntu_boost.app) in the 'dist/' folder.", "✅")
        elif system == "Linux":
            print_status("Executable created for Linux (ubuntu_boost) in the 'dist/' folder.", "✅")
            os.chmod(dist_path, 0o755)
            print_status(f"Set executable permissions for {dist_path}.", "🔧")
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Executable Creation Failed", f"Failed to create the executable: {str(e)}")
        sys.exit(1)

def is_display_available():
    """Check if the DISPLAY environment variable is set, indicating a GUI is available."""
    return os.getenv("DISPLAY") is not None

def main():
    try:
        create_virtual_env()

        print_status("Checking and installing dependencies...", "🔍")
        install_dependencies_in_order()

        print_status("Creating the executable...", "🚀")
        create_executable()

        print_status("Done.", "🎉")
    except Exception as e:
        print_status(f"An error occurred: {str(e)}", "❌")
        sys.exit(1)

def main_no_gui():
    """Main function to run when no display is available."""
    print_status("No GUI available. Running in non-GUI mode.", "🔧")
    main()

# GUI Functionality to Add Install Button
def create_install_button():
    if is_display_available():
        root = tk.Tk()
        root.title("UbuntuBoost Installer")

        tk.Label(root, text="UbuntuBoost Installer", font=("Helvetica", 16)).pack(pady=10)
        tk.Label(root, text="Press 'Install' to start the installation process.", font=("Helvetica", 12)).pack(pady=5)

        install_button = tk.Button(root, text="Install", command=main, width=20)
        install_button.pack(pady=10)

        exit_button = tk.Button(root, text="Exit", command=root.quit, width=20)
        exit_button.pack(pady=10)

        root.mainloop()
    else:
        print_status("No display available, skipping GUI.", "⚠️")
        main_no_gui()

if __name__ == "__main__":
    create_install_button()
