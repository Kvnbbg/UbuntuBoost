import os
import platform
import subprocess
import sys
import shutil
import tkinter as tk
from tkinter import messagebox

MAX_RETRIES = 3

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

def ensure_python_and_pip():
    """Ensure Python3 and pip are installed."""
    if not check_command('python3'):
        print_status("Python3 not found. Installing Python3...", "🔍")
        execute_with_retries(['sudo', 'apt', 'install', '-y', 'python3'], "Python3 installation", alternative_method=install_python)
    
    if not check_command('pip3'):
        print_status("pip3 not found. Installing pip3...", "🔍")
        execute_with_retries(['sudo', 'apt', 'install', '-y', 'python3-pip'], "pip3 installation")

def install_pyinstaller():
    """Ensure PyInstaller is installed."""
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '--upgrade', 'pip'])
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'pyinstaller'])
        print_status("PyInstaller installed successfully.", "✅")
    except subprocess.CalledProcessError as e:
        print(f"Failed to install PyInstaller: {str(e)}")
        sys.exit(1)

def create_executable():
    """Create the executable using PyInstaller."""
    system = platform.system()
    try:
        if system == "Windows":
            # Create .exe for Windows
            subprocess.check_call(['pyinstaller', '--onefile', '--windowed', 'ubuntu_boost.py'])
            print_status("Executable created for Windows (ubuntu_boost.exe) in the 'dist/' folder.", "✅")
        elif system == "Darwin":
            # Create a Mac OS app bundle
            subprocess.check_call(['pyinstaller', '--onefile', '--windowed', 'ubuntu_boost.py'])
            print_status("Executable created for macOS (ubuntu_boost.app) in the 'dist/' folder.", "✅")
        elif system == "Linux":
            # Create an executable for Linux
            subprocess.check_call(['pyinstaller', '--onefile', '--windowed', 'ubuntu_boost.py'])
            print_status("Executable created for Linux (ubuntu_boost) in the 'dist/' folder.", "✅")
        else:
            print(f"Unsupported operating system: {system}")
            sys.exit(1)

        # Set execute permissions for the generated file on Linux and macOS
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

def main():
    print_status("Ensuring Python and pip are installed...", "🔍")
    ensure_python_and_pip()

    print_status("Installing PyInstaller...", "🔧")
    install_pyinstaller()

    print_status("Creating the executable...", "🚀")
    create_executable()

    print_status("Done.", "🎉")

# GUI Functionality to Add Admin Button
def create_admin_button():
    root = tk.Tk()
    root.title("UbuntuBoost Installer")

    tk.Label(root, text="UbuntuBoost Installer", font=("Helvetica", 16)).pack(pady=10)
    tk.Label(root, text="This installation may require administrative privileges.", font=("Helvetica", 12)).pack(pady=5)
    
    admin_button = tk.Button(root, text="Run as Admin", command=run_as_admin, width=20)
    admin_button.pack(pady=10)

    exit_button = tk.Button(root, text="Exit", command=root.quit, width=20)
    exit_button.pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    if os.geteuid() != 0:
        create_admin_button()
    else:
        main()
