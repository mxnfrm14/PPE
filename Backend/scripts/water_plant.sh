#!/bin/bash

# Ce script est un wrapper qui exécute water_plant.py avec le Python du système
# Usage: ./water_plant.sh <position> <duration> [watering_id]

# Récupérer le chemin du répertoire où se trouve ce script
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Chemin complet vers le script Python
PYTHON_SCRIPT="$SCRIPT_DIR/water_plant.py"

# Chemin vers le Python du système
SYSTEM_PYTHON="/usr/bin/python3"

# Vérifier que les arguments nécessaires sont fournis
if [ "$#" -lt 2 ]; then
    echo "Usage: $0 <position> <duration> [watering_id]"
    exit 1
fi

# S'assurer que le script Python est exécutable
chmod +x "$PYTHON_SCRIPT"

# Exécuter le script Python avec sudo et le Python du système
if [ "$#" -eq 2 ]; then
    # Sans watering_id
    sudo $SYSTEM_PYTHON "$PYTHON_SCRIPT" "$1" "$2"
else
    # Avec watering_id
    sudo $SYSTEM_PYTHON "$PYTHON_SCRIPT" "$1" "$2" "$3"
fi

# Récupérer le code de sortie du script Python
exit $?