<script setup lang="ts">

// Plants for plantation management section
const plants = reactive([
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
        name: 'Carotte',
        plantedDate: '15 février',
        dureeGermination : "2 à 4 mois",
    },
    {
        id:3,
        name: 'Carotte',
        plantedDate: '15 février',
        dureeGermination : "2 à 4 mois",
    },

]);


// Function to edit plant details
const affichPlant = (index) => {
    alert(`Plus d'informations sur : ${plants[index].name}`);
    // Here you would open a modal or navigate to edit screen
};

</script>

<template>
  <div class="plants-grid" >
      <div class="plant-card" v-for="(plant, index) in plants" :key="index" >
          <div class="plant-header">{{ plant.name }}</div>
          <div class="plant-info text-blue-600/100">
              <p>Planté le : {{ plant.plantedDate }}</p>
              <p>Durée de germination : {{ plant.dureeGermination }}</p>
          
              <button class="afficher-plant-btn" @click="affichPlant(index)">
                <svg xmlns="http://www.w3.org/2000/svg" width="1em" height="1em" viewBox="0 0 14 14"><!-- Icon from Streamline by Streamline - https://creativecommons.org/licenses/by/4.0/ -->
                  <path fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" d="M7 13.5a6.5 6.5 0 1 0 0-13a6.5 6.5 0 0 0 0 13M7 4v6M4 7h6"></path>
                </svg>                            
                Afficher plus
              </button>
          </div>
        </div>  
</div>
</template>

<style scoped>

.plants-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 0.05rem;
    margin-bottom: 1.5rem;
    border-radius: 0.8rem;
}

.plant-card {
    background-color: #f9f9f9;
    border-radius: 0.8rem;
    overflow: hidden;
    margin: 0.6rem;
    box-shadow: 1px 3px 3px 1px #d8d8d8;
}

.plant-header {
    background-color: #95bd75;
    color: white;
    font-weight: bold;
    padding: 0.8rem 1rem;
}

.plant-info {
    padding: 1rem;
}

.plant-info p {
    margin: 0.3rem 0;
    color: #444;
}

.afficher-plant-btn {
    margin-top: 1rem;
    background-color: #f0f0f0;
    border: 1px solid #ddd;
    border-radius: 0.4rem;
    padding: 0.5rem 0.8rem;
    font-size: 0.8rem;
    display: flex;
    align-items: center;
    gap: 0.3rem;
    cursor: pointer;
    transition: background-color 0.2s;
}

.edit-plant-btn:hover {
    background-color: #e4e4e4;
}

.edit-plant-btn svg {
    width: 14px;
    height: 15px;
}

h3 {
    font-family: 'Aeonik-Medium', sans-serif;
    color: #333;
    margin-bottom: 1.5rem;
    font-size: 1.2rem;
}

@media (max-width: 768px) {
    .plants-grid {
        grid-template-columns: 1fr;
        /* max-width: 100px; */
    }
}
</style>

