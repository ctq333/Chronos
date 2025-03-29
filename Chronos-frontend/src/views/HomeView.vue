
<template>
   <div class="card flex justify-center">
       <div class="flex flex-wrap gap-4">
           <div class="flex items-center gap-2">
               <RadioButton v-model="ingredient" inputId="ingredient1" name="pizza" value="Cheese" />
               <label for="ingredient1">Cheese</label>
           </div>
           <div class="flex items-center gap-2">
               <RadioButton v-model="ingredient" inputId="ingredient2" name="pizza" value="Mushroom" />
               <label for="ingredient2">Mushroom</label>
           </div>
           <div class="flex items-center gap-2">
               <RadioButton v-model="ingredient" inputId="ingredient3" name="pizza" value="Pepper" />
               <label for="ingredient3">Pepper</label>
           </div>
           <div class="flex items-center gap-2">
               <RadioButton v-model="ingredient" inputId="ingredient4" name="pizza" value="Onion" />
               <label for="ingredient4">Onion</label>
           </div>
       </div>
   </div>
</template>

<script setup>
import { ref } from 'vue';

import RadioButton from 'primevue/radiobutton';

const ingredient = ref('');
</script>
