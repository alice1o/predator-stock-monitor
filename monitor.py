
import os
import json
import smtplib
import requests
from bs4 import BeautifulSoup
from email.message import EmailMessage

# 監控的 Predator 球桿
PRODUCT_URL = (
    "https://int.predatorcues.com/collections/"
    "modern-pool-cues/products/"
    "predator-panthera-10-2-balam-pool-cue-leather-wrap"
)

STATE_FILE = "state.json"


def check_stock():
    headers = {"User-Agent": "Mozilla/5.0"}

    # 取得商品資料
    response = requests.get(
        PRODUCT_URL + ".js",
        headers=headers,
        timeout=30
    )
    response.raise_for_status()
    product = response.json()

    available = any(
        variant.get("available", False)
        for variant in product.get("variants", [])
    )

    # 檢查商品頁是否仍顯示 Coming Soon
    page = requests.get(
        PRODUCT_URL,
        headers=headers,
        timeout=30
    )
    page.raise_for_status()

    soup = BeautifulSoup(page.text, "html.parser")
    main = soup.select_one("main")
    text = main.get_text(" ", strip=True).lower() if main else ""

    coming_soon = "coming soon" in text

    return available and not coming_soon


def send_email():
    msg = EmailMessage()
    msg["Subject"] = "Predator Panthera 球桿開賣通知！"
    msg["From"] = os.environ["EMAIL_USER"]
    msg["To"] = os.environ["EMAIL_TO"]

    msg.set_content(
        "你關注的 Predator Panthera 10-2 Balam "
        "Leather Wrap 可能已經開賣！\n\n"
        "立即查看商品：\n"
        + PRODUCT_URL
        + "\n\n請以官網實際購買狀態為準。"
    )

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(
            os.environ["EMAIL_USER"],
            os.environ["EMAIL_APP_PASSWORD"]
        )
        smtp.send_message(msg)


def main():
    state = {}

    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r") as file:
            state = json.load(file)

    available = check_stock()
    notified = state.get("notified", False)

    if available and not notified:
        send_email()
        notified = True
        print("可能已開賣！通知 Email 已寄出。")

    elif available:
        print("商品可購買，之前已通知過。")

    else:
        notified = False
        print("目前尚未確認開賣。")

    with open(STATE_FILE, "w") as file:
        json.dump({"notified": notified}, file)


if __name__ == "__main__":
    main()
