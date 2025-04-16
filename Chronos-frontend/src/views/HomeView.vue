
<template>
    <div class="container">
        <h1 class="text-5xl">欢迎 👏</h1>
        
    </div>
</template>

<script setup>
import { ref } from 'vue';

import Checkbox from 'primevue/checkbox';

import RadioButton from 'primevue/radiobutton';

const ingredient = ref('');

</script>

<style scoped>
    #container{
        width: 100%;
        height: 100%;
        background-color: #f3f3f3;
        display: flex;
        justify-content: center;
        align-items: center;
        padding-left: 10%;
        padding-right: 10%;
    }
    .container {
    margin-left: 10vw;
    margin-right: 10vw;
    margin-top: 10vh;
    
    }
    
</style>