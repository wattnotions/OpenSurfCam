import picamera
import time
import paramiko
import os

# Video recording settings
output_filename = "output.h264"
duration_seconds = 5  # Change this to your desired duration

# SFTP settings
remote_server = "18.201.217.84"  # Change to your remote server hostname/IP
remote_port = 22  # Default SFTP port
remote_username = "bitnami"  # Change to your remote username
remote_directory = "/home/bitnami/videos"  # Change to your desired remote directory
pem_file_path = "/home/pi/OpenSurfCam/key.pem"  # Path to your .pem file

# Callback function to print upload progress
def print_progress(transferred, to_transfer):
    print(f"Uploaded {transferred} out of {to_transfer} bytes ({transferred/to_transfer:.2%})")

# Initialize the camera
with picamera.PiCamera() as camera:
    camera.resolution = (640, 480)
    camera.framerate = 30

    print("Video recording started.")
    camera.start_recording(output_filename)

    # Record for the specified duration
    camera.wait_recording(duration_seconds)

    camera.stop_recording()
    print("Video recording ended.")

# Use the private key from the .pem file for authentication
print("Initializing SSH connection...")
private_key = paramiko.RSAKey.from_private_key_file(pem_file_path)

# Establish a connection to the server
transport = paramiko.Transport((remote_server, remote_port))
transport.connect(username=remote_username, pkey=private_key)

# Open an SFTP session
sftp = transport.open_sftp_client()

print("Starting file upload...")
sftp.put(output_filename, f"{remote_directory}/{output_filename}", callback=print_progress)

# Close the SFTP connection
sftp.close()
transport.close()

print(f"File upload complete. Video uploaded to {remote_directory}/{output_filename}")

# Code to delete the file after uploading
if os.path.exists(output_filename):
    os.remove(output_filename)
    print(f"File {output_filename} has been deleted.")
else:
    print(f"File {output_filename} does not exist or has already been deleted.")

