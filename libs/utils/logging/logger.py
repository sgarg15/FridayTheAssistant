import logging

from libs.utils.constants import Constants

# To tail the logs file in Windows (Powershell): Get-Content friday.log -Wait -Tail 30

constants = Constants()
colors = constants.color

# Create a logger
logger = logging.getLogger('friday_logger')
logger.setLevel(logging.DEBUG)

# Create a formatter to define the log format
fileFormatter = logging.Formatter('----------------------\n%(asctime)s - %(levelname)s - %(message)s\n')
consoleFormatter = logging.Formatter(colors.GREEN + '\n%(asctime)s - %(levelname)s - %(message)s' + colors.END)

# Create a file handler to write logs to a file
file_handler = logging.FileHandler('friday.log')
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(fileFormatter)

# Create a custom stream handler that prints "Content Logged" with correct formatting
class CustomConsoleHandler(logging.StreamHandler):
    def emit(self, record):
        # Backup the original message
        original_msg = record.msg
        # Replace the message with "Content Logged"
        record.msg = "Content Logged"
        record.args = ()  # Clear any arguments to prevent formatting issues
        # Emit the modified record
        super().emit(record)
        # Restore the original message
        record.msg = original_msg
        record.args = ()  # Restore any arguments

# Create and configure the custom console handler
custom_console_handler = CustomConsoleHandler()
custom_console_handler.setLevel(logging.INFO)  # You can set the desired log level for console output
custom_console_handler.setFormatter(consoleFormatter)

# Add the handlers to the logger
logger.addHandler(file_handler)
logger.addHandler(custom_console_handler)
