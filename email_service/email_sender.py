import yagmail

def send_report(receiver):

    yag = yagmail.SMTP(
        "your_email@gmail.com",
        "app_password"
    )

    yag.send(
        to=receiver,
        subject="Data Quality Report",
        contents="Attached report",
        attachments="reports/quality_report.pdf"
    )