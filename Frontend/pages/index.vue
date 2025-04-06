<template>
    <div class="home">
        
        <header class="hero">
            <div class="presentation">
                <img src="/assets/images/logo.png" alt="logo" class="icon-image" />
                <h1>GoutteAGoutte</h1>
                <p class="vertclair">Votre solution pour un jardinage intelligent et connecté.</p>
                <!-- <button @click="test">Test API</button>
                <button @click="explore">Test BDD</button> -->
                <button @click="goToPPE">Accéder à la plateforme</button>
            </div>
            
            <section class="features">
                <h2>Nos fonctionnalités</h2>
                <div class="feature" v-for="feature in features" :key="feature.id">
                    <h3>{{ feature.title }}</h3>
                    <p>{{ feature.description }}</p>
                </div>

                <div class="presentation">
                    <h2>Qui Sommes nous ?</h2>
                    <div class="feature">
                        <h3>Le projet</h3>
                        <div class="zone_texte">
                            <p>Nous sommes des étudiants qui nous occupons du potager sur le toit de notre l’école. </p>
                            <p>Mais le potager manque de main d’œuvre surtout pour la période de plantation des semis.</p>
                            <p>Nous avons donc pensé à un système qui active ou non, à distance, l'irrigation des semis !</p>
                            <p>Notre solution se démarque par son contrôle total, sa facilité d’utilisation et son aspect écoresponsable.</p>
                        </div>
                    </div>
                    <div class="feature">
                        <h3>L'équipe</h3>
                        <p>#PPE24-T-355 </p>
                        <div class="zone_texte">
                            <div class="tab_membres"> 
                                <p>trombinoscope </p>
                                <p>lien</p>
                            </div>
                        </div>
                    </div>
                
                </div>
                
            </section>
        </header>
        
      
    </div>
</template>

<script>
import Header_title from "~/components/header_title.vue";

export default {
    data() {
        return {
            features: [
                { id: 1, title: "Suivi des plantes", description: "Gardez un œil sur la santé de vos plantes." },
                { id: 2, title: "Arrosage automatique", description: "Programmez l'arrosage selon vos besoins." },
                { id: 3, title: "Conseils personnalisés", description: "Recevez des astuces adaptées à votre jardin." },
            ],
        };
    },
    methods: {
        async test() {
            const response = await $fetch("/api");
            console.log(response.message);
        },
        goToPPE() {
            this.$router.push('/ppe');
        },
        explore() {
            this.$router.push('/explore');
        },
    },
};
</script>

<style scoped>
.rows {
    grid-template-rows: 1fr;
}

.home {
    text-align: center;
    padding: 15px; 
}

.hero {
    background: linear-gradient(180deg, rgba(86,109,68,1) 0%, rgba(218,238,173,1) 50%);
    color: white;
    padding: 40px 20px;
    border-radius: 40px;
    margin-left: auto;
    margin-right: auto;
}

.hero h1 {
    font-family: "Aeonik-Bold";
    font-size: 2.8em;
    margin-bottom: 10px;
}

.hero p {
    font-family: "Aeonik-Regular";
    font-size: 1.4em;
    margin-bottom: 20px;
}

.hero button {
    font-family: "Aeonik-Bold";
    background-color: white;
    color: #566d44;
    border: none;
    padding: 10px 50px;
    margin-bottom: 60px;
    margin-top: 30px;
    cursor: pointer;
    border-radius: 5px;
    font-size: 1.4em;
    box-shadow: 0 0 5px #daeead;
}

.hero button:hover {
    background-color: #daeead;
}

.features {
    margin-top: 30px;
    color: black;
}

.features h2 {
    font-family: "Aeonik-Bold";
    font-size: 2em;
    margin-bottom: 20px;
    color: #566d44;
}

.feature {
    margin-bottom: 20px;
}

.feature h3 {
    font-family: "Aeonik-Bold";
    font-size: 1.5em;
    color: #555;
}

.feature p {
    font-family: "Aeonik-Regular";
    font-size: 1em;
    color: #555;
    margin-bottom: 10px;
}

.icon-image {
    height: 6em;
    /* width: auto; */
    padding: clamp(0.1rem, 0.7vw, 0.7rem);
    /* max-height: 400px; */
}

.vertclair{
    color: #daeead;
}

.presentation{
    margin-top: 60px;
}

.zone_texte{
    /* background-color: #a8b192; */
    padding: 10px 20px;
    margin: 5px;
    font-size: 1em;
    border-radius: 5px;
    max-width: 60rem;
    margin-left: auto;
    margin-right: auto;
}

.tab_membres{
    background-color: #c0c0c0;
    padding: 10px 20px;
    grid-template-columns: 1fr  1fr;   
}
</style>