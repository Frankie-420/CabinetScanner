import yaml, serial, os, subprocess, sqlite3, datetime
# Load YAML file
with open("config.yaml", "r") as file:
    config = yaml.safe_load(file)

COM_PORT = config["scanner"]["com_port"]
BAUDERATE = config["scanner"]["baudrate"]
TIMEOUT = config["scanner"]["timeout"]

DB_PATH = config["database"]["path"]

# Initialize SQLite database
def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS scans (
            id TEXT PRIMARY KEY,
            job_number TEXT NOT NULL,
            cabinet_number INT NOT NULL,
            scan_time TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

# Function to insert a record
def insert_scan(job_number, cabinet_number):
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        scan_id = f"{job_number}-{cabinet_number}"

        scan_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        cursor.execute("""
            INSERT INTO scans (id, job_number, cabinet_number, scan_time)
            VALUES (?, ?, ?, ?)
        """, (scan_id, job_number, cabinet_number, scan_time))

        conn.commit()
    except sqlite3.Error as e:
        print(f"Error inserting record: {e}")
    finally:
        conn.close()

def scanner_recursion():
    try:
        # Open the serial connection to the scanner
        with serial.Serial(COM_PORT, BAUDERATE, timeout=TIMEOUT) as ser:
            print(f"Listening on {COM_PORT}... (Scan a barcode)")

            while True:
                data = ser.readline().decode("utf-8").strip()  # Read and decode scanner input
                if data:
                    print("Scanned Data:", data)
                    job_number, cabinet_number = data.split(",")
                    insert_scan(job_number, cabinet_number)
    except serial.SerialException as e:
        print(f"Error: {e}")


def update_from_github():
    '''
    Supposed to update the script from GitHub
    '''
    repo_path = os.path.dirname(os.path.abspath(__file__))  # Get current script directory
    try:
        print("Fetching latest updates from GitHub...")
        subprocess.run(["git", "-C", repo_path, "pull"], check=True)
        print("Update successful!")
    except subprocess.CalledProcessError as e:
        print(f"Error updating from GitHub: {e}")

if __name__ == "__main__":
    update_from_github()
    init_db()
    scanner_recursion()