import subprocess

# Replace 'requirements.txt' with the correct path if it's not in the same directory
requirements_file = 'requirements.txt'

# Run pip to install the requirements
try:
    subprocess.check_call(['pip', 'install', '-r', requirements_file])
    print(f"All packages from {requirements_file} installed successfully.")
except subprocess.CalledProcessError as e:
    print(f"Failed to install packages. Error: {e}")
