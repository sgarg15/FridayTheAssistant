import os
import subprocess

# Define the path to the VSCode executable (may vary depending on your OS)
vscode_path = 'C:/Program Files/VSCode/code.exe'

# Navigate to the home directory
home_dir = os.path.expanduser('~')

# Launch VSCode using subprocess with full path to the executable
subprocess.run([os.path.join(home_dir, vscode_path), '.'])