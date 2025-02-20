import requests
import random
from Tools.scripts.generate_opcode_h import header
import time
import urllib.parse
import imaplib
import email
from email.header import decode_header
import re
import concurrent.futures
import json
import os


def load_json():
    with open('config.json', 'r') as f:
        config = json.load(f)

    capsolver = config["capsolver"]
    quantity = config["quantity"]
    threads = config["threads"]
    imapuser = config["imapuser"]
    imappass = config["imappass"]
    ref = config["ref"]


def get_link(toaddress):
    IMAP_SERVER = "imap.gmail.com"
    EMAIL_ACCOUNT = imapuser
    EMAIL_PASSWORD = imappass
    mail = imaplib.IMAP4_SSL(IMAP_SERVER)
    mail.login(EMAIL_ACCOUNT, EMAIL_PASSWORD)
    mail.select("inbox")


    search_criteria = f'(TO "{toaddress}" SUBJECT "Email Verification" UNSEEN)'
    status, messages = mail.search(None, search_criteria)

    email_ids = messages[0].split()

    if not email_ids:
        return 1
    else:
        latest_email_id = email_ids[-1]

        status, msg_data = mail.fetch(latest_email_id, "(RFC822)")

        for response_part in msg_data:
            if isinstance(response_part, tuple):
                msg = email.message_from_bytes(response_part[1])
                email_subject = decode_header(msg["Subject"])[0][0]
                if isinstance(email_subject, bytes):
                    email_subject = email_subject.decode()


                email_body = None

                if msg.is_multipart():
                    for part in msg.walk():
                        content_type = part.get_content_type()
                        content_disposition = str(part.get("Content-Disposition"))
                        charset = part.get_content_charset()


                        if content_type == "text/plain" and "attachment" not in content_disposition:
                            payload = part.get_payload(decode=True)
                            if payload:
                                try:
                                    email_body = payload.decode(charset or "utf-8")  # Use detected charset
                                except (UnicodeDecodeError, TypeError):
                                    email_body = payload.decode("iso-8859-1")  # Fallback encoding
                            break
                else:
                    payload = msg.get_payload(decode=True)
                    charset = msg.get_content_charset()
                    if payload:
                        try:
                            email_body = payload.decode(charset or "utf-8")
                        except (UnicodeDecodeError, TypeError):
                            email_body = payload.decode("iso-8859-1")

                if email_body:

                    verification_link_pattern = (
                        r"https:\/\/verify\.dawninternet\.com\/chromeapi\/dawn\/v1\/userverify\/verifyconfirm\?key=[a-zA-Z0-9-]+"
                    )
                    verification_link = re.search(verification_link_pattern, email_body)
                    link = verification_link.group()

                    if verification_link:
                        parsed_url = urllib.parse.urlparse(link)
                        key_value = urllib.parse.parse_qs(parsed_url.query)["key"][0]

                    else:
                        print("Verification link not found.")

                else:
                    print("Could not extract email body.")


                mail.store(latest_email_id, '+FLAGS', '\\Seen')
                return key_value


def get_name():
    namelist = ['Uma', 'Uma', 'Frank', 'Karl', 'Eve', 'Karl', 'Eve', 'Paul', 'Walter', 'Yara', 'Ivan', 'Sam', 'Grace', 'Ivan', 'Walter', 'Tom', 'Vera', 'Vera', 'Mona', 'Quinn', 'Sam', 'Vera', 'Eve', 'Uma', 'Uma', 'Zane', 'Charlie', 'Eve', 'Rita', 'Yara', 'Bob', 'Heidi', 'Zane', 'Bob', 'Bob', 'Alice', 'Oscar', 'Grace', 'Karl', 'Judy', 'Vera', 'Liam', 'Xander', 'Walter', 'Liam', 'Vera', 'Quinn', 'Uma', 'Xander', 'Walter', 'Zane', 'Bob', 'Frank', 'Karl', 'Zane', 'Bob', 'Bob', 'Paul', 'Liam', 'Yara', 'Rita', 'Nina', 'Vera', 'Xander', 'Ivan', 'Frank', 'Nina', 'David', 'Alice', 'Mona', 'Judy', 'Eve', 'Walter', 'Charlie', 'Tom', 'Rita', 'Walter', 'Nina', 'Alice', 'Grace', 'David', 'Sam', 'David', 'David', 'Grace', 'Nina', 'Oscar', 'Heidi', 'Uma', 'Heidi', 'Zane', 'Liam', 'Frank', 'Heidi', 'Walter', 'Eve', 'Grace', 'Eve', 'Zane', 'Heidi', 'Ivan', 'Ivan', 'Nina', 'Karl', 'Liam', 'David', 'Frank', 'Oscar', 'Tom', 'Nina', 'Alice', 'Zane', 'Zane', 'Eve', 'Tom', 'Yara', 'Alice', 'David', 'Walter', 'Paul', 'Nina', 'Judy', 'Xander', 'Tom', 'Alice', 'Karl', 'Karl', 'Nina', 'Walter', 'Paul', 'Oscar', 'Heidi', 'Ivan', 'Bob', 'Karl', 'Quinn', 'Karl', 'Xander', 'Yara', 'Walter', 'Vera', 'Grace', 'Sam', 'Judy', 'Karl', 'Charlie', 'Sam', 'Vera', 'Alice', 'Frank', 'Nina', 'Frank', 'Oscar', 'Rita', 'Walter', 'Vera', 'Rita', 'Liam', 'Charlie', 'Karl', 'Paul', 'Karl', 'Paul', 'Yara', 'Grace', 'Heidi', 'Quinn', 'Uma', 'Sam', 'Heidi', 'Charlie', 'Oscar', 'Judy', 'Zane', 'Ivan', 'Walter', 'Judy', 'Frank', 'Uma', 'Karl', 'Vera', 'Alice', 'Bob', 'Grace', 'Eve', 'Mona', 'Vera', 'Frank', 'Sam', 'Frank', 'Rita', 'Vera', 'Alice', 'Heidi', 'Uma', 'Rita', 'Quinn', 'Walter', 'Quinn', 'Ivan', 'David', 'Rita', 'Nina', 'Oscar', 'Yara', 'Uma', 'Grace', 'Sam', 'Vera', 'Eve', 'Heidi', 'David', 'Frank', 'Nina', 'Heidi', 'Sam', 'Quinn', 'Walter', 'Quinn', 'Nina', 'Mona', 'Paul', 'Oscar', 'David', 'Judy', 'Ivan', 'Vera', 'Charlie', 'Eve', 'Bob', 'Xander', 'Zane', 'Liam', 'Uma', 'Rita', 'Tom', 'Nina', 'Zane', 'Judy', 'Zane', 'Tom', 'Karl', 'Frank', 'Paul', 'Mona', 'Bob', 'Uma', 'Mona', 'Sam', 'Zane', 'Karl', 'Uma', 'Grace', 'Frank', 'Oscar', 'Sam', 'David', 'Grace', 'Sam', 'Bob', 'David', 'Heidi', 'David', 'Tom', 'Grace', 'Rita', 'Liam', 'Oscar', 'Nina', 'Charlie', 'Oscar', 'Rita', 'Frank', 'Xander', 'Quinn', 'Heidi', 'Alice', 'Charlie', 'Quinn', 'Rita', 'Bob', 'Eve', 'Ivan', 'Zane', 'Mona', 'Karl', 'Karl', 'Frank', 'Judy', 'Quinn', 'Xander', 'Quinn', 'Nina', 'Xander', 'Zane', 'Eve', 'Paul', 'Rita', 'Grace', 'Walter', 'Eve', 'Vera', 'Zane', 'Bob', 'Sam', 'Heidi', 'Sam', 'Rita', 'Eve', 'Walter', 'Vera', 'Vera', 'Vera', 'Tom', 'Grace', 'Liam', 'David', 'Charlie', 'Vera', 'Eve', 'David', 'Yara', 'Judy', 'Vera', 'Xander', 'Liam', 'Judy', 'Nina', 'Eve', 'Xander', 'Paul', 'Judy', 'Charlie', 'Walter', 'Heidi', 'Paul', 'Karl', 'Zane', 'Rita', 'Judy', 'Eve', 'Vera', 'Karl', 'Uma', 'Karl', 'Frank', 'Ivan', 'Grace', 'David', 'Mona', 'Mona', 'Zane', 'Alice', 'Heidi', 'Ivan', 'Uma', 'Judy', 'Mona', 'Walter', 'Quinn', 'Vera', 'Heidi', 'Zane', 'Ivan', 'Vera', 'Eve', 'Judy', 'Quinn', 'Liam', 'Rita', 'Bob', 'Uma', 'Paul', 'Mona', 'Charlie', 'Walter', 'Judy', 'Frank', 'Vera', 'Yara', 'Judy', 'Quinn', 'Karl', 'Yara', 'Heidi', 'Tom', 'David', 'Sam', 'Karl', 'Ivan', 'Zane', 'David', 'Paul', 'Zane', 'Zane', 'Eve', 'Quinn', 'Tom', 'Paul', 'Tom', 'Walter', 'Walter', 'Judy', 'Paul', 'Oscar', 'Charlie', 'Sam', 'David', 'Charlie', 'Alice', 'David', 'Zane', 'Tom', 'Heidi', 'Zane', 'Sam', 'Mona', 'Bob', 'Alice', 'Xander', 'Eve', 'Grace', 'Rita', 'Zane', 'David', 'Oscar', 'Tom', 'Quinn', 'Frank', 'Alice', 'Grace', 'Rita', 'Nina', 'Liam', 'Liam', 'Xander', 'Zane', 'Grace']
    return namelist[random.randint(0,len(namelist))]

def get_password():
    passwrd = get_name()+get_name()+str(random.randint(1,100))+"!"
    return passwrd

def verify_acct(key,token,prox):
    headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'en-US,en;q=0.9',
        'content-type': 'application/json',
        'dnt': '1',
        'origin': 'https://dashboard.dawninternet.com',
        'priority': 'u=1, i',
        'referer': 'https://dashboard.dawninternet.com/',
        'sec-ch-ua': '"Not(A:Brand";v="99", "Google Chrome";v="133", "Chromium";v="133"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36',
    }

    json_data = {
        'token': token,
    }
    params = {
        'key' : key
    }

    response = requests.post(
        "https://verify.dawninternet.com/chromeapi/dawn/v1/userverify/verifycheck",
        headers=headers,
        params=params,
        json=json_data,
        proxies=prox
    )
    if response.status_code == 200:
        print("Successfully Verfied!")
        return 1
    else:
        print("Error Verifying mail :(")
        print(response.status_code)



def get_task_id(url,key):
    data ={
        "clientKey": capsolver,
        "task": {
            "type": "AntiTurnstileTaskProxyLess",
            "websiteURL": url,
            "websiteKey": key,
        }
    }
    r = requests.post("https://api.capsolver.com/createTask",json=data)
    r_json = r.json()
    return r_json['taskId']

def solve_captcha(id):
    i=0
    data = {
        "clientKey": capsolver,
        "taskId": id
    }
    r = requests.post("https://api.capsolver.com/getTaskResult",json = data)
    time.sleep(3.5)
    r_json = r.json()
    i = 0
    while (r_json['status']== "processing"):
        print("Processing...")
        time.sleep(1.5)
        data = {
            "clientKey": capsolver,
            "taskId": id
        }
        r = requests.post("https://api.capsolver.com/getTaskResult", json=data)
        r_json = r.json()
        i+=1
        if (i>10):
            print("timed out")
            break
    return r_json['solution']['token']

def get_proxy():
    with open("proxies.txt", "r") as file:
        lines = [line.strip() for line in file.readlines()]
    return lines

def get_mail():
    with open("emails.txt", "r") as file:
        lines = [line.strip() for line in file.readlines()]
    return lines

def add_info(email,password,proxy):
    with open('output.txt', 'a') as file:
        file.write(email+":"+password+":"+proxy+"\n")


def format_proxy(proxy_string):
    parts = proxy_string.split(':')

    if len(parts) != 4:
        raise ValueError("Proxy must be in the format ip:port:user:pass")

    ip = parts[0]
    port = parts[1]
    user = parts[2]
    password = parts[3]

    formatted_proxy = {
        'http': f'http://{user}:{password}@{ip}:{port}'
    }

    return formatted_proxy

def getappid():
    r = requests.get('https://ext-api.dawninternet.com/chromeapi/dawn/v1/appid/getappid?app_v=1.1.7')
    rjson = r.json()
    if r.status_code ==200:
        return rjson['data']['appid']
    else:
        print("Failed getting app id")

def send_request(passwrd,token,mail,proxy,appid):
    headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'en-US,en;q=0.9',
        'content-type': 'application/json',
        'dnt': '1',
        'origin': 'https://dashboard.dawninternet.com',
        'priority': 'u=1, i',
        'referer': 'https://dashboard.dawninternet.com/',
        'sec-ch-ua': '"Not(A:Brand";v="99", "Google Chrome";v="133", "Chromium";v="133"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36',
    }

    params = {
        'appid': appid,
    }
    tok = (urllib.parse.quote(str(token)))


    json_data = {
        'firstname': get_name(),
        'lastname': get_name(),
        'email': mail,
        'mobile': '',
        'country': 'GB',
        'password': passwrd,
        'referralCode': ref,
        'token': tok,
        'isMarketing': False,
        'browserName': 'chrome',
    }


    response = requests.post("https://ext-api.dawninternet.com/chromeapi/dawn/v2/dashboard/user/validate-register",
        headers=headers,
        params=params,
        json=json_data,
        proxies=proxy
    )
    if response.status_code == 200:
        return 1
    else:
        print(f'Error code: ',response.status_code)


def process_account(j):
    emails = get_mail()
    proxies = get_proxy()

    if j >= len(emails) or j >= len(proxies):
        print(f"Skipping index {j}: Not enough emails or proxies.")
        return

    email = emails[j]
    prox = proxies[j]
    fprox = format_proxy(prox)
    password = get_password()

    tokenn = solve_captcha(get_task_id("https://dashboard.dawninternet.com/signup", "0x4AAAAAAA48wVDquA-98fyV"))

    if send_request(password, tokenn, email, fprox, getappid()):
        print(f"Successfully Made Account! Email: {email}")
        print("Now verifying...")
        time.sleep(7)

        for attempt in range(5):
            link = get_link(email)
            if link != 1:
                break
            print("Mail didn't send yet, retrying...")
            time.sleep(2)

        if link != 1 and verify_acct(link, solve_captcha(
                get_task_id("https://verify.dawninternet.com/chromeapi/dawn/v1/userverify/verifycheck",
                            "0x4AAAAAAA48wVDquA-98fyV")), fprox):
            print("Genned Successfully!")
            add_info(email, password,prox)
        else:
            print("Verification failed!")
    else:
        print("FAILED!!")


def main():
    mquantity = quantity
    max_threads = threads

    with concurrent.futures.ThreadPoolExecutor(max_threads) as executor:
        executor.map(process_account, range(mquantity))


if __name__ == '__main__':
    with open('config.json', 'r') as f:
        config = json.load(f)

    capsolver = config["capsolver"]
    quantity = config["quantity"]
    threads = config["threads"]
    imapuser = config["imapuser"]
    imappass = config["imappass"]
    main()
    input("Press enter to close program")
