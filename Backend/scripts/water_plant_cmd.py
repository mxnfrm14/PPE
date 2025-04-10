#!/usr/bin/env python3
"""
water_plant_cmd.py - Script pour contrôler l'arrosage sans dépendre de RPi.GPIO
Utilise les commandes système pour contrôler les GPIO

Usage: python3 water_plant_cmd.py <position> <duration_minutes> [watering_id]
"""

import sys
import time
import logging
import requests
import os
import subprocess
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

logger = logging.getLogger("water_plant")

# Vérifier si nous sommes sur un système qui a des commandes GPIO
SIMULATION_MODE = not (os.path.exists("/usr/bin/raspi-gpio") or os.path.exists("/usr/bin/gpio"))
if SIMULATION_MODE:
    logger.warning("Commandes GPIO non trouvées. Exécution en mode SIMULATION.")
else:
    logger.info("Commandes GPIO trouvées. Exécution en mode MATÉRIEL.")

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

def run_gpio_command(command):
    """Exécute une commande GPIO et retourne son résultat"""
    try:
        result = subprocess.run(command, shell=True, check=True, 
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE, 
                               text=True)
        return True, result.stdout
    except subprocess.CalledProcessError as e:
        return False, f"Erreur: {e.stderr}"

def setup_gpio(valve_gpio_pin):
    """Configure les pins GPIO en sortie"""
    if SIMULATION_MODE:
        logger.info(f"SIMULATION: Configuration des GPIO {valve_gpio_pin} et {PUMP_GPIO} en sortie")
        return True
    
    # Configuration du GPIO de la pompe en sortie
    pump_cmd = f"raspi-gpio set {PUMP_GPIO} op"
    success, output = run_gpio_command(pump_cmd)
    if not success:
        logger.error(f"Échec de la configuration du GPIO de la pompe: {output}")
        return False
    
    # Configuration du GPIO de l'électrovanne en sortie
    valve_cmd = f"raspi-gpio set {valve_gpio_pin} op"
    success, output = run_gpio_command(valve_cmd)
    if not success:
        logger.error(f"Échec de la configuration du GPIO de l'électrovanne: {output}")
        return False
    
    logger.info(f"GPIO {PUMP_GPIO} et {valve_gpio_pin} configurés en sortie avec succès")
    return True

def activate_outputs(valve_gpio_pin, active=True):
    """Active ou désactive la pompe et l'électrovanne"""
    if SIMULATION_MODE:
        state = "activés" if active else "désactivés"
        logger.info(f"SIMULATION: GPIO {PUMP_GPIO} et {valve_gpio_pin} {state}")
        return True
    
    # Définir les états à appliquer (LOW active les électrovannes, HIGH active la pompe)
    pump_state = "dh" if active else "dl"  # 'dh' = drive high, 'dl' = drive low
    valve_state = "dl" if active else "dh"  # Activé à l'état bas pour les électrovannes
    
    # Activation/désactivation de la pompe
    pump_cmd = f"raspi-gpio set {PUMP_GPIO} {pump_state}"
    success, output = run_gpio_command(pump_cmd)
    if not success:
        logger.error(f"Échec de l'activation/désactivation de la pompe: {output}")
        return False
    
    # Activation/désactivation de l'électrovanne
    valve_cmd = f"raspi-gpio set {valve_gpio_pin} {valve_state}"
    success, output = run_gpio_command(valve_cmd)
    if not success:
        logger.error(f"Échec de l'activation/désactivation de l'électrovanne: {output}")
        # Désactiver la pompe en cas d'échec
        if active:
            run_gpio_command(f"raspi-gpio set {PUMP_GPIO} dl")
        return False
    
    action = "activés" if active else "désactivés"
    logger.info(f"GPIO {PUMP_GPIO} et {valve_gpio_pin} {action} avec succès")
    return True

def cleanup():
    """Nettoyage - rien à faire avec les commandes GPIO"""
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
        logger.error("Usage: python3 water_plant_cmd.py <position> <duration_minutes> [watering_id]")
        sys.exit(1)
    
    try:
        position = int(sys.argv[1])
        duration_minutes = int(sys.argv[2])
        watering_id = sys.argv[3] if len(sys.argv) > 3 else None
        
        success = water_plant(position, duration_minutes)
        
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