<script setup>
import { ref } from 'vue';
import TheNavBar from '@/components/TheNavBar.vue';
import Button from 'primevue/button';

</script>

<template>
  <TheNavBar />
  <div> 
        <router-view></router-view>
  </div>
    
</template>

<style scoped>

</style>
