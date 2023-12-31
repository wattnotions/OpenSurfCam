from picamera2 import Picamera2
from picamera2.encoders import H264Encoder
import time
import paramiko
import os
import subprocess  # For executing ffmpeg command

# Video recording settings
output_filename = "output.h264"
mp4_filename = str(int(time.time())) + ".mp4" # Name for the converted file
duration_seconds = 5 # Change this to your desired duration
encoder = H264Encoder(bitrate=10000000)

# SFTP settings
remote_server = "54.228.44.39"  # Change to your remote server hostname/IP
remote_port = 22  # Default SFTP port
remote_username = "bitnami"  # Change to your remote username
remote_directory = "/home/bitnami/surfeye/static/videos"  # Change to your desired remote directory
pem_file_path = "/home/shane/OpenSurfCam/key"  # Path to your .pem file

# Callback function to print upload progress
def print_progress(transferred, to_transfer):
    print(f"Uploaded {transferred} out of {to_transfer} bytes ({transferred/to_transfer:.2%})")

# Initialize the camera
with Picamera2() as camera:
    camera.resolution = (640, 480)
    camera.framerate = 30

    print("Video recording started.")
    camera.start_recording(encoder, output_filename)

    # Record for the specified duration
    time.sleep(duration_seconds)

    camera.stop_recording()
    print("Video recording ended.")

# Convert h264 to mp4
print("Converting to mp4 format...")
subprocess.run(["ffmpeg", "-i", output_filename, "-c:v", "copy", "-format", "mp4", mp4_filename])

print("Conversion complete.")

# Use the private key from the .pem file for authentication
print("Initializing SSH connection...")
private_key = paramiko.RSAKey.from_private_key_file(pem_file_path)

# Establish a connection to the server
transport = paramiko.Transport((remote_server, remote_port))
transport.connect(username=remote_username, pkey=private_key)

# Open an SFTP session
sftp = transport.open_sftp_client()

print("Starting file upload...")
sftp.put(mp4_filename, f"{remote_directory}/{mp4_filename}", callback=print_progress)

# Close the SFTP connection
sftp.close()
transport.close()

print(f"File upload complete. Video uploaded to {remote_directory}/{mp4_filename}")

# Code to delete the files after uploading
for filename in [output_filename, mp4_filename]:
    if os.path.exists(filename):
        os.remove(filename)
        print(f"File {filename} has been deleted.")
    else:
        print(f"File {filename} does not exist or has already been deleted.")
