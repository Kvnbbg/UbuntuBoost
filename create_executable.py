import os
import platform
import subprocess
import sys

def install_pyinstaller():
    """Ensure PyInstaller is installed."""
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '--upgrade', 'pip'])
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'pyinstaller'])
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
            print("Executable created for Windows (ubuntu_boost.exe) in the 'dist/' folder.")
        elif system == "Darwin":
            # Create a Mac OS app bundle
            subprocess.check_call(['pyinstaller', '--onefile', '--windowed', 'ubuntu_boost.py'])
            print("Executable created for macOS (ubuntu_boost.app) in the 'dist/' folder.")
        elif system == "Linux":
            # Create an executable for Linux
            subprocess.check_call(['pyinstaller', '--onefile', '--windowed', 'ubuntu_boost.py'])
            print("Executable created for Linux (ubuntu_boost) in the 'dist/' folder.")
        else:
            print(f"Unsupported operating system: {system}")
            sys.exit(1)

        # Set execute permissions for the generated file on Linux and macOS
        if system in ["Linux", "Darwin"]:
            dist_path = os.path.join('dist', 'ubuntu_boost')
            if os.path.exists(dist_path):
                os.chmod(dist_path, 0o755)
                print(f"Set executable permissions for {dist_path}.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to create the executable: {str(e)}")
        sys.exit(1)

def main():
    print("Installing PyInstaller...")
    install_pyinstaller()
    print("Creating the executable...")
    create_executable()
    print("Done.")

if __name__ == "__main__":
    main()
