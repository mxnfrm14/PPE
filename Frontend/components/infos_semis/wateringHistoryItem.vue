<template>
    <div class="watering-event">
        <div class="watering-event-marker" :class="{ 'recent': isRecent }"></div>
        <div class="watering-event-content">
            <div class="watering-event-header">
                <span class="watering-date">{{ formattedDate }}</span>
                <span class="watering-time">{{ formattedTime }}</span>
            </div>
            <div class="watering-event-details">
                <div class="watering-amount">
                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <path d="M12 22a7 7 0 0 0 7-7c0-2-1-3.9-3-5.5s-3.5-4-4-6.5c-.5 2.5-2 4.9-4 6.5C6 11.1 5 13 5 15a7 7 0 0 0 7 7z"></path>
                    </svg>
                    <span>{{ amount }} ml</span>
                </div>
                <div class="watering-duration" v-if="duration">
                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <circle cx="12" cy="12" r="10"></circle>
                        <polyline points="12 6 12 12 16 14"></polyline>
                    </svg>
                    <span>{{ duration }} min</span>
                </div>
                <div class="watering-elapsed">{{ timeElapsed }}</div>
            </div>
        </div>
    </div>
</template>

<script setup>
const props = defineProps({
    dateTime: {
        type: String,
        required: true
    },
    amount: {
        type: [Number, String],
        required: true
    },
    duration: {
        type: [Number, String],
        default: null
    },
    isRecent: {
        type: Boolean,
        default: false
    },
    formattedDate: {
        type: String,
        required: true
    },
    formattedTime: {
        type: String,
        required: true
    },
    timeElapsed: {
        type: String,
        required: true
    }
});
</script>

<style scoped>
.watering-event {
    display: flex;
    padding: 0.8rem 0;
    border-bottom: 1px solid #eee;
    position: relative;
}

.watering-event-marker {
    width: 12px;
    height: 12px;
    background-color: #95bd75;
    border-radius: 50%;
    margin-right: 15px;
    margin-top: 5px;
}

.watering-event-marker.recent {
    background-color: #3498db;
    box-shadow: 0 0 0 3px rgba(52, 152, 219, 0.2);
}

.watering-event-content {
    flex: 1;
}

.watering-event-header {
    display: flex;
    justify-content: space-between;
    margin-bottom: 5px;
}

.watering-date {
    font-weight: 500;
    color: #333;
}

.watering-time {
    color: #777;
}

.watering-event-details {
    display: flex;
    flex-wrap: wrap;
    gap: 15px;
    align-items: center;
}

.watering-amount, .watering-duration {
    display: flex;
    align-items: center;
    gap: 5px;
    font-size: 0.9rem;
    color: #555;
}

.watering-elapsed {
    font-size: 0.85rem;
    color: #888;
    font-style: italic;
    margin-left: auto;
}
</style>
