import schedule
import time

def generate_report():

    print("Generating reports...")

schedule.every().day.at(
    "09:00"
).do(generate_report)

while True:

    schedule.run_pending()
    time.sleep(60)