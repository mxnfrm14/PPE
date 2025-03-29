<template>
    <div class="stat-card">
        <h4>{{ title }} </h4>
        <div class="stat-value">24°C</div>
        <!-- <div class="temp-range">
            <span>Min: 18°C</span>
            <span>Max: 28°C</span>
        </div> -->
    </div>
</template>

<script setup>
defineProps({
    title: {
  type: String,
  required: true,
},
});


</script>

<style scoped>

.stat-value {
    font-size: 1.8rem;
    font-weight: bold;
    color: #333;
    margin: 0.5rem 0;
}

.temp-range {
    display: flex;
    justify-content: space-between;
    color: #666;
    font-size: 0.9rem;
    margin-top: 0.5rem;
}

.stat-card {
    background-color: #f9f9f9;
    border-radius: 0.8rem;
    padding: 1rem;
    flex: 1;
}

</style>