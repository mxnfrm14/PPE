import RPi.GPIO as GPIO
import time

# Set the GPIO mode to BCM
GPIO.setmode(GPIO.BCM)

# Define the GPIO pin number
PUMP_PIN = 12

# Set up the GPIO pin as an output
GPIO.setup(PUMP_PIN, GPIO.OUT)

def activate_pump(duration=10):
    """
    Activate the pump by setting GPIO 6 to HIGH for the specified duration.
    
    Args:
        duration (int): Time in seconds to keep the pump on. Default is 10 seconds.
    """
    try:
        print(f"Turning pump ON for {duration} seconds...")
        
        # Set the GPIO pin to HIGH (3.3V) to activate the pump
        GPIO.output(PUMP_PIN, GPIO.LOW)
        
        # Wait for the specified duration
        time.sleep(duration)
        
        # Set the GPIO pin to LOW (0V) to deactivate the pump
        GPIO.output(PUMP_PIN, GPIO.HIGH)
        
        print("Pump turned OFF")
    
    except KeyboardInterrupt:
        # Handle Ctrl+C gracefully
        print("Operation canceled by user")
    #finally:
        # Clean up GPIO to release resources
        #GPIO.cleanup()

if __name__ == "__main__":
    # Activate the pump for 10 seconds
    activate_pump(10)