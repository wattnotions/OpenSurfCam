import picamera
import time
import paramiko

# Video recording settings
output_filename = "output.h264"
duration_seconds = 30  # Change this to your desired duration

# SFTP settings
remote_server = "18.201.217.84"  # Change to your remote server hostname/IP
remote_port = 22  # Default SFTP port
remote_username = "bitnami"  # Change to your remote username
remote_directory = "/home/bitnami/videos"  # Change to your desired remote directory
pem_file_path = "/home/pi/OpenSurfCam/key.pem"  # Path to your .pem file

# Initialize the camera
with picamera.PiCamera() as camera:
    camera.resolution = (640, 480)
    camera.framerate = 30

    # Start recording
    camera.start_recording(output_filename)

    # Record for the specified duration
    camera.wait_recording(duration_seconds)

    # Stop recording
    camera.stop_recording()

# Use the private key from the .pem file for authentication
private_key = paramiko.RSAKey.from_private_key_file(pem_file_path)

# Establish a connection to the server
transport = paramiko.Transport((remote_server, remote_port))
transport.connect(username=remote_username, pkey=private_key)

# Open an SFTP session
sftp = transport.open_sftp_client()
sftp.put(output_filename, f"{remote_directory}/{output_filename}")

# Close the SFTP connection
sftp.close()
transport.close()

print(f"Video uploaded to {remote_directory}/{output_filename}")
