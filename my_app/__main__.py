
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time
import requests
import random

# === Setup Firefox options and service ===
options = Options()
options.add_argument('--headless')
options.binary_location = r"C:\Program Files\Mozilla Firefox\firefox.exe"  # Firefox path
service = Service(r"C:\Program Files\geckodriver.exe")  # Your geckodriver.exe path

driver = webdriver.Firefox(service=service, options=options)
driver.maximize_window()
driver.get("https://www.instagram.com/")

wait = WebDriverWait(driver, 20)

# === Login ===
username_input = wait.until(EC.visibility_of_element_located((By.NAME, "username")))
username_input.send_keys("hristijan.kolevski")

password_input = wait.until(EC.visibility_of_element_located((By.NAME, "password")))
password_input.send_keys("Defakto0999999!")

# === Open Instagram ===

login_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']")))
login_button.click()

# === Handle "Not now" popup (save login info) ===
try:
    not_now_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Not Now')]")))
    not_now_button.click()
except:
    pass  # Popup didn't show up, continue

# === Go to profile ===
profile_link = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(@href, '/hristijan.kolevski/')]")))
profile_link.click()

# === Click followers ===
followers_link = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(@href, '/followers/')]")))

driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", followers_link)


try:
    # Try normal click first
    followers_link.click()
except:
    # Fallback to JS click if normal click fails
    driver.execute_script("arguments[0].click();", followers_link)

# === Cookies & Headers ===
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
followers_url = "https://www.instagram.com/api/v1/friendships/1505566833/followers/"
following_url = "https://www.instagram.com/api/v1/friendships/1505566833/following/"

params = {
    "count": "100",
    "search_surface": "follow_list_page"
}

# === Get Followers ===
followers = []
next_max_id = None

while True:
    if next_max_id:
        params["max_id"] = next_max_id
    else:
        params.pop("max_id", None)

    response = requests.get(followers_url, headers=headers, cookies=cookies, params=params)
    print("Followers status:", response.status_code)

    try:
        data = response.json()
    except:
        print("Non-JSON response for followers")
        print(response.text)
        break

    for user in data.get("users", []):
        followers.append("https://www.instagram.com/" + user.get("username"))
        print("Follower:", user.get("username"))

    next_max_id = data.get("next_max_id")
    if not next_max_id:
        break

    time.sleep(random.uniform(.5, 2))

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
        print("Following:", user.get("username"))

    next_max_id = data.get("next_max_id")
    if not next_max_id:
        break

    time.sleep(random.uniform(.5, 2))

# === Result ===
not_following_back = [user for user in following if user not in followers]

print("\n=== Not following you back ===\n\n\n")
for user in not_following_back:
    print(user)

# === Done ===

driver.quit()

