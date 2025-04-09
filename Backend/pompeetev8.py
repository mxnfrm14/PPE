#!/usr/bin/env python3

import RPi.GPIO as GPIO
import time

def main():
    # Utiliser la numérotation BCM
    GPIO.setmode(GPIO.BCM)
    
    # Définir les numéros de GPIO14
    PIN_1 = 25  # Correspond au pin physique 32
    PIN_2 = 6   # Correspond au pin physique 31
    PIN_3 = 12  # Correspond au pin physique 32
    PIN_4 = 16

    
    # Configurer les pins comme sorties
    GPIO.setup(PIN_1, GPIO.OUT) #EV8
    GPIO.setup(PIN_2, GPIO.OUT) #pump
    GPIO.setup(PIN_3, GPIO.OUT) #EV11
    GPIO.setup(PIN_4, GPIO.OUT) #EV5
    
    try:
        # Allumer les deux pins (mettre à HIGH)
        print(f"Activation des GPIO {PIN_1} et {PIN_2} pendant 10 secondes...")
        GPIO.output(PIN_1, GPIO.LOW)
        GPIO.output(PIN_2, GPIO.HIGH) #pump
        GPIO.output(PIN_3, GPIO.LOW)
        GPIO.output(PIN_4, GPIO.HIGH)
        # Attendre 10 secondes
        time.sleep(9)
        
        # Éteindre les pins (mettre à LOW)2
        print(f"Désactivation des GPIO {PIN_1} et {PIN_2}")
        GPIO.output(PIN_1, GPIO.LOW)
        GPIO.output(PIN_2, GPIO.LOW)
        GPIO.output(PIN_3, GPIO.LOW)
        GPIO.output(PIN_4, GPIO.LOW)

        
    except KeyboardInterrupt:
        # Gérer l'interruption par Ctrl+C
        print("Opération annulée par l'utilisateur")
    finally:
        # Nettoyer les configurations GPIO
        GPIO.cleanup()
        print("Nettoyage GPIO terminé")

if __name__ == "__main__":
    main()