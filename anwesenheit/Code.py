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

# Speichert die letzte Lesezeit pro UID
letzte_lesezeit = {}

# Minimale Pause zwischen zwei Scans desselben Chips (Sekunden)
MIN_PAUSE = 3

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
    while True:
        try:
            uid, _ = reader.read()
        except Exception:
            # Fehler beim Lesen ignorieren
            time.sleep(0.5)
            continue

        jetzt = time.time()
        letzte_zeit = letzte_lesezeit.get(uid, 0)

        # Nur wenn seit letztem Scan MIN_PAUSE Sekunden vergangen sind
        if jetzt - letzte_zeit > MIN_PAUSE:
            letzter_status = status_speicher.get(uid, "Gehen")  # Falls noch kein Eintrag, dann "Gehen"
            neuer_status = "Kommen" if letzter_status == "Gehen" else "Gehen"

            erfasse_zeit(uid, neuer_status)

            status_speicher[uid] = neuer_status
            letzte_lesezeit[uid] = jetzt

            print("Bitte Chip entfernen oder kurz warten...")

            # Hier keine Schleife, damit der gleiche Chip sofort wieder gelesen werden kann
        time.sleep(0.5)

except KeyboardInterrupt:
    GPIO.cleanup()
    print("Programm beendet.")

