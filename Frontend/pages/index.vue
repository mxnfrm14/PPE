<template>
    <div class="home">
        <Header_title title="E-Garden" subtitle="Votre jardin connecté" />
        <header class="hero">
            <h1>Bienvenue sur E-Garden</h1>
            <p>Votre solution pour un jardinage intelligent et connecté.</p>
            <button @click="test">test api</button>
            <button @click="explore">Test BDD</button>
            <button @click="goToPPE">PPE</button>
        </header>
        <section class="features">
            <h2>Nos fonctionnalités</h2>
            <div class="feature" v-for="feature in features" :key="feature.id">
                <h3>{{ feature.title }}</h3>
                <p>{{ feature.description }}</p>
            </div>
        </section>
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
.home {
    text-align: center;
    padding: 20px;
}

.hero {
    background-color: #4caf50;
    color: white;
    padding: 50px 20px;
}

.hero h1 {
    font-family: "Aeonik-Bold";
    font-size: 2.5em;
    margin-bottom: 10px;
}

.hero p {
    font-family: "Aeonik-Regular";
    font-size: 1.2em;
    margin-bottom: 20px;
}

.hero button {
    font-family: "Aeonik-Bold";
    background-color: white;
    color: #4caf50;
    border: none;
    padding: 10px 20px;
    font-size: 1em;
    cursor: pointer;
    border-radius: 5px;
}

.hero button:hover {
    background-color: #45a049;
}

.features {
    margin-top: 30px;
}

.features h2 {
    font-family: "Aeonik-Bold";
    font-size: 2em;
    margin-bottom: 20px;
}

.feature {
    margin-bottom: 20px;
}

.feature h3 {
    font-family: "Aeonik-Bold";
    font-size: 1.5em;
    color: #4caf50;
}

.feature p {
    font-family: "Aeonik-Regular";
    font-size: 1em;
    color: #555;
}
</style>