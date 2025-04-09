#!/usr/bin/env python3

import RPi.GPIO as GPIO
import time

def main():
    # Utiliser la numérotation BCM
    GPIO.setmode(GPIO.BCM)
    
    # Définir les numéros de GPIO
    PIN_1 = 12  # Correspond au pin physique 32
    PIN_2 = 6   # Correspond au pin physique 31
    
    # Configurer les pins comme sorties
    GPIO.setup(PIN_1, GPIO.OUT)
    GPIO.setup(PIN_2, GPIO.OUT)
    
    try:
        # Allumer les deux pins (mettre à HIGH)
        print(f"Activation des GPIO {PIN_1} et {PIN_2} pendant 10 secondes...")
        GPIO.output(PIN_1, GPIO.HIGH)
        GPIO.output(PIN_2, GPIO.HIGH)
        
        # Attendre 10 secondes
        time.sleep(10)
        
        # Éteindre les pins (mettre à LOW)
        print(f"Désactivation des GPIO {PIN_1} et {PIN_2}")
        GPIO.output(PIN_1, GPIO.LOW)
        GPIO.output(PIN_2, GPIO.LOW)
        
    except KeyboardInterrupt:
        # Gérer l'interruption par Ctrl+C
        print("Opération annulée par l'utilisateur")
    finally:
        # Nettoyer les configurations GPIO
        GPIO.cleanup()
        print("Nettoyage GPIO terminé")

if __name__ == "__main__":
    main()
