from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time
import requests
import random
import csv
from urllib.parse import urlparse
import os
from urllib.parse import urlparse
import pandas as pd





options = Options()
# options.add_argument('--headless')
options.binary_location = r"C:\Program Files\Mozilla Firefox\firefox.exe"

# The Service object is no longer needed; Selenium will manage the driver automatically.
driver = webdriver.Firefox(options=options)
driver.maximize_window()
driver.get("https://www.instagram.com/")

wait = WebDriverWait(driver, 20)


username_input = wait.until(EC.visibility_of_element_located((By.NAME, "username")))
username_input.send_keys("hristijan.kolevski")

password_input = wait.until(EC.visibility_of_element_located((By.NAME, "password")))
password_input.send_keys("Defakto09999999999!")



login_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']")))
login_button.click()

second_child = WebDriverWait(driver, 40).until(
    EC.element_to_be_clickable((
        By.XPATH,
        "//div[contains(@class,'x1iyjqo2') and contains(@class,'xh8yej3') and @data-visualcompletion='ignore-dynamic']/div[2]"
    ))
)

driver.get("https://www.instagram.com/donapetreska/following/")

selenium_cookies = driver.get_cookies()
cookie_dict = {cookie['name']: cookie['value'] for cookie in selenium_cookies}
cookie_header = "; ".join(f"{name}={value}" for name, value in cookie_dict.items())

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:115.0) Gecko/20100101 Firefox/115.0",
    "X-IG-App-ID": "936619743392459",
    "X-CSRFToken": cookie_dict.get("csrftoken", ""),
    "Cookie": cookie_header,
    "Referer": "https://www.instagram.com/"
}

cookies = cookie_dict.copy()

# === API URLs ===
followers_url = "https://www.instagram.com/api/v1/friendships/1066997533/followers/"
following_url = "https://www.instagram.com/api/v1/friendships/1066997533/following/"

params = {
    "count": "100",
    "search_surface": "follow_list_page"
}

# === Get Following ===
following = []
next_max_id = None

while True:
    if next_max_id:
        params["max_id"] = next_max_id
    else:
        params.pop("max_id", None)

    response = requests.get(following_url, headers=headers, cookies=cookies, params=params)
    print("Following status:", response.status_code)

    try:
        data = response.json()
    except:
        print("Non-JSON response for following")
        print(response.text)
        break

    for user in data.get("users", []):
        following.append("https://www.instagram.com/" + user.get("username"))


    next_max_id = data.get("next_max_id")
    if not next_max_id:
        break

    time.sleep(random.uniform(.5, 2))





























following = list(set(following))

df = pd.DataFrame(following, columns=["profile_url"])
df.to_csv("new.csv", index=False, encoding="utf-8")
