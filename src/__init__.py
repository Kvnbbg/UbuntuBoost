import os
import subprocess
import sys
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
        logger.warning(f"⚠ Script not found: {script_path}")
        return False
    if not os.path.isfile(script_path):
        logger.warning(f"⚠ Not a file: {script_path}")
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
            logger.info(f"Attempting to execute: {script_path}")
            result = subprocess.run([sys.executable, script_path], check=True, capture_output=True, text=True)
            logger.info(f"✅ {os.path.basename(script_path)} executed successfully.")
            logger.debug(f"Output:\n{result.stdout}")
            return True
        except subprocess.CalledProcessError as e:
            logger.error(f"❌ Failed to execute {os.path.basename(script_path)}: {e.stderr}")
            return False
        except Exception as e:
            logger.error(f"❌ An unexpected error occurred while executing {os.path.basename(script_path)}: {e}")
            return False
    return False

def main():
    """
    Main function to manage the execution of multiple scripts.
    """
    scripts = [
        {"name": "Optimizer", "script": "run.py"},
        {"name": "Sonic Pi", "script": "sonic_pi.py"},
        # Additional scripts can be added here
    ]

    executed_any_script = False

    for entry in scripts:
        script_path = os.path.join("src", entry["script"])
        success = execute_script(script_path)
        if success:
            executed_any_script = True
            break  # Stop after the first successful execution

    if not executed_any_script:
        logger.error("⚠ No scripts were executed successfully. Please check the script names or paths.")

    logger.info("🎉 Script execution management completed.")

if __name__ == "__main__":
    main()
