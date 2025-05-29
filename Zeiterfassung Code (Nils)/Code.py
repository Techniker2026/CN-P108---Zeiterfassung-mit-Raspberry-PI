import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
from datetime import datetime
import csv
import os
import time

reader = SimpleMFRC522()
LOGFILE = "zeiterfassung.csv"

# Speichert den letzten Status pro UID: 'Kommen' oder 'Gehen'
status_speicher = {}

def erfasse_zeit(uid, status):
    now = datetime.now()
    datum = now.strftime("%Y-%m-%d")
    uhrzeit = now.strftime("%H:%M:%S")
    
    eintrag = [uid, datum, uhrzeit, status]

    file_exists = os.path.isfile(LOGFILE)
    with open(LOGFILE, mode='a', newline='') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(["UID", "Datum", "Uhrzeit", "Status"])
        writer.writerow(eintrag)
    print(f"[{datum} {uhrzeit}] {status} erfasst fuer UID: {uid}")

print("System bereit. Halte einen RFID-Chip an den Leser...")

try:
    letzte_uid = None
    while True:
        uid, _ = reader.read()
        if uid != letzte_uid:
            # Status bestimmen
            letzter_status = status_speicher.get(uid, "Gehen")  # Standard: zuletzt gegangen -> jetzt Kommen
            neuer_status = "Kommen" if letzter_status == "Gehen" else "Gehen"

            erfasse_zeit(uid, neuer_status)

            # Status aktualisieren
            status_speicher[uid] = neuer_status

            letzte_uid = uid

            # Warten bis Chip entfernt wurde
            print("Bitte Chip entfernen...")
            while True:
                try:
                    neuer_uid, _ = reader.read()
                    if neuer_uid != uid:
                        break
                except:
                    pass
        time.sleep(0.5)

except KeyboardInterrupt:
    GPIO.cleanup()
    print("Programm beendet.")
