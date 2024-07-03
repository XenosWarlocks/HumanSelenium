import subprocess
import sys

# List of packages to install
packages = [
    "selenium",
    "webdriver-manager",
    # Add more packages here
]

# Function to install packages
def install_packages():
    for package in packages:
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            print(f"Successfully installed {package}")
        except subprocess.CalledProcessError as e:
            print(f"Error installing {package}: {e}")

if __name__ == "__main__":
    install_packages()
  
