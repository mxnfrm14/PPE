#!/usr/bin/env python3

import RPi.GPIO as GPIO
import time

def main():
    # Use BCM GPIO numbering
    GPIO.setmode(GPIO.BCM)
    
    # Set up GPIO pin 4 as output
    GPIO_PIN = 4
    GPIO.setup(GPIO_PIN, GPIO.OUT)
    
    try:
        # Set pin 4 to HIGH (3.3V)
        print(f"Setting GPIO pin {GPIO_PIN} HIGH for 10 seconds...")
        GPIO.output(GPIO_PIN, GPIO.HIGH)
        
        # Wait for 10 seconds
        time.sleep(10)
        
        # Set pin 4 back to LOW (0V)
        print(f"Setting GPIO pin {GPIO_PIN} LOW")
        GPIO.output(GPIO_PIN, GPIO.LOW)
        
    finally:
        # Clean up GPIO settings
        GPIO.cleanup()
        print("GPIO cleanup completed")

if __name__ == "__main__":
    main()