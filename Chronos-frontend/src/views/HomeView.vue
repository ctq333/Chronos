<script setup>
//import TheNavbar from './components/TheNavBar.vue';

import InputText from 'primevue/inputtext';
import { ref } from 'vue';


const msg = ref('');
</script>
<template>
   <InputText v-model="msg" />
</template>
