import requests
import random
import string
import time
import imapclient
import email
from bs4 import BeautifulSoup

# ✅ Your Email Credentials (Yandex or Gmail)
EMAIL_ACCOUNT = "your-email@example.com"
EMAIL_PASSWORD = "your-email-password"

# ✅ Generate Random Email
def random_email():
    return "fb" + ''.join(random.choices(string.ascii_lowercase + string.digits, k=10)) + "@yandex.com"

# ✅ Generate Unique Random Password
def random_password():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=12))

# ✅ Facebook Registration URL
FB_REGISTER_URL = "https://m.facebook.com/reg"

# ✅ Function to Create Facebook Account
def create_facebook_account():
    email = random_email()
    password = random_password()  # Generate a unique password for each account
    name = random.choice(["John", "David", "Michael", "Chris"]) + " " + random.choice(["Smith", "Johnson", "Brown", "Williams"])

    session = requests.Session()
    headers = {"User-Agent": "Mozilla/5.0 (Linux; Android 10) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.101 Mobile Safari/537.36"}

    response = session.get(FB_REGISTER_URL, headers=headers)

    if response.status_code == 200:
        print(f"🔹 Creating account: {email} | {password}")
        payload = {
            "firstname": name.split()[0],
            "lastname": name.split()[1],
            "email": email,
            "password": password,
            "birthday_day": str(random.randint(1, 28)),
            "birthday_month": str(random.randint(1, 12)),
            "birthday_year": str(random.randint(1980, 2005)),
            "gender": random.choice(["1", "2"]),  # 1 = Female, 2 = Male
            "terms": "on",
            "submit": "Sign Up"
        }

        register_response = session.post(FB_REGISTER_URL, data=payload, headers=headers)

        if "checkpoint" in register_response.url:
            print("⚠️ Account created but needs verification (Checkpoint).")
            return None
        elif "confirmemail" in register_response.url:
            print("✅ Account created! Verifying email...")
            otp = get_email_otp(email)
            if otp:
                verify_facebook_otp(session, otp)
                print("✅ Email verified successfully!")
                with open("created_accounts.txt", "a") as file:
                    file.write(f"{email} | {password}\n")
            else:
                print("❌ Failed to verify email.")
        else:
            print("❌ Failed to create account.")

# ✅ Function to Fetch OTP from Email
def get_email_otp(target_email):
    print(f"📩 Checking email for OTP: {target_email}")
    imap_server = "imap.yandex.com"  # Change to "imap.gmail.com" if using Gmail
    try:
        client = imapclient.IMAPClient(imap_server, ssl=True)
        client.login(EMAIL_ACCOUNT, EMAIL_PASSWORD)
        client.select_folder("INBOX")

        messages = client.search(["UNSEEN"])
        for msg_id in messages:
            raw_msg = client.fetch(msg_id, ["RFC822"])[msg_id][b"RFC822"]
            msg = email.message_from_bytes(raw_msg)

            if target_email in msg["To"]:
                content = msg.get_payload(decode=True).decode("utf-8")
                otp = extract_otp(content)
                if otp:
                    print(f"✅ OTP Found: {otp}")
                    return otp
        print("❌ No OTP found.")
    except Exception as e:
        print(f"❌ Email Fetch Error: {e}")
    return None

# ✅ Function to Extract OTP from Email Content
def extract_otp(content):
    soup = BeautifulSoup(content, "html.parser")
    text = soup.get_text()
    otp = "".join(filter(str.isdigit, text))
    return otp[:6] if otp else None

# ✅ Function to Submit OTP to Facebook
def verify_facebook_otp(session, otp):
    verify_url = "https://m.facebook.com/confirmemail"
    data = {"otp": otp, "submit": "Verify"}
    session.post(verify_url, data=data)
    print("✅ OTP Submitted!")

# ✅ Bulk Account Creation
num_accounts = int(input("Enter number of accounts to create: "))
for _ in range(num_accounts):
    create_facebook_account()
    time.sleep(5)  # Wait before creating the next account
