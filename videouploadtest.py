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

# Upload the video to the remote server using SFTP
transport = paramiko.Transport((remote_server, remote_port))
transport.connect(username="bitnami")

sftp = transport.open_sftp()
sftp.put(output_filename, f"{remote_directory}/{output_filename}")

# Close the SFTP connection
sftp.close()
transport.close()

print(f"Video uploaded to {remote_directory}/{output_filename}")
