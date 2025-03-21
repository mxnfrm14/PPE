<template>
  <div class="custom-frame">
    <div class="icon-background" :style="{ backgroundColor: iconBackgroundColor }">
      <img :src="iconPath" alt="icon" class="icon-image" />
    </div>
    <div class="text-container">
      <h1>{{ title }} </h1>
      <h2>{{ subtitle }}</h2>
    </div>
  </div>
</template>

<script setup>
defineProps({
iconPath: {
  type: String ,
  required: true,
},
iconBackgroundColor: {
  type: String,
  required: true,
},
title: {
  type: String,
  required: true,
},
subtitle: {
  type: String,
  required: true,
},
});
</script>

<style scoped>
.custom-frame {
width: 100%;
max-width: 18rem;
min-width: 10.5rem;
height: 100%;
background-color: white;
display: flex;
flex-direction: row;
align-items: center;
padding: clamp(0.4rem, 1vw, 1rem);
border-radius: min(1rem, 20px);
gap: 0.8rem;
}

.icon-background {
display: flex;
align-items: center;
justify-content: center;
width: 16%;
height: auto;
border-radius: clamp(0.5rem, 0.7vw, 0.8rem);
}

.icon-image {
width: 100%;
height: auto;
padding: clamp(0.1rem, 0.7vw, 0.7rem);
}

.text-container {
display: flex;
flex-direction: column;
align-items: flex-start;
}

.custom-frame h1 {
font-size: clamp(0.7rem, 0.8vw, 1rem);
margin: 2px;
font-family: 'Aeonik-Medium';
color: #000000;
}

.custom-frame h2 {
font-size: clamp(0.6rem, 0.8vw, 0.9rem);
font-family: 'Aeonik-Regular';
color: #7B7B7B;
margin: 0;
}

/* Responsive - Mobile */
@media screen and (max-width: 768px) {
.custom-frame {
  flex-direction: column;
  align-items: center;
  text-align: center;
  gap: 0.5rem;
  padding: 1rem;
}

.icon-background {
  width: 3rem;
  height: 3rem;
}

.icon-image {
  width: 2rem;
  height: 2rem;
}

.text-container {
  align-items: center;
}

.custom-frame h1 {
  font-size: 1rem;
}

.custom-frame h2 {
  font-size: 0.85rem;
}
}
</style>
