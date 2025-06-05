from gpiozero import OutputDevice
import time
import math

PUL = OutputDevice(17)
DIR = OutputDevice(27)
ENA = OutputDevice(22)

ENA.off()

def snelheid_scurve(t, max_snelheid, totaal_stappen):
    verhouding = (t / totaal_stappen)
    if verhouding < 0.5:
        return max_snelheid * (2 * verhouding) ** 2
    else:
        return max_snelheid * (1 -2 * (1 - verhouding) ** 2)
        

def draai_stappen(aantal_stappen, richting=1, max_snelheid=0.002):
    DIR.value = 1 if richting == 1 else 0
    for t in range(aantal_stappen):
        snelheid = snelheid_scurve(t, max_snelheid, aantal_stappen)
        PUL.on()
        time.sleep(snelheid)
        PUL.off()
        time.sleep(snelheid)


try:
    print("start 1 toer")
    stappen_per_tafelrotatie = 6400 * 9
    draai_stappen(stappen_per_tafelrotatie, richting=1, max_snelheid=0.002)
    print("1 toer voltooid")
finally:
    ENA.on()