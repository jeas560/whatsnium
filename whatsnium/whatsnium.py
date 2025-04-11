import os
import time
import yaml
from typing import List, Optional
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.webdriver import WebDriver

__all__ = ["Whatsnium"]


class Whatsnium:
    """
    Whatsnium - Automate WhatsApp Web messaging using Selenium.
    """

    def __init__(self, driver_path: str = "chromedriver", label_file: str = "labels.yaml") -> None:
        """
        Args:
            driver_path (str): Path to the ChromeDriver executable.
            label_file (str): Path to the YAML file containing localized labels.
        """
        if not os.path.exists(driver_path):
            raise FileNotFoundError("ChromeDriver not found at the specified path.")
        if not os.path.exists(label_file):
            raise FileNotFoundError("Label YAML file not found.")    
            
        self.driver_path = driver_path
        self.driver: Optional[WebDriver] = None
        self.labels = self._load_labels(label_file)

    def _load_labels(self, label_file: str) -> dict:
        with open(label_file, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)
        
    def _build_xpath(self, labels: List[str]) -> str:
        return '//div[@role="textbox" and (' + " or ".join([f'@aria-label="{label}"' for label in labels]) + ')]'
                
    def start_driver(self) -> None:
        """Starts the Chrome WebDriver and opens WhatsApp Web."""
        service = Service(self.driver_path)
        self.driver = webdriver.Chrome(service=service)
        self.driver.get("https://web.whatsapp.com/")
        print("[Whatsnium] Please scan the QR code in the opened browser...")

    def wait_for_login(self, timeout: int = 60) -> None:
        """
        Waits for the user to scan the QR code and log in.

        Args:
            timeout (int): Number of seconds to wait.
        """
        print(f"[Whatsnium] Waiting for login (up to {timeout} seconds)...")

        search_box_xpath = self._build_xpath(self.labels["search_input"])
        WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located((By.XPATH, search_box_xpath))
        )
        print("[Whatsnium] Login successful!")

    def send_message(self, contact_name: str, message: str) -> None:
        """
        Sends a message to a WhatsApp contact.

        Args:
            contact_name (str): Name of the contact.
            message (str): Text message to send.
        """
        if not self.driver:
            raise RuntimeError("WebDriver not started. Call start_driver() first.")
        
        search_box_xpath = self._build_xpath(self.labels["search_input"])

        search_box = WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located((By.XPATH, search_box_xpath))
        )
        search_box.clear()
        search_box.send_keys(contact_name)
        time.sleep(1)

        contact = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, f'//span[@title="{contact_name}"]'))
        )
        contact.click()
        time.sleep(1)

        message_box_xpath = self._build_xpath(self.labels["message_input"])
        message_box = self.driver.find_element(By.XPATH, message_box_xpath)
        message_box.send_keys(message + Keys.ENTER)

        print(f"[Whatsnium] Message sent to {contact_name}")

    def read_last_messages(self, contact_name: str, limit: int = 10) -> List[str]:
        """
        Reads the most recent messages from a contact.

        Args:
            contact_name (str): Name of the contact.
            limit (int): Number of messages to retrieve.

        Returns:
            List[str]: List of text messages.
        """
        self.send_message(contact_name, "")
        time.sleep(2)

        messages = self.driver.find_elements(By.XPATH, '//div[contains(@class,"message-in")]')
        return [msg.text for msg in messages[-limit:]]

    def close(self) -> None:
        """Closes the browser."""
        if self.driver:
            self.driver.quit()
            print("[Whatsnium] Browser session closed.")
