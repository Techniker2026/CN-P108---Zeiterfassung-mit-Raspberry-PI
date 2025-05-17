import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
from datetime import datetime
import csv
import os

reader = SimpleMFRC522()
LOGFILE = "zeiterfassung.csv"

def erfasse_zeit(uid):
    now = datetime.now()
    datum = now.strftime("%Y-%m-%d")
    uhrzeit = now.strftime("%H:%M:%S")
    
    eintrag = [uid, datum, uhrzeit]

    file_exists = os.path.isfile(LOGFILE)
    with open(LOGFILE, mode='a', newline='') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(["UID", "Datum", "Uhrzeit"])
        writer.writerow(eintrag)
    print(f"[{datum} {uhrzeit}] Erfasst UID: {uid}")

print("Bereit zur Zeiterfassung. Halte einen RFID-Chip an den Leser...")

try:
    while True:
        uid, _ = reader.read()
        erfasse_zeit(uid)
except KeyboardInterrupt:
    GPIO.cleanup()
    print("Programm beendet.")

