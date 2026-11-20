
import os
import smtplib
from email.message import EmailMessage

# 建立測試信件
msg = EmailMessage()
msg["Subject"] = "Predator 球桿監控 - Email 測試成功"
msg["From"] = os.environ["EMAIL_USER"]
msg["To"] = os.environ["EMAIL_TO"]

msg.set_content(
    "這是一封 Predator 球桿監控測試信！\n\n"
    "如果你收到這封信，代表 GitHub 可以透過 Gmail 寄送通知。\n\n"
    "監控商品：Predator Panthera 10-2 Balam Leather Wrap\n\n"
    "這只是測試信，不代表商品已經開賣。"
)

# 透過 Gmail 寄送
with smtplib.SMTP_SSL("smtp.gmail.com", 465, timeout=30) as smtp:
    smtp.login(
        os.environ["EMAIL_USER"],
        os.environ["EMAIL_APP_PASSWORD"]
    )
    smtp.send_message(msg)

print("測試信已成功送交 Gmail 寄送！")
