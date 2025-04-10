<template>
    <div class="landing-page">
      <!-- Hero Section -->
      <section class="hero">
        <div class="hero-content container">
          <div class="hero-left">
            <img src="/assets/images/logo.png" alt="GoutteAGoutte Logo" class="hero-logo" />
            <h1>GoutteAGoutte</h1>
            <p class="tagline">Votre solution pour un jardinage intelligent et connecté</p>
            <button @click="goToPPE" class="cta-button">
              <span>Accéder à la plateforme</span>
              <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M5 12h14"></path>
                <path d="m12 5 7 7-7 7"></path>
              </svg>
            </button>
          </div>
          <div class="hero-right">
            <div class="hero-image">
              <div class="illustration">
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 450 450" fill="none">
                  <path d="M225 410c90.575 0 164-73.425 164-164S315.575 82 225 82 61 155.425 61 246s73.425 164 164 164z" fill="#daeead" />
                  <path d="M347 155c0 11.598-9.402 21-21 21s-21-9.402-21-21 9.402-21 21-21 21 9.402 21 21z" fill="#566d44" />
                  <path d="M228 126c0 13.255-10.745 24-24 24s-24-10.745-24-24 10.745-24 24-24 24 10.745 24 24z" fill="#566d44" />
                  <path d="M321 274c0 8.284-6.716 15-15 15s-15-6.716-15-15 6.716-15 15-15 15 6.716 15 15z" fill="#566d44" />
                  <path fill-rule="evenodd" clip-rule="evenodd" d="M202.992 390.008c5.023-24.246 5.023-48.492 0-72.738-24.246-5.023-48.492-5.023-72.738 0-5.023 24.246-5.023 48.492 0 72.738 24.246 5.023 48.492 5.023 72.738 0z" fill="#566d44" />
                  <path d="M139 207c-25.957 0-47-21.043-47-47s21.043-47 47-47 47 21.043 47 47-21.043 47-47 47z" stroke="#566d44" stroke-width="6" />
                  <path d="M310 354c-19.33 0-35-15.67-35-35s15.67-35 35-35 35 15.67 35 35-15.67 35-35 35z" stroke="#566d44" stroke-width="6" />
                  <path d="M223 268c-3.866 0-7-3.134-7-7s3.134-7 7-7 7 3.134 7 7-3.134 7-7 7z" fill="#566d44" />
                  <path d="M232 376c-5.523 0-10-4.477-10-10s4.477-10 10-10 10 4.477 10 10-4.477 10-10 10z" fill="#566d44" />
                  <path d="M225 82v164M61 246h328" stroke="#566d44" stroke-width="2" stroke-dasharray="6 6" />
                  <path d="M212 259c0 7.18-5.82 13-13 13s-13-5.82-13-13 5.82-13 13-13 13 5.82 13 13z" stroke="#566d44" stroke-width="2" />
                  <path d="M175 318c0 6.075-4.925 11-11 11s-11-4.925-11-11 4.925-11 11-11 11 4.925 11 11z" fill="#566d44" />
                  <path fill-rule="evenodd" clip-rule="evenodd" d="M217 181.669c4.377 10.563 8.754 21.126 13.131 31.689a1.2 1.2 0 0 1-2.211.917c-3.642-8.79-7.285-17.581-10.928-26.371L217 181.669zm15.193 33.188l.006-.014-.006.014z" fill="#566d44" />
                  <path d="M218 182c0 2.761-2.239 5-5 5s-5-2.239-5-5 2.239-5 5-5 5 2.239 5 5z" fill="#566d44" />
                  <path d="M230 213c0 2.761-2.239 5-5 5s-5-2.239-5-5 2.239-5 5-5 5 2.239 5 5z" fill="#566d44" />
                  <path fill-rule="evenodd" clip-rule="evenodd" d="M168 203c4.418 0 8-3.582 8-8s-3.582-8-8-8-8 3.582-8 8 3.582 8 8 8zm0 4c6.627 0 12-5.373 12-12s-5.373-12-12-12-12 5.373-12 12 5.373 12 12 12z" fill="#566d44" />
                  <path d="M193 335a4 4 0 1 1-8 0 4 4 0 0 1 8 0z" fill="#566d44" />
                  <path d="M281.892 230.673a14.287 14.287 0 1 1-20.219-20.218 14.287 14.287 0 0 1 20.219 20.218z" stroke="#566d44" stroke-width="4" />
                  <path fill-rule="evenodd" clip-rule="evenodd" d="M271.571 115.428c3.905-3.905 10.237-3.905 14.142 0l14.142 14.143c3.905 3.905 3.905 10.237 0 14.142-3.905 3.905-10.237 3.905-14.142 0l-14.142-14.142c-3.905-3.905-3.905-10.237 0-14.143z" stroke="#566d44" stroke-width="4" />
                  <path fill-rule="evenodd" clip-rule="evenodd" d="M280 380c0-11.046-8.954-20-20-20s-20 8.954-20 20 8.954 20 20 20 20-8.954 20-20zm4 0c0-13.255-10.745-24-24-24s-24 10.745-24 24 10.745 24 24 24 24-10.745 24-24z" fill="#566d44" />
                </svg>
              </div>
            </div>
          </div>
        </div>
        <div class="wave-bottom">
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1440 120">
            <path fill="#ffffff" fill-opacity="1" d="M0,64L80,69.3C160,75,320,85,480,80C640,75,800,53,960,42.7C1120,32,1280,32,1360,32L1440,32L1440,120L1360,120C1280,120,1120,120,960,120C800,120,640,120,480,120C320,120,160,120,80,120L0,120Z"></path>
          </svg>
        </div>
      </section>
  
      <!-- Features Section -->
      <section class="features">
        <div class="container">
          <h2 class="section-title">Nos fonctionnalités</h2>
          <div class="features-grid">
            <div class="feature-card" v-for="feature in features" :key="feature.id">
              <div class="feature-icon" :class="`icon-${feature.id}`">
                <svg v-if="feature.id === 1" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M12 22a7 7 0 0 0 7-7c0-2-1-3.9-3-5.5s-3.5-4-4-6.5c-.5 2.5-2 4.9-4 6.5C6 11.1 5 13 5 15a7 7 0 0 0 7 7z"></path>
                </svg>
                <svg v-else-if="feature.id === 2" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M19 21V5a2 2 0 0 0-2-2H7a2 2 0 0 0-2 2v16"></path>
                  <path d="M12 11.5v-6"></path>
                  <path d="M9.5 8h5"></path>
                  <path d="M10 21h4"></path>
                  <path d="M4 15.5A3.5 3.5 0 0 1 7.5 12"></path>
                  <path d="M20 15.5a3.5 3.5 0 0 0-3.5-3.5"></path>
                  <path d="M4 19a4 4 0 0 1 4-4"></path>
                  <path d="M20 19a4 4 0 0 0-4-4"></path>
                </svg>
                <svg v-else xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <circle cx="12" cy="12" r="10"></circle>
                  <line x1="12" y1="8" x2="12" y2="12"></line>
                  <line x1="12" y1="16" x2="12.01" y2="16"></line>
                </svg>
              </div>
              <h3>{{ feature.title }}</h3>
              <p>{{ feature.description }}</p>
            </div>
          </div>
        </div>
      </section>
  
      <!-- About Section -->
      <section class="about">
        <div class="container">
          <h2 class="section-title">Qui Sommes-nous ?</h2>
          
          <div class="about-card">
            <h3>Le projet</h3>
            <div class="about-content">
              <div class="about-text">
                <p>Nous sommes des étudiants qui nous occupons du potager sur le toit de notre école.</p>
                <p>Mais le potager manque de main d'œuvre surtout pour la période de plantation des semis.</p>
                <p>Nous avons donc pensé à un système qui active ou non, à distance, l'irrigation des semis !</p>
                <p>Notre solution se démarque par son contrôle total, sa facilité d'utilisation et son aspect écoresponsable.</p>
              </div>
              <div class="about-image">
                <div class="plant-illustration">
                  <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200" fill="none">
                    <path d="M100 180c-5.523 0-10-4.477-10-10V80c0-5.523 4.477-10 10-10s10 4.477 10 10v90c0 5.523-4.477 10-10 10z" fill="#566d44"></path>
                    <path d="M100 70c15.464 0 28-12.536 28-28S115.464 14 100 14 72 26.536 72 42s12.536 28 28 28z" fill="#daeead"></path>
                    <path d="M70 100c0-11.046-8.954-20-20-20s-20 8.954-20 20 8.954 20 20 20 20-8.954 20-20z" fill="#daeead"></path>
                    <path d="M170 100c0-11.046-8.954-20-20-20s-20 8.954-20 20 8.954 20 20 20 20-8.954 20-20z" fill="#daeead"></path>
                    <path d="M70 140c0-11.046-8.954-20-20-20s-20 8.954-20 20 8.954 20 20 20 20-8.954 20-20z" fill="#daeead"></path>
                    <path d="M170 140c0-11.046-8.954-20-20-20s-20 8.954-20 20 8.954 20 20 20 20-8.954 20-20z" fill="#daeead"></path>
                  </svg>
                </div>
              </div>
            </div>
          </div>
          
          <!-- Team Section -->
          <div class="team-card">
            <h3>L'équipe</h3>
            <p class="team-id">#PPE24-T-355</p>
            
            <div class="project-links">
              <a href="https://github.com/mxnfrm14/PPE" target="_blank" rel="noopener noreferrer" class="github-link">
                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="currentColor">
                  <path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/>
                </svg>
                <span>Voir notre projet sur GitHub</span>
              </a>
            </div>
            
            <div class="carousel-container">
              <div class="carousel-slides" ref="carouselSlides">
                <div v-for="(member, index) in teamMembers" :key="index" class="carousel-slide">
                  <div class="member-avatar">
                    <img :src="member.image" :alt="member.name" />
                  </div>
                  <p class="member-name">{{ member.name }}</p>
                  <p class="member-role">{{ member.role }}</p>
                  <p class="member-major">{{ member.major }}</p>
                  <a :href="member.linkedin" target="_blank" rel="noopener noreferrer" class="linkedin-button">
                    <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
                      <path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433c-1.144 0-2.063-.926-2.063-2.065 0-1.138.92-2.063 2.063-2.063 1.14 0 2.064.925 2.064 2.063 0 1.139-.925 2.065-2.064 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/>
                    </svg>
                    <span>LinkedIn</span>
                  </a>
                </div>
              </div>
              
              <button class="carousel-btn prev" @click="prevSlide">
                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="m15 18-6-6 6-6"></path>
                </svg>
              </button>
              <button class="carousel-btn next" @click="nextSlide">
                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="m9 18 6-6-6-6"></path>
                </svg>
              </button>
            </div>
            
            <div class="carousel-dots">
              <span v-for="(_, index) in teamMembers.length" :key="index" 
                    :class="{ 'active': currentSlide === index }"
                    @click="goToSlide(index)"></span>
            </div>
          </div>
        </div>
      </section>
  
      <!-- Footer -->
      <footer class="footer">
        <div class="container">
          <div class="footer-content">
            <div class="footer-logo">
              <img src="/assets/images/logo.png" alt="GoutteAGoutte Logo" class="footer-logo-img" />
              <span>GoutteAGoutte</span>
            </div>
            <p class="footer-tagline">Votre solution pour un jardinage intelligent et connecté</p>
            <div class="footer-actions">
              <button @click="goToPPE" class="footer-button">Accéder à la plateforme</button>
            </div>
          </div>
          <div class="footer-bottom">
            <p>&copy; {{ new Date().getFullYear() }} GoutteAGoutte - Équipe #PPE24-T-355. Tous droits réservés.</p>
          </div>
        </div>
      </footer>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        features: [
          { id: 1, title: "Suivi des plantes", description: "Gardez un œil sur la santé de vos plantes en temps réel grâce à nos capteurs intelligents." },
          { id: 2, title: "Arrosage automatique", description: "Programmez l'arrosage selon les besoins spécifiques de chaque plante et économisez de l'eau." },
          { id: 3, title: "Conseils personnalisés", description: "Recevez des astuces adaptées à votre jardin pour optimiser la croissance de vos plantes." },
        ],
        teamMembers: [
          { 
            name: "Maxence Fromentin", 
            role: "Chef de projet", 
            major: "Majeure CREATE",
            image: "/assets/creditImages/maxence.png",
            linkedin: "https://www.linkedin.com/in/maxence-fromentin-654618256/" 
          },
          { 
            name: "Raphaël Pinard", 
            role: "Electronicien", 
            major: "Majeure Système Embarqué",
            image: "/assets/creditImages/raphael.PNG",
            linkedin: "https://www.linkedin.com/in/rapha%C3%ABl-pinard-507643269/" 
          },
          { 
            name: "Jérémy Eyraud", 
            role: "Technicien", 
            major: "Majeure Système Embarqué",
            image: "/assets/creditImages/jeremy.PNG",
            linkedin: "https://www.linkedin.com/in/j%C3%A9r%C3%A9my-eyraud-70b254253/" 
          },
          { 
            name: "Lily Wunsch", 
            role: "Développeur Frontend", 
            major: "Majeure Énergies et Environnement",
            image: "/assets/creditImages/lily.PNG",
            linkedin: "https://www.linkedin.com/in/lily-wunsch-784555252/" 
          },
          { 
            name: "Jeffrey Jacquin", 
            role: "Responsable communication", 
            major: "Majeure Énergies et Environnement",
            image: "/assets/creditImages/jeffrey.PNG",
            linkedin: "https://www.linkedin.com/in/jeffrey-jacquin-415590252/" 
          },
          { 
            name: "Nicolas Thorrez", 
            role: "Développeur Backend", 
            major: "Majeure Cloud",
            image: "/assets/creditImages/nicolas.PNG",
            linkedin: "https://www.linkedin.com/in/nicolasthorrez/" 
          },
          { 
            name: "Daria Cousy", 
            role: "Architecte Backend", 
            major: "Majeure Énergies et Environnement",
            image: "/assets/creditImages/daria.PNG",
            linkedin: "https://www.linkedin.com/in/daria-cousy/" 
          }
        ],
        currentSlide: 0,
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
      goToPPE() {
        this.$router.push('/ppe');
      },
      nextSlide() {
        this.currentSlide = (this.currentSlide + 1) % this.teamMembers.length;
        this.updateCarousel();
        this.restartSlideshow();
      },
      prevSlide() {
        this.currentSlide = (this.currentSlide - 1 + this.teamMembers.length) % this.teamMembers.length;
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
        }
      },
      startSlideshow() {
        this.slideInterval = setInterval(() => {
          this.nextSlide();
        }, 5000);
      },
      stopSlideshow() {
        clearInterval(this.slideInterval);
      },
      restartSlideshow() {
        this.stopSlideshow();
        this.startSlideshow();
      }
    }
  };
  </script>
  
  <style scoped>
  /* Global Styles */
  .landing-page {
    font-family: 'Aeonik-Regular', sans-serif;
    color: #333;
    overflow-x: hidden;
  }
  
  .container {
    width: 100%;
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 20px;
  }
  
  .section-title {
    font-family: 'Aeonik-Bold', sans-serif;
    font-size: 2.5rem;
    text-align: center;
    color: #566d44;
    margin-bottom: 2rem;
  }
  
  /* Hero Section */
  .hero {
    background: linear-gradient(135deg, #566d44 0%, #7b9d60 100%);
    color: white;
    padding: 6rem 0 0;
    position: relative;
    overflow: hidden;
  }
  
  .hero-content {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding-bottom: 4rem;
  }
  
  .hero-left {
    flex: 1;
    max-width: 600px;
    position: relative;
    z-index: 5;
  }
  
  .cta-wrapper {
    position: relative;
    z-index: 10;
    margin-bottom: 20px;
  }
  
  .hero-right {
    flex: 1;
    display: flex;
    justify-content: center;
  }
  
  .hero-logo {
    width: 100px;
    height: auto;
    margin-bottom: 1rem;
  }
  
  .hero h1 {
    font-family: 'Aeonik-Bold', sans-serif;
    font-size: 3.5rem;
    margin: 0 0 1rem;
  }
  
  .tagline {
    font-size: 1.5rem;
    margin-bottom: 2rem;
    opacity: 0.9;
  }
  
  .cta-button {
    background-color: white;
    color: #566d44;
    border: none;
    border-radius: 50px;
    padding: 15px 30px;
    font-size: 1.2rem;
    font-weight: bold;
    cursor: pointer;
    display: flex;
    align-items: center;
    gap: 10px;
    transition: all 0.3s ease;
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
    position: relative;
    z-index: 10;
  }
  
  .cta-button:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 15px rgba(0, 0, 0, 0.15);
    background-color: #daeead;
  }
  
  .hero-image {
    max-width: 400px;
    animation: float 6s ease-in-out infinite;
  }
  
  .illustration {
    width: 100%;
    height: auto;
  }
  
  .wave-bottom {
    position: absolute;
    bottom: 0;
    left: 0;
    width: 100%;
    line-height: 0;
    z-index: 1;
  }
  
  /* Features Section */
  .features {
    padding: 5rem 0;
    background-color: #fff;
  }
  
  .features-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
    gap: 2rem;
  }
  
  .feature-card {
    background-color: white;
    border-radius: 20px;
    padding: 2rem;
    text-align: center;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.05);
    transition: all 0.3s ease;
    border: 1px solid #f0f0f0;
  }
  
  .feature-card:hover {
    transform: translateY(-10px);
    box-shadow: 0 15px 35px rgba(0, 0, 0, 0.1);
  }
  
  .feature-icon {
    width: 70px;
    height: 70px;
    margin: 0 auto 1.5rem;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 50%;
    background-color: #daeead;
    color: #566d44;
  }
  
  .feature-icon svg {
    width: 35px;
    height: 35px;
  }
  
  .feature-card h3 {
    font-family: 'Aeonik-Bold', sans-serif;
    font-size: 1.5rem;
    margin-bottom: 1rem;
    color: #566d44;
  }
  
  .feature-card p {
    color: #666;
    line-height: 1.6;
  }
  
  /* About Section */
  .about {
    padding: 5rem 0;
    background-color: #f9f9f9;
  }
  
  .about-card, .team-card {
    background-color: white;
    border-radius: 20px;
    padding: 2.5rem;
    margin-bottom: 3rem;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.05);
  }
  
  .about-card h3, .team-card h3 {
    font-family: 'Aeonik-Bold', sans-serif;
    font-size: 2rem;
    color: #566d44;
    text-align: center;
    margin-bottom: 1.5rem;
  }
  
  .about-content {
    display: flex;
    align-items: center;
    gap: 3rem;
  }
  
  .about-text {
    flex: 3;
  }
  
  .about-text p {
    margin-bottom: 1rem;
    line-height: 1.8;
    color: #555;
  }
  
  .about-image {
    flex: 2;
    display: flex;
    justify-content: center;
  }
  
  .plant-illustration {
    width: 100%;
    max-width: 250px;
  }
  
  .team-id {
    text-align: center;
    font-size: 1.2rem;
    color: #566d44;
    font-weight: bold;
    margin-bottom: 2rem;
  }
  
  /* Project Links */
  .project-links {
    display: flex;
    justify-content: center;
    margin-bottom: 2rem;
  }
  
  .github-link {
    display: flex;
    align-items: center;
    gap: 10px;
    text-decoration: none;
    background-color: #333;
    color: white;
    padding: 10px 20px;
    border-radius: 30px;
    font-size: 1rem;
    transition: all 0.3s ease;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  }
  
  .github-link:hover {
    background-color: #000;
    transform: translateY(-2px);
    box-shadow: 0 6px 10px rgba(0, 0, 0, 0.15);
  }
  
  .github-link svg {
    width: 24px;
    height: 24px;
  }
  
  /* Member info */
  .member-major {
    color: #666;
    font-size: 0.9rem;
    margin-bottom: 1rem;
    font-style: italic;
  }
  
  .linkedin-button {
    display: flex;
    align-items: center;
    gap: 6px;
    text-decoration: none;
    background-color: #0077b5;
    color: white;
    padding: 8px 15px;
    border-radius: 20px;
    font-size: 0.9rem;
    transition: all 0.3s ease;
    margin-top: 0.8rem;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  }
  
  .linkedin-button:hover {
    background-color: #005e8b;
    transform: translateY(-2px);
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
  }
  
  /* Carousel */
  .carousel-container {
    position: relative;
    width: 100%;
    height: 400px;
    overflow: hidden;
    border-radius: 15px;
    margin-bottom: 1.5rem;
  }
  
  .carousel-slides {
    display: flex;
    transition: transform 0.5s ease-in-out;
    height: 100%;
  }
  
  .carousel-slide {
    min-width: 100%;
    height: 100%;
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 1rem;
    box-sizing: border-box;
  }
  
  .member-avatar {
    width: 180px;
    height: 180px;
    border-radius: 50%;
    overflow: hidden;
    margin-bottom: 1.5rem;
    border: 5px solid #daeead;
    box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
  }
  
  .member-avatar img {
    width: 100%;
    height: 100%;
    object-fit: cover;
  }
  
  .member-name {
    font-family: 'Aeonik-Bold', sans-serif;
    font-size: 1.5rem;
    color: #566d44;
    margin: 0.5rem 0;
  }
  
  .member-role {
    color: #333;
    font-size: 1.1rem;
    font-weight: 500;
  }
  
  .carousel-btn {
    position: absolute;
    top: 50%;
    transform: translateY(-50%);
    width: 40px;
    height: 40px;
    border-radius: 50%;
    border: none;
    background-color: rgba(86, 109, 68, 0.8);
    color: white;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    transition: all 0.3s ease;
    z-index: 2;
  }
  
  .carousel-btn:hover {
    background-color: rgba(86, 109, 68, 1);
    transform: translateY(-50%) scale(1.1);
  }
  
  .carousel-btn.prev {
    left: 10px;
  }
  
  .carousel-btn.next {
    right: 10px;
  }
  
  .carousel-dots {
    display: flex;
    justify-content: center;
    gap: 10px;
  }
  
  .carousel-dots span {
    width: 12px;
    height: 12px;
    border-radius: 50%;
    background-color: #ddd;
    cursor: pointer;
    transition: all 0.3s ease;
  }
  
  .carousel-dots span.active {
    background-color: #566d44;
    transform: scale(1.2);
  }
  
  /* Footer */
  .footer {
    background-color: #566d44;
    color: white;
    padding: 4rem 0 2rem;
  }
  
  .footer-content {
    display: flex;
    flex-direction: column;
    align-items: center;
    text-align: center;
    margin-bottom: 3rem;
  }
  
  .footer-logo {
    display: flex;
    align-items: center;
    gap: 10px;
    margin-bottom: 1rem;
  }
  
  .footer-logo-img {
    width: 60px;
    height: auto;
  }
  
  .footer-logo span {
    font-family: 'Aeonik-Bold', sans-serif;
    font-size: 1.8rem;
  }
  
  .footer-tagline {
    font-size: 1.1rem;
    margin-bottom: 2rem;
    opacity: 0.9;
  }
  
  .footer-button {
    background-color: white;
    color: #566d44;
    border: none;
    border-radius: 50px;
    padding: 12px 25px;
    font-size: 1rem;
    font-weight: bold;
    cursor: pointer;
    transition: all 0.3s ease;
  }
  
  .footer-button:hover {
    background-color: #daeead;
  }
  
  .footer-bottom {
    text-align: center;
    padding-top: 2rem;
    border-top: 1px solid rgba(255, 255, 255, 0.2);
    font-size: 0.9rem;
    opacity: 0.7;
  }
  
  /* Animations */
  @keyframes float {
    0% {
      transform: translateY(0px);
    }
    50% {
      transform: translateY(-20px);
    }
    100% {
      transform: translateY(0px);
    }
  }
  
  /* Responsive Styles */
  @media (max-width: 992px) {
    .hero-content {
      flex-direction: column;
      text-align: center;
    }
    
    .hero-left {
      margin-bottom: 3rem;
    }
    
    .hero h1 {
      font-size: 3rem;
    }
    
    .about-content {
      flex-direction: column;
    }
    
    .cta-button {
      margin: 0 auto;
    }
  }
  
  @media (max-width: 768px) {
    .section-title {
      font-size: 2rem;
    }
    
    .hero {
      padding-top: 4rem;
    }
    
    .hero h1 {
      font-size: 2.5rem;
    }
    
    .tagline {
      font-size: 1.2rem;
    }
    
    .feature-card {
      padding: 1.5rem;
    }
    
    .about-card, .team-card {
      padding: 1.5rem;
    }
    
    .carousel-container {
      height: 420px;
    }
  }
  
  @media (max-width: 480px) {
    .hero h1 {
      font-size: 2rem;
    }
    
    .hero-logo {
      width: 80px;
    }
    
    .feature-icon {
      width: 60px;
      height: 60px;
    }
    
    .feature-card h3 {
      font-size: 1.3rem;
    }
    
    .about-card h3, .team-card h3 {
      font-size: 1.5rem;
    }
    
    .carousel-container {
      height: 450px;
    }
    
    .member-avatar {
      width: 150px;
      height: 150px;
    }
    
    .linkedin-button {
      padding: 6px 12px;
    }
  }
  </style>