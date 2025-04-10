#!/usr/bin/env python3
"""
water_plant.py - Script to control watering system GPIO pins on Raspberry Pi

Usage: python3 water_plant.py <valve_position> <duration> [watering_id]
"""

import sys
import time
import logging
import RPi.GPIO as GPIO
import requests

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("/var/log/e-garden/watering.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger("water_plant")

# Vérifiez que cette URL correspond exactement à votre configuration d'API
API_ENDPOINT = "http://localhost:8000/api/plant/watering/status/internal"

# GPIO pin for the water pump - will be activated with any valve
PUMP_GPIO = 6

# Mapping des positions aux GPIO pins des électrovannes
VALVE_MAPPING = {
    1: 4,    # Position 1 -> GPIO 4
    2: 17,   # Position 2 -> GPIO 17
    3: 27,   # Position 3 -> GPIO 27
    4: 22,   # Position 4 -> GPIO 22
    5: 16,   # Position 5 -> GPIO 16 (EV5)
    6: 5,    # Position 6 -> GPIO 5
    7: 26,   # Position 7 -> GPIO 26
    8: 23,   # Position 8 -> GPIO 23
    9: 24,   # Position 9 -> GPIO 24
    10: 25,  # Position 10 -> GPIO 25 (EV8)
    11: 12,  # Position 11 -> GPIO 12 (EV11)
    12: 16   # Position 12 -> GPIO 16 (partagé avec 5)
}

def setup_gpio():
    """Initialize GPIO settings"""
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)

def cleanup():
    """Clean up GPIO pins"""
    GPIO.cleanup()

def water_plant(position, duration):
    """
    Activate watering for the specified position, for the given duration
    
    Args:
        position (int): Position number (1-12) to activate
        duration (int): Duration in minutes to keep the pins active
    """
    if position not in VALVE_MAPPING:
        logger.error(f"Position invalide: {position}")
        return False
        
    valve_gpio_pin = VALVE_MAPPING[position]
    logger.info(f"Position {position} correspond au GPIO {valve_gpio_pin}")
    
    try:
        logger.info(f"Configuration des GPIO: électrovanne {valve_gpio_pin} et pompe {PUMP_GPIO}")
        GPIO.setup(valve_gpio_pin, GPIO.OUT)
        GPIO.setup(PUMP_GPIO, GPIO.OUT)
        
        # Activation de la pompe (HIGH) et de l'électrovanne (LOW pour activer)
        logger.info(f"Activation pompe (GPIO {PUMP_GPIO}) et électrovanne (GPIO {valve_gpio_pin}) pour {duration} minutes")
        GPIO.output(PUMP_GPIO, GPIO.HIGH)
        GPIO.output(valve_gpio_pin, GPIO.HIGH)  # Note: LOW pour activer conformément au code original
        
        
        time.sleep(duration)
        
        # Désactivation de la pompe et de l'électrovanne
        logger.info(f"Désactivation électrovanne (GPIO {valve_gpio_pin}) et pompe (GPIO {PUMP_GPIO})")
        GPIO.output(valve_gpio_pin, GPIO.LOW)
        GPIO.output(PUMP_GPIO, GPIO.LOW)
        
        logger.info(f"Arrosage terminé avec succès pour la position {position} (GPIO {valve_gpio_pin})")
        return True
    except Exception as e:
        logger.error(f"Erreur pendant l'arrosage: {str(e)}")
        # S'assurer que les pins sont éteints en cas d'erreur
        try:
            GPIO.output(valve_gpio_pin, GPIO.LOW)
            GPIO.output(PUMP_GPIO, GPIO.LOW)
        except:
            pass
        return False

def update_status(watering_id, success):
    """Update the watering status in the database via API call"""
    try:
        response = requests.post(
            API_ENDPOINT,
            params={"watering_id": watering_id, "success": success}
        )
        
        if response.status_code == 200:
            logger.info(f"Successfully updated watering status for ID {watering_id}")
        else:
            logger.error(f"Failed to update watering status: {response.status_code} - {response.text}")
    except Exception as e:
        logger.error(f"Error updating watering status: {str(e)}")

def main():
    if len(sys.argv) < 3:
        logger.error("Usage: python3 water_plant.py <position> <duration> [watering_id]")
        sys.exit(1)
    
    try:
        position = int(sys.argv[1])
        duration = int(sys.argv[2])
        watering_id = sys.argv[3] if len(sys.argv) > 3 else None
        
        setup_gpio()
        success = water_plant(position, duration)
        
        if watering_id:
            update_status(watering_id, success)
        
        cleanup()
        sys.exit(0 if success else 1)
        
    except ValueError:
        logger.error("La position et la durée doivent être des entiers")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Erreur inattendue: {str(e)}")
        cleanup()
        sys.exit(1)

if __name__ == "__main__":
    main()