import os
import subprocess
import sys
import platform
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def validate_script_path(script_path):
    """
    Validate that the script path exists and is a file.
    :param script_path: The full path to the script file to validate.
    :return: bool - True if valid, False otherwise.
    """
    if not os.path.exists(script_path):
        logger.warning(f"⚠️ Script not found: {script_path}")
        return False
    if not os.path.isfile(script_path):
        logger.warning(f"⚠️ Not a file: {script_path}")
        return False
    return True

def execute_script(script_path):
    """
    Executes a script by its path if it passes validation.
    :param script_path: The full path to the script file to execute.
    :return: bool - True if the script executed successfully, False otherwise.
    """
    if validate_script_path(script_path):
        try:
            logger.info(f"⚙️ Attempting to execute: {script_path}")
            result = subprocess.run([sys.executable, script_path], check=True, capture_output=True, text=True)
            logger.info(f"✅ {os.path.basename(script_path)} executed successfully.")
            logger.debug(f"📝 Output:\n{result.stdout}")
            return True
        except subprocess.CalledProcessError as e:
            logger.error(f"❌ Failed to execute {os.path.basename(script_path)}: {e.stderr}")
            logger.info("💡 Tip: Ensure the script has the correct permissions and required dependencies.")
            return False
        except Exception as e:
            logger.error(f"❌ An unexpected error occurred while executing {os.path.basename(script_path)}: {e}")
            logger.info("🔧 Troubleshooting: Check if the script path is correct or if there are missing dependencies.")
            return False
    return False

def main():
    """
    Main function to manage the execution of optimizers based on the OS.
    It selects the correct script depending on the user's operating system.
    """
    system = platform.system()
    logger.info(f"📋 Detected OS: {system}")

    if system == "Linux":
        logger.info("🐧 Detected Linux (Ubuntu) system.")
        script = "Optimizer.py"
    elif system == "Darwin":
        logger.info("🍎 Detected macOS system.")
        script = "MacBoost.sh"
    else:
        logger.error(f"⚠️ Unsupported operating system: {system}. This script only supports Linux (Ubuntu) and macOS.")
        sys.exit(1)

    script_path = os.path.join("src", script)
    success = execute_script(script_path)

    if not success:
        logger.error(f"⚠️ Script execution failed: {script_path}")
        logger.info("🔗 Tip: Visit https://support.com/troubleshooting for more help with script execution.")

    logger.info("🎉 Script execution management completed.")

if __name__ == "__main__":
    main()

