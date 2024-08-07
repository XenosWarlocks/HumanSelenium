############################################################################
import subprocess
import sys


# List of packages to install
packages = [
    "selenium",
    "webdriver-manager",
    "pandas",
    "openpyxl"
    # Add more packages here
]


# Function to uninstall and install packages
def reinstall_packages():
    for package in packages:
        try:
            # Uninstall the package
            subprocess.check_call([sys.executable, "-m", "pip", "uninstall", package, "-y"])
            print(f"Successfully uninstalled {package}")
           
            # Install the package
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            print(f"Successfully installed {package}")
           
        except subprocess.CalledProcessError as e:
            print(f"Error processing {package}: {e}")


if __name__ == "__main__":
    reinstall_packages()


