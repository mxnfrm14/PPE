<script setup lang="ts">
import { reactive } from 'vue';

// Accept the selected plant ID as a prop
const props = defineProps({
    selectedPlantId: {
        type: Number,
        default: null
    }
});

const test = reactive([
    {
        id:1,
        name: 'Carotte',
        plantedDate: '15 février',
        dureeGermination : "2 à 4 mois",
        periodeSemis: "mars à juillet",
        temperatureMin: 15,
        temperatireMax: 20,
        methodesReco: "godets profonds (10-12 cm), espacer 2-3 graines puis les recouvrir",
        conditionCulture:"Sol : legerement enrichi (compost ou fertilisant). Ameubli, drainant et peu caillouteux à sablonneux. \nBesoin en arrosage : régulier, le sol doit rester frais et humide",
        txHumidReco: 70, /* en % */
        txHumidMesure: 80,
    },
    {
        id:2,
        name: 'AAA',
        plantedDate: 'AAAAA',
        dureeGermination : "2 à 4 mois",
        periodeSemis: "mars à juillet",
        temperatureMin: 15,
        temperatireMax: 20,
        methodesReco: "CA MARCHE godets profonds (10-12 cm), espacer 2-3 graines puis les recouvrir",
        conditionCulture:"Sol : legerement enrichi (compost ou fertilisant). Ameubli, drainant et peu caillouteux à sablonneux. \nBesoin en arrosage : régulier, le sol doit rester frais et humide",
        txHumidReco: 70, /* en % */
        txHumidMesure: 80,
    },
]);

// Get the selected plant based on the ID
const getSelectedPlant = () => {
    if (!props.selectedPlantId) return null;
    return test.find(plant => plant.id === props.selectedPlantId);
};
</script>

<template>
    <div class="infos">
        <!-- Display info only when a plant is selected -->
        <div v-if="props.selectedPlantId" class="info-card">
            <div v-if="getSelectedPlant()" class="text-info">
                <p class="info-title">Méthode recommandée:</p>
                <p>{{ getSelectedPlant().methodesReco }}</p>
                
                <p class="info-title">Période de semis:</p>
                <p>{{ getSelectedPlant().periodeSemis }}</p>
                
                <p class="info-title">Température idéale:</p>
                <p>{{ getSelectedPlant().temperatureMin }}°C - {{ getSelectedPlant().temperatireMax }}°C</p>
                
                <p class="info-title">Conditions de culture:</p>
                <p>{{ getSelectedPlant().conditionCulture }}</p>
            </div>
            <div v-else class="not-found">
                Informations non disponibles
            </div>
        </div>
        <div v-else class="no-selection">
            <p>Veuillez sélectionner un semis pour voir les informations détaillées</p>
        </div>
    </div>
</template>

<style scoped>
.infos {
    gap: 0.05rem;
    margin-bottom: 1.5rem;
    border-radius: 1.6rem;
}

.info-card {
    background-color: #f9f9f9;
    border-radius: 0.8rem;
    overflow: hidden;
    margin: 0.6rem;
    box-shadow: 1px 3px 3px 1px #d8d8d8;
    padding: 1rem;
}

.text-info {
    padding: 0.5rem;
}

.info-title {
    font-weight: bold;
    margin-top: 1rem;
    margin-bottom: 0.2rem;
    color: #95bd75;
}

.no-selection, .not-found {
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 2rem;
    color: #888;
    font-style: italic;
    text-align: center;
}
</style>