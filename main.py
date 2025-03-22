import yaml, serial, os, subprocess
# Load YAML file
with open("config.yaml", "r") as file:
    config = yaml.safe_load(file)

# Accessing values
print("Export Location:", config["export_location"])

COM_PORT = config["scanner"]["com_port"]
BAUDERATE = config["scanner"]["baudrate"]
TIMEOUT = config["scanner"]["timeout"]


def scanner_recursion():
    try:
        # Open the serial connection to the scanner
        with serial.Serial(COM_PORT, BAUDERATE, timeout=TIMEOUT) as ser:
            print(f"Listening on {COM_PORT}... (Scan a barcode)")

            while True:
                data = ser.readline().decode("utf-8").strip()  # Read and decode scanner input
                if data:
                    print("Scanned Data:", data)
    except serial.SerialException as e:
        print(f"Error: {e}")


def update_from_github():
    repo_path = os.path.dirname(os.path.abspath(__file__))  # Get current script directory
    try:
        print("Fetching latest updates from GitHub...")
        subprocess.run(["git", "-C", repo_path, "pull"], check=True)
        print("Update successful!")
    except subprocess.CalledProcessError as e:
        print(f"Error updating from GitHub: {e}")

if __name__ == "__main__":
    update_from_github()