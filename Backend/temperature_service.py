"""
Service pour la gestion du capteur de température MCP9808
"""

import time
import smbus2
from datetime import datetime

# Configuration pour MCP9808
MCP9808_I2C_ADDR = 0x18  # Adresse I2C par défaut
MCP9808_REG_AMBIENT_TEMP = 0x05

class TemperatureSensor:
    def __init__(self):
        self.last_reading = None
        self.last_timestamp = None
    
    def read_temperature(self):
        """Lit la température du capteur MCP9808"""
        try:
            # Initialiser le bus I2C
            bus = smbus2.SMBus(1)
            
            # Lire la température
            data = bus.read_i2c_block_data(MCP9808_I2C_ADDR, MCP9808_REG_AMBIENT_TEMP, 2)
            raw_temp = (data[0] << 8) | data[1]
            
            # Extraire la température
            temp_c = (raw_temp & 0x0FFF) / 16.0
            if raw_temp & 0x1000:  # Bit de signe
                temp_c -= 256.0
            
            # Mettre à jour les attributs
            self.last_reading = round(temp_c, 2)
            self.last_timestamp = datetime.now()
            
            # Fermer le bus
            bus.close()
            
            return {
                "temperature": self.last_reading,
                "timestamp": self.last_timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                "status": "success"
            }
            
        except Exception as e:
            error_msg = str(e)
            print(f"Erreur de lecture du capteur: {error_msg}")
            
            # En cas d'erreur, retourner la dernière lecture valide si disponible
            if self.last_reading is not None:
                return {
                    "temperature": self.last_reading,
                    "timestamp": self.last_timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                    "status": "cached",
                    "error": error_msg
                }
            
            return {
                "temperature": None,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "status": "error",
                "error": error_msg
            }

# Créez une instance unique du service
temperature_service = TemperatureSensor()