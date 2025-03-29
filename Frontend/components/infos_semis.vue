<script setup lang="ts">
import { ref, reactive } from 'vue';

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
        name: 'Carotte (1)',
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
        name: 'AAA (2)',
        plantedDate: 'AAAAA',
        dureeGermination : "2 à 4 mois",
        periodeSemis: "mars à juillet",
        temperatureMin: 15,
        temperatireMax: 20,
        methodesReco: "id2 godets profonds (10-12 cm), espacer 2-3 graines puis les recouvrir",
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


// Function to water plant manually
const waterPlantManually = () => {
    // Here you would call your API to trigger watering
    alert(`Arrosage manuel de ${getSelectedPlant().name} déclenché`);


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

                <p class="info-title">Durée de germination:</p>
                <p>{{ getSelectedPlant()?.dureeGermination }}</p>
                
                <p class="info-title">Température idéale:</p>
                <p>{{ getSelectedPlant().temperatureMin }}°C - {{ getSelectedPlant().temperatireMax }}°C</p>
                
                <p class="info-title">Conditions de culture:</p>
                <p>{{ getSelectedPlant().conditionCulture }}</p>

                <p class="info-title">Taux humidité recommandé:</p>
                <p>{{ getSelectedPlant().txHumidReco }} %</p>

                <p class="info-title">Taux humidité mesuré:</p>
                <p>{{ getSelectedPlant()?.txHumidMesure }} %</p>
                <div class="centrer">
                    <button class="arrosage-plant-btn" @click="waterPlantManually" > 
                        <svg xmlns="http://www.w3.org/2000/svg" width="1.2em" height="1.2em" viewBox="0 0 14 14"><!-- Icon from Streamline by Streamline - https://creativecommons.org/licenses/by/4.0/ -->
                            <path fill="none" stroke=white stroke-linecap="round" stroke-linejoin="round" d="M11.5 9C11.5 6.51 7 .5 7 .5S2.5 6.51 2.5 9a4.5 4.5 0 0 0 9 0Z"/>
                        </svg>                    
                        Arrosage
                    </button>
                </div>
                
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

.arrosage-plant-btn {
    margin-top: 1rem;
    display: flex;
    align-items: center;
    gap: 0.6rem;
    cursor: pointer;
    transition: background-color 0.2s;
    width: 8rem;
    background-color: #3498db;
    color: white;
    border: none;
    border-radius: 0.5rem;
    padding: 0.5rem 1rem;
    font-size: 0.9rem;

}

.centrer{
    margin-top: 1rem;
    align-items: center;
    justify-items: center;
}
</style>