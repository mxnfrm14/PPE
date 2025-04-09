#!/usr/bin/env python3
"""
water_plant.py - Script to control watering system GPIO pins on Raspberry Pi

Usage: python3 water_plant.py <valve_gpio_pin> <duration_minutes> [watering_id]
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

def setup_gpio():
    """Initialize GPIO settings"""
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)

def cleanup():
    """Clean up GPIO pins"""
    GPIO.cleanup()

def water_plant(valve_gpio_pin, duration_minutes):
    """
    Activate watering for the specified valve GPIO pin and pump, for the given duration
    
    Args:
        valve_gpio_pin (int): GPIO pin number for the valve to activate
        duration_minutes (int): Duration in minutes to keep the pins active
    """
    try:
        logger.info(f"Setting up GPIO pins: valve {valve_gpio_pin} and pump {PUMP_GPIO} for watering")
        GPIO.setup(valve_gpio_pin, GPIO.OUT)
        GPIO.setup(PUMP_GPIO, GPIO.OUT)
        
        # Turn ON both the water pump and the specific valve
        logger.info(f"Turning ON pump (GPIO {PUMP_GPIO}) and valve (GPIO {valve_gpio_pin}) for {duration_minutes} minutes")
        GPIO.output(PUMP_GPIO, GPIO.HIGH)
        GPIO.output(valve_gpio_pin, GPIO.HIGH)
        
        # Wait for the specified duration
        duration_seconds = duration_minutes * 60
        time.sleep(duration_seconds)
        
        # Turn OFF both the water pump and the valve
        logger.info(f"Turning OFF valve (GPIO {valve_gpio_pin}) and pump (GPIO {PUMP_GPIO})")
        GPIO.output(valve_gpio_pin, GPIO.LOW)
        GPIO.output(PUMP_GPIO, GPIO.LOW)
        
        logger.info(f"Watering completed successfully for valve GPIO {valve_gpio_pin}")
        return True
    except Exception as e:
        logger.error(f"Error during watering process: {str(e)}")
        # Make sure to turn off the pins in case of error
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
        logger.error("Usage: python3 water_plant.py <valve_gpio_pin> <duration_minutes> [watering_id]")
        sys.exit(1)
    
    try:
        valve_gpio_pin = int(sys.argv[1])
        duration_minutes = int(sys.argv[2])
        watering_id = sys.argv[3] if len(sys.argv) > 3 else None
        
        setup_gpio()
        success = water_plant(valve_gpio_pin, duration_minutes)
        
        if watering_id:
            update_status(watering_id, success)
        
        cleanup()
        sys.exit(0 if success else 1)
        
    except ValueError:
        logger.error("GPIO pin and duration must be integers")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        cleanup()
        sys.exit(1)

if __name__ == "__main__":
    main()