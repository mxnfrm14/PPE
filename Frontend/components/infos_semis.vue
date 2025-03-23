<script setup lang="ts">
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
</script>

<template>
    <div class="infos" >
        <div v-for="(plant, index) in test" :key="index">
            <div class="info-card"  v-if="plant.id === 2">

                <!-- Ajouter code affichage des infos Semis ici -->
                <div class="text-info">
                    <p>  Methode recommendée : {{ plant.methodesReco }}</p>

                </div>


            </div>
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


.texte-info {
    padding: 1rem;
    margin: 30px;
    background-color: #973636;
}

</style>