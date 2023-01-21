import os
import subprocess
import getpass

def scan_directory(directory):
    result = subprocess.run(['clamscan', '-r', directory], stdout=subprocess.PIPE)
    return result.stdout.decode()

# Check if the script is running as root
if getpass.getuser() != 'root':
    print("This script must be run as root")
    exit()

root_directory = '/'
directories = [d for d in os.listdir(root_directory) if os.path.isdir(os.path.join(root_directory, d))]

# Create a log file to store the results
with open('scan_results.txt', 'w') as f:
    for directory in directories:
        try:
            result = scan_directory(os.path.join(root_directory, directory))
            f.write(result)
            print(result)
            # Check if the scan found any infected files
            if "Infected files: 1" in result:
                print(f"Found infected files in {directory}, deleting...")
                # Delete infected files
                subprocess.run(['clamscan', '-r', '--remove', directory], stdout=subprocess.PIPE)
                f.write(f"Deleted infected files in {directory}")
        except Exception as e:
            print(f"An error occurred while scanning {directory}: {e}")
            f.write(f"An error occurred while scanning {directory}: {e}")
