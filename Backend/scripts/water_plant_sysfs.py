#!/usr/bin/env python3
"""
water_plant_sysfs.py - Script pour contrôler l'arrosage via l'interface sysfs
Sans dépendance à RPi.GPIO ni à d'autres utilitaires

Usage: python3 water_plant_sysfs.py <position> <duration_minutes> [watering_id]
"""

import sys
import time
import logging
import requests
import os
from pathlib import Path

# Configuration du logging
log_dir = Path("/var/log/e-garden")
if not log_dir.exists():
    try:
        log_dir.mkdir(parents=True, exist_ok=True)
    except Exception:
        # Fallback à /tmp si on ne peut pas créer le répertoire
        log_dir = Path("/tmp")

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_dir / "watering.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger("water_plant_sysfs")

# Vérifier si nous sommes sur un système qui a l'interface sysfs GPIO
SYSFS_GPIO_PATH = Path("/sys/class/gpio")
SIMULATION_MODE = not SYSFS_GPIO_PATH.exists()

if SIMULATION_MODE:
    logger.warning("Interface sysfs GPIO non trouvée. Exécution en mode SIMULATION.")
else:
    logger.info("Interface sysfs GPIO trouvée. Exécution en mode MATÉRIEL.")

# URL de l'API pour mettre à jour le statut d'arrosage
API_ENDPOINT = "http://localhost:8000/api/plant/watering/status/internal"

# GPIO pour la pompe - sera activé avec n'importe quelle électrovanne
PUMP_GPIO = 6

# Mapping des positions aux GPIO des électrovannes
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

def write_file(path, content):
    """Écrit le contenu dans un fichier"""
    try:
        with open(path, 'w') as f:
            f.write(content)
        return True
    except Exception as e:
        logger.error(f"Erreur lors de l'écriture dans {path}: {str(e)}")
        return False

def gpio_export(gpio_pin):
    """Exporte un GPIO via sysfs"""
    if SIMULATION_MODE:
        logger.info(f"SIMULATION: Export du GPIO {gpio_pin}")
        return True
    
    # Vérifier si le GPIO est déjà exporté
    if Path(f"{SYSFS_GPIO_PATH}/gpio{gpio_pin}").exists():
        logger.info(f"GPIO {gpio_pin} déjà exporté")
        return True
    
    # Exporter le GPIO
    return write_file(f"{SYSFS_GPIO_PATH}/export", str(gpio_pin))

def gpio_set_direction(gpio_pin, direction):
    """Définit la direction d'un GPIO (in/out)"""
    if SIMULATION_MODE:
        logger.info(f"SIMULATION: Direction du GPIO {gpio_pin} définie sur {direction}")
        return True
    
    # Définir la direction (in/out)
    return write_file(f"{SYSFS_GPIO_PATH}/gpio{gpio_pin}/direction", direction)

def gpio_set_value(gpio_pin, value):
    """Définit la valeur d'un GPIO (0/1)"""
    if SIMULATION_MODE:
        logger.info(f"SIMULATION: Valeur du GPIO {gpio_pin} définie sur {value}")
        return True
    
    # Définir la valeur (0/1)
    return write_file(f"{SYSFS_GPIO_PATH}/gpio{gpio_pin}/value", str(value))

def gpio_unexport(gpio_pin):
    """Libère un GPIO via sysfs"""
    if SIMULATION_MODE:
        logger.info(f"SIMULATION: Libération du GPIO {gpio_pin}")
        return True
    
    # Vérifier si le GPIO est exporté
    if not Path(f"{SYSFS_GPIO_PATH}/gpio{gpio_pin}").exists():
        logger.info(f"GPIO {gpio_pin} déjà libéré")
        return True
    
    # Libérer le GPIO
    return write_file(f"{SYSFS_GPIO_PATH}/export", str(gpio_pin))

def setup_gpio(valve_gpio_pin):
    """Configure les pins GPIO en sortie"""
    # Exporter et configurer le GPIO de la pompe
    if not gpio_export(PUMP_GPIO):
        logger.error(f"Échec de l'export du GPIO {PUMP_GPIO}")
        return False
    
    if not gpio_set_direction(PUMP_GPIO, "out"):
        logger.error(f"Échec de la configuration du GPIO {PUMP_GPIO} en sortie")
        return False
    
    # Exporter et configurer le GPIO de l'électrovanne
    if not gpio_export(valve_gpio_pin):
        logger.error(f"Échec de l'export du GPIO {valve_gpio_pin}")
        return False
    
    if not gpio_set_direction(valve_gpio_pin, "out"):
        logger.error(f"Échec de la configuration du GPIO {valve_gpio_pin} en sortie")
        return False
    
    logger.info(f"GPIO {PUMP_GPIO} et {valve_gpio_pin} configurés avec succès")
    return True

def activate_outputs(valve_gpio_pin, active=True):
    """Active ou désactive la pompe et l'électrovanne"""
    # Pour la pompe : 1 = actif, 0 = inactif
    pump_value = 1 if active else 0
    
    # Pour l'électrovanne : 0 = actif (LOW), 1 = inactif (HIGH)
    valve_value = 0 if active else 1
    
    # Activer/désactiver la pompe
    if not gpio_set_value(PUMP_GPIO, pump_value):
        logger.error(f"Échec de l'activation/désactivation de la pompe (GPIO {PUMP_GPIO})")
        return False
    
    # Activer/désactiver l'électrovanne
    if not gpio_set_value(valve_gpio_pin, valve_value):
        logger.error(f"Échec de l'activation/désactivation de l'électrovanne (GPIO {valve_gpio_pin})")
        # Désactiver la pompe en cas d'échec
        if active:
            gpio_set_value(PUMP_GPIO, 0)
        return False
    
    action = "activés" if active else "désactivés"
    logger.info(f"GPIO {PUMP_GPIO} et {valve_gpio_pin} {action} avec succès")
    return True

def cleanup(valve_gpio_pin):
    """Nettoie les ressources GPIO"""
    if SIMULATION_MODE:
        logger.info("SIMULATION: Nettoyage terminé")
        return
    
    # Désactiver les sorties
    gpio_set_value(PUMP_GPIO, 0)
    gpio_set_value(valve_gpio_pin, 1)
    
    # Libérer les GPIO
    gpio_unexport(PUMP_GPIO)
    gpio_unexport(valve_gpio_pin)
    
    logger.info("Nettoyage terminé")

def water_plant(position, duration_minutes):
    """
    Active l'arrosage pour la position spécifiée, pendant la durée donnée
    
    Args:
        position (int): Numéro de position (1-12) à activer
        duration_minutes (int): Durée en minutes de l'activation
    """
    if position not in VALVE_MAPPING:
        logger.error(f"Position invalide: {position}")
        return False
        
    valve_gpio_pin = VALVE_MAPPING[position]
    logger.info(f"Position {position} correspond au GPIO {valve_gpio_pin}")
    
    try:
        # Configuration des GPIO
        if not setup_gpio(valve_gpio_pin):
            return False
        
        # Activation de la pompe et de l'électrovanne
        logger.info(f"Activation de la pompe (GPIO {PUMP_GPIO}) et électrovanne (GPIO {valve_gpio_pin}) pour {duration_minutes} minutes")
        if not activate_outputs(valve_gpio_pin, active=True):
            return False
        
        # Attente pendant la durée spécifiée
        duration_seconds = duration_minutes * 60
        if SIMULATION_MODE and duration_seconds > 10:
            logger.info(f"SIMULATION: Attente réduite à 5 secondes au lieu de {duration_seconds} secondes")
            time.sleep(5)
        else:
            time.sleep(duration_seconds)
        
        # Désactivation de la pompe et de l'électrovanne
        logger.info(f"Désactivation de la pompe (GPIO {PUMP_GPIO}) et électrovanne (GPIO {valve_gpio_pin})")
        activate_outputs(valve_gpio_pin, active=False)
        
        logger.info(f"Arrosage terminé avec succès pour la position {position} (GPIO {valve_gpio_pin})")
        return True
    except Exception as e:
        logger.error(f"Erreur pendant l'arrosage: {str(e)}")
        # S'assurer que tout est désactivé en cas d'erreur
        try:
            activate_outputs(valve_gpio_pin, active=False)
        except:
            pass
        return False
    finally:
        cleanup(valve_gpio_pin)

def update_status(watering_id, success):
    """Met à jour le statut d'arrosage dans la base de données via l'API"""
    try:
        response = requests.post(
            API_ENDPOINT,
            params={"watering_id": watering_id, "success": success}
        )
        
        if response.status_code == 200:
            logger.info(f"Statut d'arrosage mis à jour avec succès pour l'ID {watering_id}")
        else:
            logger.error(f"Échec de la mise à jour du statut: {response.status_code} - {response.text}")
    except Exception as e:
        logger.error(f"Erreur lors de la mise à jour du statut: {str(e)}")

def main():
    if len(sys.argv) < 3:
        logger.error("Usage: python3 water_plant_sysfs.py <position> <duration_minutes> [watering_id]")
        sys.exit(1)
    
    try:
        position = int(sys.argv[1])
        duration_minutes = int(sys.argv[2])
        watering_id = sys.argv[3] if len(sys.argv) > 3 else None
        
        success = water_plant(position, duration_minutes)
        
        if watering_id:
            update_status(watering_id, success)
        
        sys.exit(0 if success else 1)
        
    except ValueError:
        logger.error("La position et la durée doivent être des entiers")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Erreur inattendue: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()