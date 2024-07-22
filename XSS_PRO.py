import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time
from selenium.common.exceptions import UnexpectedAlertPresentException, NoAlertPresentException
import argparse

chrome_driver = None

class Colors:
    RESET = "\033[0m"
    RED = "\033[91m"
    GREEN = "\033[92m"

def print_in_color(text, color):
    print(color + text + Colors.RESET)
    
# Function to get the ChromeDriver instance
def get_chrome_driver():
    global chrome_driver
    if chrome_driver is None:
        # If the ChromeDriver instance doesn't exist, create one
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')  # Run in headless mode
        chrome_driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    return chrome_driver

# Function to send payloads and capture the response
def send_payload(url, payload, retries=3):
    for attempt in range(retries):
        try:
            response = requests.get(url + payload)
            return response
        except requests.exceptions.ConnectionError as e:
            print(f"Connection error: {e}. Retrying ({attempt + 1}/{retries})...")
            time.sleep(5) 
        except ConnectionResetError as cre:
            print(f"Connection reset error: {cre}. Retrying ({attempt + 1}/{retries})...")
            time.sleep(5)  
    return None

# Function to check if the payload triggers a popup
def check_popup(url, payload):
    driver = get_chrome_driver()
    
    try:
        driver.get(url + payload)
        time.sleep(2)
        
        # Check for alert
        try:
            alert = driver.switch_to.alert
            alert_text = alert.text
            alert.accept()
            return True, alert_text
        except NoAlertPresentException:
            return False, None
    except UnexpectedAlertPresentException as e:
        try:
            alert = driver.switch_to.alert
            alert_text = alert.text
            alert.accept()
            return True, alert_text
        except NoAlertPresentException:
            return False, None
    finally:
        pass

if __name__ == "__main__":
    print("""


                                                                                
                                             ,-.----.                ,----..    
 ,--,     ,--,  .--.--.    .--.--.           \    /  \              /   /   \   
 |'. \   / .`| /  /    '. /  /    '.         |   :    \            /   .     :  
 ; \ `\ /' / ;|  :  /`. /|  :  /`. /         |   |  .\ :  __  ,-. .   /   ;.  \ 
 `. \  /  / .';  |  |--` ;  |  |--`          .   :  |: |,' ,'/ /|.   ;   /  ` ; 
  \  \/  / ./ |  :  ;_   |  :  ;_            |   |   \ :'  | |' |;   |  ; \ ; | 
   \  \.'  /   \  \    `. \  \    `.         |   : .   /|  |   ,'|   :  | ; | ' 
    \  ;  ;     `----.   \ `----.   \        ;   | |`-' '  :  /  .   |  ' ' ' : 
   / \  \  \    __ \  \  | __ \  \  |        |   | ;    |  | '   '   ;  \; /  | 
  ;  /\  \  \  /  /`--'  //  /`--'  /        :   ' |    ;  : |    \   \  ',  /  
./__;  \  ;  \'--'.     /'--'.     /         :   : :    |  , ;     ;   :    /   
|   : / \  \  ; `--'---'   `--'---'          |   | :     ---'       \   \ .'    
;   |/   \  ' |                              `---'.|                 `---`      
`---'     `--`                                 `---`                            
                                                                                

 
    """)

    parser = argparse.ArgumentParser(description='Process some URLs and payloads.')
    parser.add_argument('--payloads', required=True, help='Path to the payload file')
    parser.add_argument('--urls', required=True, help='Path to the URLs file')
    
    args = parser.parse_args()
    
    # Read URLs from file
    with open(args.urls, 'r') as url_file:
        # Extract the base URL until the '=' sign
        urls = [line.strip()[:line.strip().index('=') + 1] for line in url_file if '=' in line]

    # Read payloads from file
    with open(args.payloads, 'r') as payload_file:
        payloads = [line.strip() for line in payload_file]

    for url in urls:
        for payload in payloads:
            url_with_payload = url + payload
            response = send_payload(url_with_payload, payload)
            popup_triggered, alert_text = check_popup(url_with_payload, payload)
        
            if popup_triggered:
                print_in_color(f"URL: {url_with_payload}, Payload: {payload} triggered a popup with alert text: {alert_text}", Colors.RED)
                print()
            else:
                print_in_color(f"URL: {url_with_payload}, Payload: {payload} did not trigger a popup.", Colors.GREEN)
                print()
        
            time.sleep(10)
    # Quit the ChromeDriver instance after use
    if chrome_driver:
        chrome_driver.quit()
