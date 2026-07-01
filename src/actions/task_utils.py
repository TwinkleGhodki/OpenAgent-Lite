import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from datetime import datetime
import pyautogui

def take_screenshot():
    try:
        screenshot = ImageGrab.grab()
        screenshot.save("screenshot.png")
        print("Screenshot saved as screenshot.png")
        log_action("Take Screenshot", "Success")
    except Exception as e:
        log_action("Take Screenshot", f"Failed - {e}")

def send_email(subject, body, to_email, attachment_path=None):
    try:
        sender_email = "twinkle.ghodki04@gmail.com"
        app_password = "zjyjhrharmxokqxg" 

        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = to_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        if attachment_path and os.path.exists(attachment_path):
            with open(attachment_path, 'rb') as file:
                part = MIMEApplication(file.read(), Name=os.path.basename(attachment_path))
                part['Content-Disposition'] = f'attachment; filename="{os.path.basename(attachment_path)}"'
                msg.attach(part)

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, app_password)
        server.send_message(msg)
        server.quit()

        print("Email sent successfully!")
        log_action("Send Email", "Success")

    except Exception as e:
        log_action("Send Email", f"Failed - {e}")

def web_scrape(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        print("\n--- Web Page Title ---")
        print(soup.title.string.strip() if soup.title else "No Title")
        print("\n--- First 500 characters of Page Content ---")
        print(soup.get_text(strip=True)[:500])
        log_action(f"Web Scrape for {url}", "Success")
    except Exception as e:
        log_action(f"Web Scrape for {url}", f"Failed - {e}")
        print(f"Error: {e}")   