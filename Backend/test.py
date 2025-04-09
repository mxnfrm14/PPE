import RPi.GPIO as GPIO
import time

# Configuration
PIN = 13  # Numéro GPIO (et non le numéro physique)

# Setup
GPIO.setmode(GPIO.BCM)      # Utilise le numéro BCM (GPIO6)
GPIO.setup(PIN, GPIO.OUT)   # Définit la broche comme sortie

# Allumer la broche
GPIO.output(PIN, GPIO.HIGH)
print("GPIO 6 allumée")
time.sleep(5)  # Attend 5 secondes

# Éteindre la broche
GPIO.output(PIN, GPIO.LOW)
print("GPIO 6 éteinte")

# Nettoyage
GPIO.cleanup()
