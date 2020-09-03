import os

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def send_email_html_format(subject, recipients, body_text, attachment_file=None):
    """This script sends email in html format; this also supports attachments"""
    from email.mime.multipart import MIMEMultipart
    from email.mime.image import MIMEImage
    from email.mime.text import MIMEText
    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = os.getenv('GMAIL_ID')
    recipients = recipients
    msg['To'] = ", ".join(recipients)
    body = body_text
    msg.attach(MIMEText(body, 'html'))
    if attachment_file:
        with open(attachment_file, 'r') as fp:
            file = MIMEText(fp.read())
        msg.attach(file)
    send_email(msg)

def send_email(msg):
    #  get gmail login info
    import smtplib
    try:
        server = smtplib.SMTP( "smtp.gmail.com", 587 ) # add these 2 to .yml as well
        server.starttls()
        server.login(os.getenv('GMAIL_ID'), os.getenv('GMAIL_PWD'))
        server.send_message(msg)
        server.quit()
        print(f"Email sent successfully!")
    except Exception as e:
        print(f"Unable to send email! {e}")

def get_latest_price(item, headless=True):

    try:
        chrome_options = Options()
        if headless:
            chrome_options.add_argument('--headless')
            chrome_options.add_argument('--disable-gpu')
            chrome_options.add_argument('--no-sandbox')
        driver = webdriver.Chrome(options=chrome_options)
        driver.implicitly_wait(10)
        print(f"Searching {item['item_desc']}")
        driver.get(item["item_url"])
        if item["store_name"].lower() == 'amazon':
            element = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, "//*[@id='priceblock_dealprice' or @id='priceblock_ourprice' or @id='priceblock_saleprice']")))
        # else:
        #     element = WebDriverWait(driver, 30).until(
        #     EC.presence_of_element_located((By.XPATH, "//div[@class='StandardPriceBlock']/div/span[@class='notranslate']")))
        string_price = element.text.strip()
        print(string_price)
        price = string_price
        target_price = item["target_price"]
        if float(price.strip('$')) < float(target_price):
            print(f"Price {price} is below target price of: ${target_price}")
            print("Sending email....")
            subject = f"""Price Alert for - {item["item_desc"]}"""
            body_text = f"""Price {price} is below target price of: ${target_price} for {item["item_desc"]}"""
            send_email_html_format(subject=subject,recipients=[os.getenv('GMAIL_ID')],body_text=body_text)
        else:
            print(f"Price {price} is above target price of: ${target_price}")
    except Exception as e:
        print(f"Something went wrong while searching.. Details: {e}")
        price = None
    finally:
        driver.quit()
    return price