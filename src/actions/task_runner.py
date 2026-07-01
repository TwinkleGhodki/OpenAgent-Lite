import os
import shutil
import pyautogui
import time
from selenium import webdriver
from logger import log_action
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import webbrowser
from PIL import ImageGrab
import speech_recognition as sr
import requests
from bs4 import BeautifulSoup

from browser_manager import get_driver, close_driver

import schedule
import time
import threading
import os

# Import your existing task functions
from task_utils import take_screenshot, send_email, web_scrape  # adjust if paths differ

def scheduled_screenshot():
    print("📷 Scheduled screenshot task running...")
    take_screenshot()

def scheduled_email():
    print("📧 Scheduled email task running...")
    subject = "Automated Update"
    body = "This is a scheduled message sent from the automation system."
    to_email = "twinkle.ghodki04@gmail.com"
    send_email(subject, body, to_email)

def scheduled_scrape():
    print("🌐 Scheduled web scraping running...")
    url = "https://example.com"
    web_scrape(url)

def start_scheduler():
    print("Scheduler started. Press Ctrl+C to exit.")

    # 🕐 Schedule your tasks
    schedule.every(1).minutes.do(scheduled_screenshot)
    schedule.every(5).minutes.do(scheduled_email)
    schedule.every(10).minutes.do(scheduled_scrape)

    def run_schedule():
        while True:
            schedule.run_pending()
            time.sleep(1)

    scheduler_thread = threading.Thread(target=run_schedule, daemon=True)
    scheduler_thread.start()


# 1: Open YouTube
def open_youtube():
    try:
        driver = get_driver()
        driver.get("https://www.youtube.com")
        log_action("Open YouTube", "Success")
    except Exception as e:
        log_action("Open YouTube", f"Failed - {e}")

# 2: Rename Files
def rename_files(folder_path):
    try:
        for count, filename in enumerate(os.listdir(folder_path)):
            dst = f"holiday_{str(count+1)}.jpg"
            src = os.path.join(folder_path, filename)
            dst = os.path.join(folder_path, dst)
            os.rename(src, dst)
        log_action("Rename Files", "Success")
    except Exception as e:
        log_action("Rename Files", f"Failed - {e}")

# 3: Delete Temp Files
def delete_temp_files(folder_path):
    try:
        for filename in os.listdir(folder_path):
            if filename.endswith('.tmp'):
                os.remove(os.path.join(folder_path, filename))
        log_action("Delete Temp Files", "Success")
    except Exception as e:
        log_action("Delete Temp Files", f"Failed - {e}")

# 4: Search YouTube
def search_youtube(search_query):
    try:
        driver = get_driver()
        driver.get("https://www.youtube.com")
        time.sleep(2)
        search_box = driver.find_element(By.NAME, "search_query")
        search_box.send_keys(search_query)
        search_box.send_keys(Keys.RETURN)
        time.sleep(5)
        log_action(f"Search YouTube for '{search_query}'", "Success")
    except Exception as e:
        log_action(f"Search YouTube for '{search_query}'", f"Failed - {e}")

# 5: Download PDFs
def download_pdfs(url, download_folder='downloads'):
    try:
        os.makedirs(download_folder, exist_ok=True)
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        pdf_links = [urljoin(url, link.get("href")) for link in soup.find_all("a") if link.get("href", "").endswith(".pdf")]
        if not pdf_links:
            print("No PDFs found on the page.")
            log_action(f"Download PDFs from {url}", "No PDFs Found")
            return
        for pdf_url in pdf_links:
            filename = os.path.join(download_folder, pdf_url.split("/")[-1])
            with requests.get(pdf_url, stream=True) as r:
                with open(filename, 'wb') as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        f.write(chunk)
            print(f"Downloaded: {filename}")
        log_action(f"Download PDFs from {url}", "Success")
    except Exception as e:
        log_action(f"Download PDFs from {url}", f"Failed - {e}")

# 6: Send Email
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

# 7: Open Google
def open_google():
    try:
        driver = get_driver()
        driver.get("https://www.google.com")
        log_action("Open Google", "Success")
    except Exception as e:
        log_action("Open Google", f"Failed - {e}")

# 8: Search Google
def search_google(query):
    try:
        driver = get_driver()
        driver.get("https://www.google.com")
        time.sleep(2)
        search_box = driver.find_element(By.NAME, "q")
        search_box.send_keys(query)
        search_box.send_keys(Keys.RETURN)
        time.sleep(5)
        log_action(f"Search Google for '{query}'", "Success")
    except Exception as e:
        log_action(f"Search Google for '{query}'", f"Failed - {e}")

# 9: Download Images using Pexels API
def download_images(query, num_images=1):
    try:
        folder_path = "downloaded_images"
        os.makedirs(folder_path, exist_ok=True)

        api_key = "PzI4THcRPNfklycoPlXfyVzqFkeW36M3rWOJhomQ5nN8gnt0IzBJ600j"  
        headers = {
            "Authorization": api_key
        }
        params = {
            "query": query,
            "per_page": num_images
        }
        response = requests.get("https://api.pexels.com/v1/search", headers=headers, params=params)

        if response.status_code != 200:
            print(f"Failed to retrieve images. Status code: {response.status_code}")
            return

        data = response.json()
        photos = data.get("photos", [])

        if not photos:
            print("No images found for this query.")
            return

        for i, photo in enumerate(photos):
            img_url = photo["src"]["original"]
            img_data = requests.get(img_url).content
            filename = os.path.join(folder_path, f"{query}_{i + 1}.jpg")
            with open(filename, 'wb') as f:
                f.write(img_data)
            print(f"Downloaded image {i + 1}: {filename}")

        print("Images downloaded successfully.")
        log_action(f"Download Images for '{query}'", "Success")

    except Exception as e:
        print(f"Error while downloading images: {e}")
        log_action(f"Download Images for '{query}'", f"Failed - {e}")


# 10: Take Screenshot
def take_screenshot():
    try:
        screenshot = ImageGrab.grab()
        screenshot.save("screenshot.png")
        print("Screenshot saved as screenshot.png")
        log_action("Take Screenshot", "Success")
    except Exception as e:
        log_action("Take Screenshot", f"Failed - {e}")

# 11: Write to File
def write_to_file(file_path, content):
    try:
        with open(file_path, 'w') as f:
            f.write(content)
        print(f"Written to file: {file_path}")
        log_action(f"Write to File {file_path}", "Success")
    except Exception as e:
        log_action(f"Write to File {file_path}", f"Failed - {e}")

# 12: Voice Command
def voice_command():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening for your command...")
        audio = recognizer.listen(source)
    try:
        command = recognizer.recognize_google(audio)
        print(f"You said: {command}")
        return command
    except sr.UnknownValueError:
        print("Sorry, I could not understand your command.")
    except sr.RequestError as e:
        print(f"Could not request results; {e}")
    return None

# 13: Web Scraping 
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
