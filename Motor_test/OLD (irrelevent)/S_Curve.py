from gpiozero import OutputDevice
import time
import math

PUL = OutputDevice(17)
DIR = OutputDevice(27)
ENA = OutputDevice(22)

ENA.off()

def s_curve(t, total_steps):
    """ Geeft een S-curve waarde tussen 0 en 1 gebaseerd op cosine functie """
    return 0.5 * (1 - math.cos(math.pi * t / total_steps))

def draai_stappen_s_curve(aantal_stappen, min_snelheid, max_snelheid, richting=1, accel_stappen=200):
    DIR.value = 1 if richting == 1 else 0

    if 2 * accel_stappen > aantal_stappen:
        accel_stappen = aantal_stappen // 2

    const_snelheid_stappen = aantal_stappen - 2 * accel_stappen

    # Acceleratie met S-curve
    for i in range(accel_stappen):
        f = s_curve(i, accel_stappen)
        snelheid = min_snelheid + f * (max_snelheid - min_snelheid)
        PUL.on()
        time.sleep(snelheid)
        PUL.off()
        time.sleep(snelheid)

    # Constante snelheid
    for _ in range(const_snelheid_stappen):
        PUL.on()
        time.sleep(max_snelheid)
        PUL.off()
        time.sleep(max_snelheid)

    # Deceleratie met S-curve
    for i in range(accel_stappen):
        f = s_curve(i, accel_stappen)
        snelheid = max_snelheid + f * (min_snelheid - max_snelheid)
        PUL.on()
        time.sleep(snelheid)
        PUL.off()
        time.sleep(snelheid)

try:
    stappen_per_tafelrotatie = 3200 * 9
    min_snelheid = 0.0009  # Langzaam begin/eind
    max_snelheid = 0.0001  # Snelste punt
    accel_stappen = 4000

    start = time.time()
    draai_stappen_s_curve(
        aantal_stappen=stappen_per_tafelrotatie,
        min_snelheid=min_snelheid,
        max_snelheid=max_snelheid,
        richting=1,
        accel_stappen=accel_stappen
    )
    end = time.time()
    print("1 toer voltooid in", round(end - start, 2), "seconden")

except KeyboardInterrupt:
    print("\nOnderbroken met Ctrl+C! Motor wordt uitgeschakeld...")

finally:
    ENA.on()
    print("ENA is weer hoog gezet (motor uit)")
