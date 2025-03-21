<template>
    <div class="custom-frame">
        <div class="text-container">
            <h1>{{ title }}</h1>
            <h2>{{ subtitle }}</h2>
        </div>
        <div class="toggle-switch" @click="toggleMode">
            <div class="toggle-track" :class="{ 'active': !isManualMode }">
                <div class="toggle-indicator" :class="{ 'active': !isManualMode }"></div>
            </div>
            <span class="toggle-label">{{ isManualMode ? 'Mode Manuel' : 'Mode Auto' }}</span>
        </div>
    </div>
</template>

<script setup>
import { ref } from 'vue';

const props = defineProps({
    title: {
        type: String,
        required: true,
    },
    subtitle: {
        type: String,
        required: true,
    },
});

const isManualMode = ref(false);

const toggleMode = () => {
    isManualMode.value = !isManualMode.value;
};
</script>

<style scoped>
.custom-frame {
    width: 100%;
    max-width: 30rem;
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

.toggle-switch {
    margin-left: auto;
    display: flex;
    flex-direction: column;
    align-items: center;
    cursor: pointer;
}

.toggle-track {
    position: relative;
    width: 3.5rem;
    height: 1.5rem;
    background-color: #cccccc;
    border-radius: 1rem;
    transition: background-color 0.3s ease;
}

.toggle-track.active {
    background-color: #95bd75;
}

.toggle-indicator {
    position: absolute;
    top: 0.15rem;
    left: 0.15rem;
    width: 1.2rem;
    height: 1.2rem;
    background-color: white;
    border-radius: 50%;
    transition: transform 0.3s ease;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.2);
}

.toggle-indicator.active {
    transform: translateX(2rem);
}

.toggle-label {
    margin-top: 0.3rem;
    font-size: clamp(0.6rem, 0.7vw, 0.8rem);
    font-family: 'Aeonik-Regular';
    color: #333;
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

    .toggle-switch {
        margin: 0.5rem 0 0;
    }
}
</style>