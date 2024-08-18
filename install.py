import os
import platform
import subprocess
import sys
import shutil
import tkinter as tk
from tkinter import messagebox

MAX_RETRIES = 3

# Assign complexity scores to dependencies
DEPENDENCIES = {
    'python3': 1,
    'pip3': 1,
    'pygame': 2,
    'pyinstaller': 3,
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

def request_admin_permissions():
    """Request administrative permissions if not already running as root."""
    if os.geteuid() != 0:
        print_status("This action requires administrative permissions. Please run as root or with sudo.", "🔒")
        sys.exit(1)

def install_python():
    """Install Python using the appropriate method for the OS."""
    if platform.system() == "Windows":
        subprocess.check_call(['choco', 'install', 'python', '-y'])
    elif platform.system() == "Darwin":
        subprocess.check_call(['brew', 'install', 'python'])
    elif platform.system() == "Linux":
        subprocess.check_call(['sudo', 'apt', 'install', '-y', 'python3'])
    print_status("Python installed using an alternative method.", "🔧")

def ensure_dependency_installed(dependency, install_command, description, alternative_method=None):
    """Ensure a dependency is installed based on its complexity."""
    if not check_command(dependency):
        print_status(f"{description} not found. Installing...", "🔍")
        execute_with_retries(install_command, f"{description} installation", alternative_method=alternative_method)

def ensure_python_and_pip():
    """Ensure Python3 and pip are installed."""
    ensure_dependency_installed('python3', ['sudo', 'apt', 'install', '-y', 'python3'], "Python3", alternative_method=install_python)
    ensure_dependency_installed('pip3', ['sudo', 'apt', 'install', '-y', 'python3-pip'], "pip3")

def install_pygame():
    """Ensure Pygame is installed."""
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'pygame'])
        print_status("Pygame installed successfully.", "✅")
    except subprocess.CalledProcessError as e:
        print(f"Failed to install Pygame: {str(e)}")
        sys.exit(1)

def install_pyinstaller():
    """Ensure PyInstaller is installed."""
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '--upgrade', 'pip'])
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'pyinstaller'])
        print_status("PyInstaller installed successfully.", "✅")
    except subprocess.CalledProcessError as e:
        print(f"Failed to install PyInstaller: {str(e)}")
        sys.exit(1)

def install_dependencies_in_order():
    """Install all dependencies based on their complexity score."""
    sorted_dependencies = sorted(DEPENDENCIES.items(), key=lambda item: item[1])
    for dep, complexity in sorted_dependencies:
        if dep == 'python3':
            ensure_python_and_pip()
        elif dep == 'pip3':
            ensure_python_and_pip()  # pip3 is handled with Python
        elif dep == 'pygame':
            install_pygame()
        elif dep == 'pyinstaller':
            install_pyinstaller()

def create_executable():
    """Create the executable using PyInstaller."""
    system = platform.system()
    try:
        if system == "Windows":
            subprocess.check_call(['pyinstaller', '--onefile', '--windowed', 'ubuntu_boost.py'])
            print_status("Executable created for Windows (ubuntu_boost.exe) in the 'dist/' folder.", "✅")
        elif system == "Darwin":
            subprocess.check_call(['pyinstaller', '--onefile', '--windowed', 'ubuntu_boost.py'])
            print_status("Executable created for macOS (ubuntu_boost.app) in the 'dist/' folder.", "✅")
        elif system == "Linux":
            subprocess.check_call(['pyinstaller', '--onefile', '--windowed', 'ubuntu_boost.py'])
            print_status("Executable created for Linux (ubuntu_boost) in the 'dist/' folder.", "✅")
        else:
            print(f"Unsupported operating system: {system}")
            sys.exit(1)

        if system in ["Linux", "Darwin"]:
            dist_path = os.path.join('dist', 'ubuntu_boost')
            if os.path.exists(dist_path):
                os.chmod(dist_path, 0o755)
                print_status(f"Set executable permissions for {dist_path}.", "🔧")
    except subprocess.CalledProcessError as e:
        print(f"Failed to create the executable: {str(e)}")
        sys.exit(1)

def run_as_admin():
    """Attempt to run the script as an administrator."""
    if os.geteuid() != 0:
        try:
            print_status("Attempting to run as administrator...", "🔒")
            subprocess.check_call(['sudo', sys.executable] + sys.argv)
            sys.exit(0)
        except subprocess.CalledProcessError as e:
            print_status(f"Failed to gain administrative privileges: {str(e)}", "❌")
            sys.exit(1)
    else:
        print_status("Already running with administrative privileges.", "✅")

def is_display_available():
    """Check if the DISPLAY environment variable is set, indicating a GUI is available."""
    return os.getenv('DISPLAY') is not None

def main():
    print_status("Checking and installing dependencies...", "🔍")
    install_dependencies_in_order()

    print_status("Creating the executable...", "🚀")
    create_executable()

    print_status("Done.", "🎉")

def main_no_gui():
    """Main function to run when no display is available."""
    print_status("No GUI available. Running in non-GUI mode.", "🔧")
    main()

# GUI Functionality to Add Admin Button
def create_admin_button():
    if is_display_available():
        root = tk.Tk()
        root.title("UbuntuBoost Installer")

        tk.Label(root, text="UbuntuBoost Installer", font=("Helvetica", 16)).pack(pady=10)
        tk.Label(root, text="This installation may require administrative privileges.", font=("Helvetica", 12)).pack(pady=5)
        
        admin_button = tk.Button(root, text="Run as Admin", command=run_as_admin, width=20)
        admin_button.pack(pady=10)

        exit_button = tk.Button(root, text="Exit", command=root.quit, width=20)
        exit_button.pack(pady=10)

        root.mainloop()
    else:
        print_status("No display available, skipping GUI.", "⚠️")
        main_no_gui()

if __name__ == "__main__":
    if os.geteuid() != 0:
        create_admin_button()
    else:
        main()
