import os
import subprocess

from libs.utils.logging.logger import logger


class Runner:
    def __init__(self):
        pass		

    def runCode(self, code: str):
        logger.info(f"Going to run this code: \n{code}")
        try:
            # Capture the standard output and error
            result = subprocess.run(['python', '-c', code], capture_output=True, text=True, check=True)
            if result.stdout:
                logger.info(f"Code output: {result.stdout.strip()}")
            if result.stderr:
                logger.error(f"Code error: {result.stderr.strip()}")
            return result.stdout.strip()
        except subprocess.CalledProcessError as e:
            logger.error(f"Error running code: {e.stderr.strip()}")
            return e.stderr.strip()