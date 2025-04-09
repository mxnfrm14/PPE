"""
Service for managing humidity sensors through MCP3008 ADC
"""

import time
import spidev
from datetime import datetime

class HumiditySensor:
    def __init__(self):
        self.last_readings = {
            5: None,  # Place 5 maps to channel 0
            8: None,  # Place 8 maps to channel 1
            11: None  # Place 11 maps to channel 2
        }
        self.channel_mapping = {
            5: 0,  # Place 5 maps to channel 0
            8: 1,  # Place 8 maps to channel 1
            11: 2  # Place 11 maps to channel 2
        }
        self.last_timestamp = None
        
        # Initialize SPI
        try:
            self.spi = spidev.SpiDev()
            self.spi.open(0, 0)  # Use /dev/spidev0.0 for SPI communication
            self.spi.max_speed_hz = 50000
            self.spi_available = True
        except Exception as e:
            print(f"Failed to initialize SPI: {e}")
            self.spi_available = False
    
    def read_adc(self, channel):
        """Read a value from the MCP3008 ADC"""
        if not self.spi_available:
            return None
            
        if channel < 0 or channel > 7:
            raise ValueError("Channel must be between 0 and 7.")
        
        # SPI message to read from ADC
        command = [1, (8 + channel) << 4, 0]
        response = self.spi.xfer2(command)
        
        # Convert the raw value (10-bit value)
        result = ((response[1] & 3) << 8) + response[2]
        return result
    
    def raw_to_percentage(self, raw_value):
        """Convert raw ADC value to humidity percentage"""
        if raw_value is None:
            return None
            
        # For soil moisture sensors, we invert the percentage
        # Dry soil = high resistance = high ADC value
        # Wet soil = low resistance = low ADC value
        return 100 - (raw_value / 1023.0 * 100)
    
    def read_humidity(self, place=None):
        """Read humidity for a specific place or all places"""
        try:
            now = datetime.now()
            
            # If a specific place is requested
            if place is not None:
                if place not in self.channel_mapping:
                    return {
                        "status": "error",
                        "error": f"No humidity sensor for place {place}",
                        "timestamp": now.strftime("%Y-%m-%d %H:%M:%S")
                    }
                
                channel = self.channel_mapping[place]
                raw_value = self.read_adc(channel)
                humidity = self.raw_to_percentage(raw_value)
                
                if humidity is not None:
                    self.last_readings[place] = humidity
                    self.last_timestamp = now
                
                return {
                    "place": place, 
                    "humidity": round(humidity, 2) if humidity is not None else None,
                    "raw_value": raw_value,
                    "timestamp": now.strftime("%Y-%m-%d %H:%M:%S"),
                    "status": "success" if humidity is not None else "error"
                }
            
            # Read all places with sensors
            results = {}
            for place, channel in self.channel_mapping.items():
                raw_value = self.read_adc(channel)
                humidity = self.raw_to_percentage(raw_value)
                
                if humidity is not None:
                    self.last_readings[place] = humidity
                
                results[place] = {
                    "humidity": round(humidity, 2) if humidity is not None else None,
                    "raw_value": raw_value,
                    "timestamp": now.strftime("%Y-%m-%d %H:%M:%S"),
                    "status": "success" if humidity is not None else "error"
                }
            
            self.last_timestamp = now
            return results
            
        except Exception as e:
            error_msg = str(e)
            print(f"Error reading humidity sensor: {error_msg}")
            
            # In case of error, return the last valid reading if available
            if place is not None and self.last_readings.get(place) is not None:
                return {
                    "place": place,
                    "humidity": round(self.last_readings[place], 2),
                    "timestamp": self.last_timestamp.strftime("%Y-%m-%d %H:%M:%S") if self.last_timestamp else now.strftime("%Y-%m-%d %H:%M:%S"),
                    "status": "cached",
                    "error": error_msg
                }
            
            return {
                "humidity": None,
                "timestamp": now.strftime("%Y-%m-%d %H:%M:%S"),
                "status": "error",
                "error": error_msg
            }
    
    def cleanup(self):
        """Clean up SPI resources"""
        if self.spi_available:
            self.spi.close()

# Create a single instance of the service
humidity_service = HumiditySensor()