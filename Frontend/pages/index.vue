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
                            <p>Nous sommes des étudiants qui nous occupons du potager sur le toit de notre l'école. </p>
                            <p>Mais le potager manque de main d'œuvre surtout pour la période de plantation des semis.</p>
                            <p>Nous avons donc pensé à un système qui active ou non, à distance, l'irrigation des semis !</p>
                            <p>Notre solution se démarque par son contrôle total, sa facilité d'utilisation et son aspect écoresponsable.</p>
                        </div>
                    </div>
                    <div class="feature">
                        <h3>L'équipe</h3>
                        <p>#PPE24-T-355 </p>
                        <div class="zone_texte">
                            <div class="trombinoscope">
                                <div class="carousel-container">
                                    <div class="carousel-slides" ref="carouselSlides">
                                        <div class="carousel-slide">
                                            <img src="/assets/creditImages/lily.PNG" alt="Lily" />
                                            <p class="member-name">Lily</p>
                                            <p class="member-role">Chef de projet</p>
                                        </div>
                                        <div class="carousel-slide">
                                            <img src="/assets/creditImages/daria.PNG" alt="Daria" />
                                            <p class="member-name">Daria</p>
                                            <p class="member-role">Développeuse Backend</p>
                                        </div>
                                        <div class="carousel-slide">
                                            <img src="/assets/creditImages/jeremy.PNG" alt="Jérémy" />
                                            <p class="member-name">Jérémy</p>
                                            <p class="member-role">Développeur Frontend</p>
                                        </div>
                                        <div class="carousel-slide">
                                            <img src="/assets/creditImages/jeffrey.PNG" alt="Jeffrey" />
                                            <p class="member-name">Jeffrey</p>
                                            <p class="member-role">Développeur IoT</p>
                                        </div>
                                        <div class="carousel-slide">
                                            <img src="/assets/creditImages/maxence.PNG" alt="Maxence" />
                                            <p class="member-name">Maxence</p>
                                            <p class="member-role">Développeur IoT</p>
                                        </div>
                                        <div class="carousel-slide">
                                            <img src="/assets/creditImages/nicolas.PNG" alt="Nicolas" />
                                            <p class="member-name">Nicolas</p>
                                            <p class="member-role">Développeur Backend</p>
                                        </div>
                                        <div class="carousel-slide">
                                            <img src="/assets/creditImages/raphael.PNG" alt="Raphaël" />
                                            <p class="member-name">Raphaël</p>
                                            <p class="member-role">Développeur Frontend</p>
                                        </div>
                                    </div>
                                    <button class="carousel-btn prev" @click="prevSlide">&lt;</button>
                                    <button class="carousel-btn next" @click="nextSlide">&gt;</button>
                                </div>
                                <div class="carousel-dots">
                                    <span v-for="(_, index) in 7" :key="index" 
                                          :class="{ 'active': currentSlide === index }"
                                          @click="goToSlide(index)"></span>
                                </div>
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
            currentSlide: 0,
            slidesCount: 7,
            slideInterval: null
        };
    },
    mounted() {
        this.startSlideshow();
        window.addEventListener('resize', this.updateCarousel);
        this.updateCarousel();
    },
    beforeDestroy() {
        this.stopSlideshow();
        window.removeEventListener('resize', this.updateCarousel);
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
        nextSlide() {
            this.currentSlide = (this.currentSlide + 1) % this.slidesCount;
            this.updateCarousel();
            this.restartSlideshow();
        },
        prevSlide() {
            this.currentSlide = (this.currentSlide - 1 + this.slidesCount) % this.slidesCount;
            this.updateCarousel();
            this.restartSlideshow();
        },
        goToSlide(index) {
            this.currentSlide = index;
            this.updateCarousel();
            this.restartSlideshow();
        },
        updateCarousel() {
            if (this.$refs.carouselSlides) {
                const translateX = -this.currentSlide * 100;
                this.$refs.carouselSlides.style.transform = `translateX(${translateX}%)`;
                this.$refs.carouselSlides.style.transition = 'transform 0.5s ease-in-out';
            }
        },
        startSlideshow() {
            this.slideInterval = setInterval(() => {
                this.nextSlide();
            }, 3000); // Change d'image toutes les 3 secondes au lieu de 5
        },
        stopSlideshow() {
            clearInterval(this.slideInterval);
        },
        restartSlideshow() {
            this.stopSlideshow();
            this.startSlideshow();
        }
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

.trombinoscope{
    background-color: transparent;
    padding: 20px;
    border-radius: 10px;
    max-width: 600px;
    margin: 0 auto;
}

.carousel-container{
    position: relative;
    width: 100%;
    height: 350px;
    overflow: hidden;
    border-radius: 8px;
    box-shadow: none;
    margin-bottom: 20px;
}

.carousel-slides{
    display: flex;
    transition: transform 0.5s ease-in-out;
    height: 100%;
}

.carousel-slide{
    min-width: 100%;
    height: 100%;
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 10px;
    box-sizing: border-box;
    background-color: transparent;
}

.carousel-slide img{
    width: 200px;
    height: 200px;
    object-fit: cover;
    border-radius: 50%;
    margin-bottom: 15px;
    border: 3px solid #566d44;
}

.carousel-slide p.member-name{
    font-family: "Aeonik-Bold";
    color: #566d44;
    font-size: 1.3em;
    margin: 5px 0;
}

.carousel-slide p.member-role{
    font-family: "Aeonik-Regular";
    color: #666;
    font-size: 1em;
    margin-top: 0;
}

.carousel-btn{
    position: absolute;
    top: 50%;
    transform: translateY(-50%);
    background-color: rgba(86, 109, 68, 0.6);
    border: 2px solid #566d44;
    width: 40px;
    height: 40px;
    border-radius: 50%;
    font-size: 1.5em;
    color: white;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 10;
    transition: all 0.3s ease;
}

.carousel-btn:hover {
    background-color: rgba(86, 109, 68, 1);
    transform: translateY(-50%) scale(1.1);
    box-shadow: 0 0 8px rgba(86, 109, 68, 0.6);
}

.carousel-btn.prev{
    left: 10px;
}

.carousel-btn.next{
    right: 10px;
}

.carousel-dots{
    position: relative;
    display: flex;
    justify-content: center;
    gap: 10px;
    margin-top: 15px;
}

.carousel-dots span{
    width: 15px;
    height: 15px;
    border-radius: 50%;
    background-color: rgba(86, 109, 68, 0.4);
    border: 2px solid #566d44;
    cursor: pointer;
    transition: transform 0.3s, background-color 0.3s;
}

.carousel-dots span:hover {
    transform: scale(1.2);
}

.carousel-dots span.active{
    background-color: #566d44;
    transform: scale(1.2);
}
</style>