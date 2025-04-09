import spidev
import time

# Initialisation du bus SPI (MCP3008)
spi = spidev.SpiDev()
spi.open(0, 0)  # Utilisation de /dev/spidev0.0 pour la communication SPI
spi.max_speed_hz = 50000

# Fonction pour lire une valeur à partir de l'ADC MCP3008
def read_adc(channel):
    if channel < 0 or channel > 7:
        raise ValueError("Le canal doit être compris entre 0 et 7.")
    
    # Message SPI pour lire l'ADC
    command = [1, (8 + channel) << 4, 0]
    response = spi.xfer2(command)
    
    # Conversion de la valeur lue (valeur sur 10 bits)
    result = ((response[1] & 3) << 8) + response[2]
    return result

# Fonction pour convertir la valeur brute en pourcentage
def raw_to_percentage(raw_value):
    # Nous supposons que la plage des capteurs est de 0 à 1023
    # Par exemple, 0 correspond à 0% d'humidité, et 1023 correspond à 100% d'humidité
    return (raw_value / 1023.0) * 100

# Boucle pour lire et afficher les valeurs des capteurs
try:
    while True:
        # Lire les données des capteurs
        ch0_value = read_adc(0)
        ch1_value = read_adc(1)
        ch2_value = read_adc(2)
        
        # Convertir les valeurs brutes en pourcentages
        ch0_percentage = raw_to_percentage(ch0_value)
        ch1_percentage = raw_to_percentage(ch1_value)
        ch2_percentage = raw_to_percentage(ch2_value)
        
        # Afficher les valeurs brutes et les pourcentages dans le terminal
        print(f"Capteur CH0 (Humidité 1) - Valeur brute: {ch0_value}, Pourcentage d'humidité: {ch0_percentage:.2f}%")
        print(f"Capteur CH1 (Humidité 2) - Valeur brute: {ch1_value}, Pourcentage d'humidité: {ch1_percentage:.2f}%")
        print(f"Capteur CH2 (Humidité 3) - Valeur brute: {ch2_value}, Pourcentage d'humidité: {ch2_percentage:.2f}%")
        print("-" * 50)  # Ligne de séparation pour plus de clarté
        
        # Attendre 1 seconde avant de lire à nouveau
        time.sleep(1)

except KeyboardInterrupt:
    print("Lecture interrompue par l'utilisateur.")
finally:
    # Fermer la connexion SPI proprement
    spi.close()
